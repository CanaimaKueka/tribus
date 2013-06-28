import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts


RSYNC_EXCLUDE = (
    '.DS_Store',
    '.hg',
    '*.pyc',
    '*.example',
    '*.db',
    'media/admin',
    'media/attachments',
    'local_settings.py',
    'fabfile.py',
    'bootstrap.py',
)

env.home = '/home/caktus/'
env.project = 'caktus_website'


def _setup_path():
    env.root = os.path.join(env.home, 'www', env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.settings = '%(project)s.settings_%(environment)s' % env


def staging():
    """ use staging environment on remote host"""
    env.user = 'caktus'
    env.environment = 'staging'
    env.hosts = ['173.203.208.254']
    _setup_path()


def production():
    """ use production environment on remote host"""
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    run('mkdir -p %(root)s' % env)
    run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
    create_virtualenv()
    deploy()
    update_requirements()


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --distribute'
    run('virtualenv %s %s' % (args, env.virtualenv_root))


def deploy():
    """ rsync code to remote host """
    require('root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    # defaults rsync options:
    # -pthrvz
    # -p preserve permissions
    # -t preserve times
    # -h output numbers in a human-readable format
    # -r recurse into directories
    # -v increase verbosity
    # -z compress file data during the transfer
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )
    touch()


def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    requirements = os.path.join(env.code_root, 'requirements')
    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'apps.txt')]
        run(' '.join(cmd))


def touch():
    """ touch wsgi file to trigger reload """
    require('code_root', provided_by=('staging', 'production'))
    apache_dir = os.path.join(env.code_root, 'apache')
    with cd(apache_dir):
        run('touch %s.wsgi' % env.environment)


def update_apache_conf():
    """ upload apache configuration to remote host """
    require('root', provided_by=('staging', 'production'))
    source = os.path.join('apache', '%(environment)s.conf' % env)
    dest = os.path.join(env.home, 'apache.conf.d')
    put(source, dest, mode=0755)
    apache_reload()


def configtest():    
    """ test Apache configuration """
    require('root', provided_by=('staging', 'production'))
    run('apache2ctl configtest')


def apache_reload():    
    """ reload Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 reload')


def apache_restart():    
    """ restart Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    run('sudo /etc/init.d/apache2 restart')


def symlink_django():    
    """ create symbolic link so Apache can serve django admin media """
    require('root', provided_by=('staging', 'production'))
    admin_media = os.path.join(env.virtualenv_root,
                               'src/django/django/contrib/admin/media/')
    media = os.path.join(env.code_root, 'media/admin')
    if not files.exists(media):
        run('ln -s %s %s' % (admin_media, media))


def reset_local_media():
    """ Reset local media from remote host """
    require('root', provided_by=('staging', 'production'))
    media = os.path.join(env.code_root, 'media', 'upload')
    local('rsync -rvaz %s@%s:%s media/' % (env.user, env.hosts[0], media))


# -------------------

from fabric.api import *
# Default release is 'current'
env.release = 'current'

def production():
  """Production server settings"""
  env.settings = 'production'
  env.user = 'myproject'
  env.path = '/home/%(user)s/sites/myproject' % env
  env.hosts = ['mydomain.com']

def setup():
  """
  Setup a fresh virtualenv and install everything we need so it's ready to deploy to
  """
  run('mkdir -p %(path)s; cd %(path)s; virtualenv --no-site-packages .; mkdir releases; mkdir shared;' % env)
  clone_repo()
  checkout_latest()
  install_requirements()

def deploy():
  """Deploy the latest version of the site to the server and restart nginx"""
  checkout_latest()
  install_requirements()
  symlink_current_release()
  migrate()
  restart_server()

def clone_repo():
  """Do initial clone of the git repo"""
  run('cd %(path)s; git clone /home/%(user)s/git/repositories/myproject.git repository' % env)

def checkout_latest():
  """Pull the latest code into the git repo and copy to a timestamped release directory"""
  import time
  env.release = time.strftime('%Y%m%d%H%M%S')
  run("cd %(path)s/repository; git pull origin master" % env)
  run('cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*' % env)

def install_requirements():
  """Install the required packages using pip"""
  run('cd %(path)s; %(path)s/bin/pip install -r ./releases/%(release)s/requirements.txt' % env)

def symlink_current_release():
  """Symlink our current release, uploads and settings file"""
  with settings(warn_only=True):
    run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)
  run('cd %(path)s; ln -s %(release)s releases/current' % env)
  """ production settings"""
  run('cd %(path)s/releases/current/; cp settings_%(settings)s.py myproject/settings.py' % env)
  with settings(warn_only=True):
    run('rm %(path)s/shared/static' % env)
    run('cd %(path)s/releases/current/static/; ln -s %(path)s/releases/%(release)s/static %(path)s/shared/static ' %env)

def migrate():
  """Run our migrations"""
  run('cd %(path)s/releases/current; ../../bin/python manage.py syncdb --noinput --migrate' % env)

def rollback():
  """
  Limited rollback capability. Simple loads the previously current
  version of the code. Rolling back again will swap between the two.
  """
  run('cd %(path)s; mv releases/current releases/_previous;' % env)
  run('cd %(path)s; mv releases/previous releases/current;' % env)
  run('cd %(path)s; mv releases/_previous releases/previous;' %env)
  restart_server()

def restart_server():
  """Restart the web server"""
  with settings(warn_only=True):
    sudo('kill -9 `cat /tmp/project-master_helpmamme.pid`')
    sudo('rm /tmp/project-master_helpmamme.pid /tmp/uwsgi_helpmamme.sock')
  run('cd %(path)s/releases/current; %(path)s/bin/uwsgi --ini %(path)s/releases/current/uwsgi.ini' % env)
  sudo('/etc/init.d/nginx restart')