#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pwd
import sys
import site
from fabric.api import *

from tribus import BASEDIR
from tribus.config.pkg import (debian_dependencies, f_workenv_preseed,
                               f_sql_preseed, f_users_ldif, f_python_dependencies)


def development():
    env.user = pwd.getpwuid(os.getuid()).pw_name
    env.root = 'root'
    env.environment = 'development'
    env.hosts = ['localhost']
    env.basedir = BASEDIR
    env.virtualenv_dir = os.path.join(env.basedir, 'virtualenv')
    env.virtualenv_args = ' '.join(['--clear', '--no-site-packages', '--distribute'])
    env.virtualenv_activate = os.path.join(env.virtualenv_dir, 'bin', 'activate')
    env.settings = 'tribus.config.web'
    env.sudo_prompt = 'Executed'
    env.f_python_dependencies = f_python_dependencies


def environment():
    configure_sudo()
    preseed_packages()
    install_packages()
    configure_postgres()
    populate_ldap()
    create_virtualenv()
    update_virtualenv()
    configure_django()
    deconfigure_sudo()


def configure_sudo():
    with settings(command='su root -c "echo \'%(user)s ALL= NOPASSWD: ALL\' > /etc/sudoers.d/tribus"' % env):
        local('%(command)s' % env)


def deconfigure_sudo():
    with settings(command='sudo rm -rf /etc/sudoers.d/tribus' % env):
        local('%(command)s' % env)


def preseed_packages():
    with settings(command='sudo debconf-set-selections %s' % f_workenv_preseed):
        local('%(command)s' % env)


def install_packages():
    with settings(command='sudo DEBIAN_FRONTEND="noninteractive" \
aptitude install --assume-yes --allow-untrusted \
-o DPkg::Options::="--force-confmiss" \
-o DPkg::Options::="--force-confnew" \
-o DPkg::Options::="--force-overwrite" \
%s' % ' '.join(debian_dependencies)):
        local('%(command)s' % env)


def configure_postgres():
    with settings(command=[
        'sudo echo "postgres:tribus" | chpasswd',
        'sudo su postgres -c \"psql -U postgres -f %s\"' % f_sql_preseed,
    ]):
        local('%s' % '; '.join(env.command))


def populate_ldap():
    env.ldap_passwd = 'tribus'
    env.ldap_writer = 'cn=admin,dc=tribus,dc=org'
    env.ldap_server = 'localhost'
    env.ldap_base = 'dc=tribus,dc=org'
    env.users_ldif = f_users_ldif
    with settings(command='ldapsearch -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -h "%(ldap_server)s" -b "%(ldap_base)s" \
-LLL "(uid=*)" | perl -p00e \'s/\\r?\\n //g\' | grep "dn: "| \
sed \'s/dn: //g\' | sed \'s/ /_@_/g\'' % env):
        ldap_entries = local('%(command)s' % env, capture=True)

    for ldap_entry in ldap_entries.split():
        env.ldap_entry = ldap_entry
        with settings(command='ldapdelete -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -h "%(ldap_server)s" "%(ldap_entry)s"' % env):
            local('%(command)s' % env)

    with settings(command='ldapadd -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -h "%(ldap_server)s" -f "%(users_ldif)s"' % env):
        local('%(command)s' % env)


def create_virtualenv():
    with cd('%(basedir)s' % env):
        with settings(command='virtualenv %(virtualenv_args)s %(virtualenv_dir)s' % env):
            local('%(command)s' % env)


def update_virtualenv():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s pip install -r %(f_python_dependencies)s' % env)


def py_activate_virtualenv():
    os.environ['PATH'] = os.path.join(env.virtualenv_dir, 'bin') + os.pathsep + os.environ['PATH']
    site.addsitedir(os.path.join(env.virtualenv_dir, 'lib', 'python%s' % sys.version[:3], 'site-packages'))
    sys.prefix = env.virtualenv_dir
    sys.path.insert(0, env.virtualenv_dir)


def configure_django():
    syncdb_django()
    createsuperuser_django()


def createsuperuser_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py createsuperuser --noinput --username admin --email admin@localhost.com' % env)

    py_activate_virtualenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
    from django.contrib.auth.models import User

    u = User.objects.get(username__exact='admin')
    u.set_password('tribus')
    u.save()


def syncdb_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py syncdb --noinput' % env)
            local('%(command)s python manage.py migrate' % env)


def runserver_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py runserver' % env)


def update_po():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py update_po' % env):
            local('%(command)s' % env)


def create_pot():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py create_pot' % env):
            local('%(command)s' % env)


def build_html():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py build_html ' % env):
            local('%(command)s' % env)


def build_img():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py build_img ' % env):
            local('%(command)s' % env)


def build_man():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py build_man ' % env):
            local('%(command)s' % env)


def build_mo():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py build_mo ' % env):
            local('%(command)s' % env)


def sdist():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py sdist ' % env):
            local('%(command)s' % env)


def bdist():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py bdist ' % env):
            local('%(command)s' % env)


def install():
    with cd('%(basedir)s' % env):
        with settings(command='python setup.py install ' % env):
            local('%(command)s' % env)

#         with settings(command='sed -i -e \'s/# Translations template for Tribus./# $(POTITLE)./\' \
# -e \'s/# Copyright (C).*/# Copyright (C) $(YEAR) $(AUTHOR)/\' \
# -e \'s/# This file is distributed under.*/same license as the $(PACKAGE) package./\' \
# -e \'s/# FIRST AUTHOR <EMAIL@ADDRESS>/#\\n# Translators:\\n# $(AUTHOR) <$(EMAIL)>, $(YEAR)/\' \
# -e \'s/"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"/"PO-Revision-Date: $(PODATE)\\n"/\' \
# -e \'s/"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"/"Last-Translator: $(AUTHOR) <$(EMAIL)>\\n"/\' \
# -e \'s/"Language-Team: LANGUAGE <LL@li.org>\\n"/"Language-Team: $(POTEAM) <$(MAILIST)>\\n"/\' \
# -e \'s/"Language: \\n"/"Language: English\\n"/g\' $(POTFILE)' % env):
#             local('%(command)s' % env)

# import os

# from fabric.api import *
# from fabric.contrib.project import rsync_project
# from fabric.contrib import files, console
# from fabric import utils
# from fabric.decorators import hosts


# RSYNC_EXCLUDE = (
#     '.DS_Store',
#     '.hg',
#     '*.pyc',
#     '*.example',
#     '*.db',
#     'media/admin',
#     'media/attachments',
#     'local_settings.py',
#     'fabfile.py',
#     'bootstrap.py',
# )

# env.virtualenv = '/home/caktus/'
# env.project = 'caktus_website'


# def _setup_path():
#     env.root = os.path.join(env.home, 'www', env.environment)
#     env.code_root = os.path.join(env.root, env.project)
#     env.virtualenv_root = os.path.join(env.root, 'env')
#     env.settings = '%(project)s.settings_%(environment)s' % env


# def staging():
#     """ use staging environment on remote host"""
#     env.user = 'caktus'
#     env.environment = 'staging'
#     env.hosts = ['173.203.208.254']
#     _setup_path()


# def production():
#     """ use production environment on remote host"""
#     utils.abort('Production deployment not yet implemented.')


# def bootstrap():
#     """ initialize remote host environment (virtualenv, deploy, update) """
#     require('root', provided_by=('staging', 'production'))
#     run('mkdir -p %(root)s' % env)
#     run('mkdir -p %s' % os.path.join(env.home, 'www', 'log'))
#     create_virtualenv()
#     deploy()
#     update_requirements()


# def create_virtualenv():
#     """ setup virtualenv on remote host """
#     require('virtualenv_root', provided_by=('staging', 'production'))
#     args = '--clear --distribute'
#     run('virtualenv %s %s' % (args, env.virtualenv_root))


# def deploy():
#     """ rsync code to remote host """
#     require('root', provided_by=('staging', 'production'))
#     if env.environment == 'production':
#         if not console.confirm('Are you sure you want to deploy production?',
#                                default=False):
#             utils.abort('Production deployment aborted.')
#     # defaults rsync options:
#     # -pthrvz
#     # -p preserve permissions
#     # -t preserve times
#     # -h output numbers in a human-readable format
#     # -r recurse into directories
#     # -v increase verbosity
#     # -z compress file data during the transfer
#     extra_opts = '--omit-dir-times'
#     rsync_project(
#         env.root,
#         exclude=RSYNC_EXCLUDE,
#         delete=True,
#         extra_opts=extra_opts,
#     )
#     touch()


# def update_requirements():
#     """ update external dependencies on remote host """
#     require('code_root', provided_by=('staging', 'production'))
#     requirements = os.path.join(env.code_root, 'requirements')
#     with cd(requirements):
#         cmd = ['pip install']
#         cmd += ['-E %(virtualenv_root)s' % env]
#         cmd += ['--requirement %s' % os.path.join(requirements, 'apps.txt')]
#         run(' '.join(cmd))


# def touch():
#     """ touch wsgi file to trigger reload """
#     require('code_root', provided_by=('staging', 'production'))
#     apache_dir = os.path.join(env.code_root, 'apache')
#     with cd(apache_dir):
#         run('touch %s.wsgi' % env.environment)


# def update_apache_conf():
#     """ upload apache configuration to remote host """
#     require('root', provided_by=('staging', 'production'))
#     source = os.path.join('apache', '%(environment)s.conf' % env)
#     dest = os.path.join(env.home, 'apache.conf.d')
#     put(source, dest, mode=0755)
#     apache_reload()


# def configtest():    
#     """ test Apache configuration """
#     require('root', provided_by=('staging', 'production'))
#     run('apache2ctl configtest')


# def apache_reload():    
#     """ reload Apache on remote host """
#     require('root', provided_by=('staging', 'production'))
#     run('sudo /etc/init.d/apache2 reload')


# def apache_restart():    
#     """ restart Apache on remote host """
#     require('root', provided_by=('staging', 'production'))
#     run('sudo /etc/init.d/apache2 restart')


# def symlink_django():    
#     """ create symbolic link so Apache can serve django admin media """
#     require('root', provided_by=('staging', 'production'))
#     admin_media = os.path.join(env.virtualenv_root,
#                                'src/django/django/contrib/admin/media/')
#     media = os.path.join(env.code_root, 'media/admin')
#     if not files.exists(media):
#         run('ln -s %s %s' % (admin_media, media))


# def reset_local_media():
#     """ Reset local media from remote host """
#     require('root', provided_by=('staging', 'production'))
#     media = os.path.join(env.code_root, 'media', 'upload')
#     local('rsync -rvaz %s@%s:%s media/' % (env.user, env.hosts[0], media))


# # -------------------

# from fabric.api import *
# # Default release is 'current'
# env.release = 'current'

# def production():
#   """Production server settings"""
#   env.settings = 'production'
#   env.user = 'myproject'
#   env.path = '/home/%(user)s/sites/myproject' % env
#   env.hosts = ['mydomain.com']

# def setup():
#   """
#   Setup a fresh virtualenv and install everything we need so it's ready to deploy to
#   """
#   run('mkdir -p %(path)s; cd %(path)s; virtualenv --no-site-packages .; mkdir releases; mkdir shared;' % env)
#   clone_repo()
#   checkout_latest()
#   install_requirements()

# def deploy():
#   """Deploy the latest version of the site to the server and restart nginx"""
#   checkout_latest()
#   install_requirements()
#   symlink_current_release()
#   migrate()
#   restart_server()

# def clone_repo():
#   """Do initial clone of the git repo"""
#   run('cd %(path)s; git clone /home/%(user)s/git/repositories/myproject.git repository' % env)

# def checkout_latest():
#   """Pull the latest code into the git repo and copy to a timestamped release directory"""
#   import time
#   env.release = time.strftime('%Y%m%d%H%M%S')
#   run("cd %(path)s/repository; git pull origin master" % env)
#   run('cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*' % env)

# def install_requirements():
#   """Install the required packages using pip"""
#   run('cd %(path)s; %(path)s/bin/pip install -r ./releases/%(release)s/requirements.txt' % env)

# def symlink_current_release():
#   """Symlink our current release, uploads and settings file"""
#   with settings(warn_only=True):
#     run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)
#   run('cd %(path)s; ln -s %(release)s releases/current' % env)
#   """ production settings"""
#   run('cd %(path)s/releases/current/; cp settings_%(settings)s.py myproject/settings.py' % env)
#   with settings(warn_only=True):
#     run('rm %(path)s/shared/static' % env)
#     run('cd %(path)s/releases/current/static/; ln -s %(path)s/releases/%(release)s/static %(path)s/shared/static ' %env)

# def migrate():
#   """Run our migrations"""
#   run('cd %(path)s/releases/current; ../../bin/python manage.py syncdb --noinput --migrate' % env)

# def rollback():
#   """
#   Limited rollback capability. Simple loads the previously current
#   version of the code. Rolling back again will swap between the two.
#   """
#   run('cd %(path)s; mv releases/current releases/_previous;' % env)
#   run('cd %(path)s; mv releases/previous releases/current;' % env)
#   run('cd %(path)s; mv releases/_previous releases/previous;' %env)
#   restart_server()

# def restart_server():
#   """Restart the web server"""
#   with settings(warn_only=True):
#     sudo('kill -9 `cat /tmp/project-master_helpmamme.pid`')
#     sudo('rm /tmp/project-master_helpmamme.pid /tmp/uwsgi_helpmamme.sock')
#   run('cd %(path)s/releases/current; %(path)s/bin/uwsgi --ini %(path)s/releases/current/uwsgi.ini' % env)
#   sudo('/etc/init.d/nginx restart')

# def pack():
#     # create a new source distribution as tarball
#     local('python setup.py sdist --formats=gztar', capture=False)

# def deploy():
#     # figure out the release name and version
#     dist = local('python setup.py --fullname', capture=True).strip()
#     # upload the source tarball to the temporary folder on the server
#     put('dist/%s.tar.gz' % dist, '/tmp/yourapplication.tar.gz')
#     # create a place where we can unzip the tarball, then enter
#     # that directory and unzip it
#     run('mkdir /tmp/yourapplication')
#     with cd('/tmp/yourapplication'):
#         run('tar xzf /tmp/yourapplication.tar.gz')
#         # now setup the package with our virtual environment's
#         # python interpreter
#         run('/var/www/yourapplication/env/bin/python setup.py install')
#     # now that all is set up, delete the folder again
#     run('rm -rf /tmp/yourapplication /tmp/yourapplication.tar.gz')
#     # and finally touch the .wsgi file so that mod_wsgi triggers
#     # a reload of the application
#     run('touch /var/www/yourapplication.wsgi')