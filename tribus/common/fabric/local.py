#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import pwd
import sys
import site
import urllib
# import lsb_release
from fabric.api import local, env, settings, cd
from tribus import BASEDIR
from tribus.config.base import PACKAGECACHE
from tribus.config.ldap import (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BASE,
                                AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
from tribus.config.pkg import (debian_run_dependencies,
                               debian_build_dependencies,
                               debian_maint_dependencies, f_workenv_preseed,
                               f_sql_preseed, f_users_ldif,
                               f_python_dependencies)
from tribus.common.logger import get_logger
from tribus.config.waffle_cfg import SWITCHES_CONFIGURATION

logger = get_logger()


def development():
    env.user = pwd.getpwuid(os.getuid()).pw_name
    env.root = 'root'
    env.environment = 'development'
    env.hosts = ['localhost']
    env.basedir = BASEDIR
    env.virtualenv_dir = os.path.join(env.basedir, 'virtualenv')
    env.virtualenv_cache = os.path.join(BASEDIR, 'virtualenv_cache')
    env.virtualenv_site_dir = os.path.join(
        env.virtualenv_dir, 'lib', 'python%s' %
        sys.version[:3], 'site-packages')
    env.virtualenv_args = ' '.join(['--clear', '--no-site-packages',
                                    '--setuptools', '--unzip-setuptools'])
    env.virtualenv_activate = os.path.join(
        env.virtualenv_dir, 'bin', 'activate')
    env.settings = 'tribus.config.web'
    env.sudo_prompt = 'Executed'
    env.f_python_dependencies = f_python_dependencies
    env.xapian_destdir = os.path.join(
        env.virtualenv_dir, 'lib', 'python%s' %
        sys.version[:3], 'site-packages', 'xapian')
    env.xapian_init = os.path.join(
        os.path.sep,
        'usr',
        'share',
        'pyshared',
        'xapian',
        '__init__.py')
    env.xapian_so = os.path.join(
        os.path.sep,
        'usr',
        'lib',
        'python%s' % sys.version[:3],
        'dist-packages',
        'xapian',
        '_xapian.so')
    env.reprepro_dir = os.path.join(BASEDIR, 'test_repo')
    env.sample_packages_dir = os.path.join(BASEDIR, 'package_samples')
    env.distributions_path = os.path.join(BASEDIR, 'tribus', 'config',
                                          'data', 'dists-template')
    env.selected_packages = os.path.join(BASEDIR, 'tribus', 'config',
                                         'data', 'selected_packages.list')


def environment():
    configure_sudo()
    preseed_packages()
    install_packages(debian_build_dependencies)
    install_packages(debian_maint_dependencies)
    install_packages(debian_run_dependencies)
    drop_mongo()
    configure_postgres()
    populate_ldap()
    create_virtualenv()
    include_xapian()
    update_virtualenv()
    configure_django()
    deconfigure_sudo()

# REPOSITORY TASKS ------------------------------------------------------------


def install_repository():
    '''
    Crea un repositorio de paquetes y lo inicializa.
    '''

    py_activate_virtualenv()
    from tribus.common.reprepro import create_repository
    create_repository(env.reprepro_dir, env.distributions_path)


def select_sample_packages():
    '''
    Selecciona una muestra de paquetes.
    '''

    py_activate_virtualenv()
    from tribus.common.repository import init_sample_packages
    from tribus.config.pkgrecorder import CANAIMA_ROOT, SAMPLES_DIR
    init_sample_packages(CANAIMA_ROOT, SAMPLES_DIR)


def get_sample_packages():
    '''
    Descarga la muestra de paquetes
    '''

    py_activate_virtualenv()
    from tribus.common.repository import download_sample_packages
    from tribus.config.pkgrecorder import CANAIMA_ROOT, LOCAL_ROOT, SAMPLES_DIR
    download_sample_packages(CANAIMA_ROOT, SAMPLES_DIR)
    urllib.urlretrieve(os.path.join(CANAIMA_ROOT, "distributions"),
                       os.path.join(LOCAL_ROOT, "distributions"))
    
    
def get_selected():
    py_activate_virtualenv()
    from tribus.common.repository import get_selected_packages
    from tribus.config.pkgrecorder import CANAIMA_ROOT, SAMPLES_DIR
    get_selected_packages(CANAIMA_ROOT, SAMPLES_DIR, env.selected_packages)
    

def index_sample_packages():
    '''
    Indexa los paquetes descargados en el repositorio.
    '''

    from tribus.common.utils import list_items, find_files
    from tribus.common.reprepro import include_deb
    dirs = [os.path.dirname(f)
            for f in find_files(env.sample_packages_dir, 'list')]
    dists = filter(None, list_items(env.sample_packages_dir, dirs=True, files=False))
    with cd('%(reprepro_dir)s' % env):
        for directory in dirs:
            # No se me ocurre una mejor forma (dinamica) de hacer esto
            dist = [dist_name for dist_name in dists if dist_name in directory][0]
            results = [each for each in os.listdir(directory) if each.endswith('.deb')]
            if results:
                include_deb(env.reprepro_dir, dist, directory)
            else:
                logger.info('There are no packages in %s' % directory)


def index_selected():
    from tribus.common.utils import list_items, find_files
    from tribus.common.reprepro import include_deb
    from tribus.config.pkgrecorder import LOCAL_ROOT, SAMPLES_DIR
    for dist in list_items(SAMPLES_DIR, True, False):
        for comp in list_items(os.path.join(SAMPLES_DIR, dist), True, False):
            for sample in find_files(os.path.join(SAMPLES_DIR, dist, comp)):
                with cd('%(reprepro_dir)s' % env):
                    try:
                        include_deb(LOCAL_ROOT, dist, comp, sample)
                    except:
                        logger.info('There are no packages here!')


def wipe_repo():
    from tribus.common.reprepro import reset_repository
    reset_repository(env.reprepro_dir)


# -----------------------------------------------------------------------------

# TRIBUS DATABASE TASKS -------------------------------------------------------

def filldb_from_local():
    py_activate_virtualenv()
    from tribus.common.recorder import fill_db_from_cache, create_cache
    from tribus.config.pkgrecorder import LOCAL_ROOT
    create_cache(LOCAL_ROOT, PACKAGECACHE)
    fill_db_from_cache(PACKAGECACHE)


def create_cache_from_remote():
    py_activate_virtualenv()
    from tribus.common.recorder import create_cache
    from tribus.config.pkgrecorder import CANAIMA_ROOT
    create_cache(CANAIMA_ROOT, PACKAGECACHE)


def filldb_from_remote():
    py_activate_virtualenv()
    from tribus.common.recorder import fill_db_from_cache
    fill_db_from_cache(PACKAGECACHE)


def resetdb():
    configure_sudo()
    drop_mongo()
    configure_postgres()
    populate_ldap()
    configure_django()
    rebuild_index()
    register_existent_modules()
    deconfigure_sudo()

# -----------------------------------------------------------------------------
# WAFFLE SWITCHES

def register_existent_modules():
    '''
    Registra switches para los modulos existentes en tribus
    * Nube de aplicaciones
    * Perfiles de usuarios
    '''
    
    with cd('%(basedir)s' % env):
        for switch_name, switch_data in SWITCHES_CONFIGURATION.items():
            local('python manage.py switch %s %s --create' 
                  % (switch_name, switch_data[1]), capture=False)


# -----------------------------------------------------------------------------


def rebuild_index():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py rebuild_index \
--noinput --verbosity 3 --traceback' %
                env, capture=False)


def clean_tasks():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py celery purge' % 
                #'%(command)s celery purge -f -A tribus --app=tribus.config.celery_cfg' %
                env, capture=False)


def include_xapian():
    with settings(command='mkdir -p %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)

    with settings(command='ln -fs %(xapian_init)s %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)

    with settings(command='ln -fs %(xapian_so)s %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)


def configure_sudo():
    with settings(command='su root -c "DEBIAN_FRONTEND=noninteractive \
aptitude install --assume-yes --allow-untrusted \
-o DPkg::Options::=--force-confmiss -o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite sudo; mkdir -p /etc/sudoers.d/; \
echo \'%(user)s ALL= NOPASSWD: ALL\' > /etc/sudoers.d/tribus; \
chmod 0440 /etc/sudoers.d/tribus"' % env):
        local('%(command)s' % env, capture=False)


def deconfigure_sudo():
    with settings(command='sudo /bin/bash -c \
                  "rm -rf /etc/sudoers.d/tribus"' % env):
        local('%(command)s' % env, capture=False)


def preseed_packages():
    with settings(command='sudo /bin/bash -c \
"debconf-set-selections %s"' % f_workenv_preseed):
        local('%(command)s' % env, capture=False)


def install_packages(dependencies):
    with settings(command='sudo /bin/bash -c "DEBIAN_FRONTEND=noninteractive \
aptitude install --assume-yes --allow-untrusted \
-o DPkg::Options::=--force-confmiss -o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite %s"' % ' '.join(dependencies)):
        local('%(command)s' % env, capture=False)


def configure_postgres():
    with settings(command='sudo /bin/bash -c \
"echo \'postgres:tribus\' | chpasswd"'):
        local('%(command)s' % env, capture=False)

    with settings(command='cp %s /tmp/' % f_sql_preseed):
        local('%(command)s' % env, capture=False)

    with settings(command='sudo /bin/bash -c \
"sudo -i -u postgres /bin/sh -c \'psql -f /tmp/preseed-db.sql\'"'):
        local('%(command)s' % env, capture=False)


def populate_ldap():
    env.ldap_passwd = AUTH_LDAP_BIND_PASSWORD
    env.ldap_writer = AUTH_LDAP_BIND_DN
    env.ldap_server = AUTH_LDAP_SERVER_URI
    env.ldap_base = AUTH_LDAP_BASE
    env.users_ldif = f_users_ldif
    with settings(command='ldapsearch -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -H "%(ldap_server)s" -b "%(ldap_base)s" \
-LLL "(uid=*)" | perl -p00e \'s/\\r?\\n //g\' | grep "dn: "| \
sed \'s/dn: //g\' | sed \'s/ /_@_/g\'' % env):
        ldap_entries = local('%(command)s' % env, capture=True)

    for ldap_entry in ldap_entries.split():
        env.ldap_entry = ldap_entry
        with settings(command='ldapdelete -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -H "%(ldap_server)s" "%(ldap_entry)s"' % env):
            local('%(command)s' % env, capture=False)

    with settings(command='ldapadd -x -w "%(ldap_passwd)s" \
-D "%(ldap_writer)s" -H "%(ldap_server)s" -f "%(users_ldif)s"' % env):
        local('%(command)s' % env, capture=False)


def create_virtualenv():
    with cd('%(basedir)s' % env):
        with settings(command='virtualenv \
%(virtualenv_args)s %(virtualenv_dir)s' % env):
            local('%(command)s' % env, capture=False)


def update_virtualenv():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s pip install \
--download-cache=%(virtualenv_cache)s \
--requirement=%(f_python_dependencies)s' %
                env, capture=False)

        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s nodeenv -p' % env, capture=False)

        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s npm install -g' % env, capture=False)


def py_activate_virtualenv():
    os.environ['PATH'] = os.path.join(
        env.virtualenv_dir,
        'bin') + os.pathsep + os.environ['PATH']
    site.addsitedir(env.virtualenv_site_dir)
    sys.prefix = env.virtualenv_dir
    sys.path.insert(0, env.virtualenv_dir)
    sys.path.insert(0, env.virtualenv_site_dir)


def configure_django():
    syncdb_django()
    createsuperuser_django()


def drop_mongo():
    with settings(command='mongo tribus --eval \'db.dropDatabase()\'' % env):
        local('%(command)s' % env, capture=False)


def createsuperuser_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py createsuperuser --noinput \
--username tribus --email tribus@localhost.com --verbosity 3 --traceback' %
                env, capture=False)
    py_activate_virtualenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
    from django.contrib.auth.models import User
    from tribus.web.registration.ldap.utils import create_ldap_user
    u = User.objects.get(username__exact='tribus')
    u.set_password('tribus')
    u.save()
    create_ldap_user(u)


def syncdb_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py syncdb \
--noinput --verbosity 3 --traceback' %
                env, capture=False)
            local(
                '%(command)s python manage.py migrate \
--verbosity 3 --traceback' %
                env, capture=False)


def runserver_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py runserver \
--verbosity 3 --traceback' %
                env, capture=False)


def runcelery_daemon():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py celeryd -c 1 --beat -l INFO' %
                #'%(command)s celery worker -A tribus --app=tribus.config.celery_cfg -c 1 -l INFO' %
                env, capture=False)


#def runcelery_worker():
#    with cd('%(basedir)s' % env):
#        with settings(command='. %(virtualenv_activate)s;' % env):
#            local(
#                '%(command)s python manage.py celery beat -s celerybeat-schedule' %
#                #'%(command)s celery worker -A tribus --app=tribus.config.celery_cfg -B -c 1 -l INFO' %
#                env, capture=False)


def shell_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python manage.py shell \
--verbosity 3 --traceback' %
                env, capture=False)


def update_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py update_catalog' %
                env, capture=False)


def extract_messages():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py extract_messages' %
                env, capture=False)


def compile_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py compile_catalog' %
                env, capture=False)


def init_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py init_catalog' %
                env, capture=False)


def tx_pull():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s tx pull -a --skip' % env, capture=False)


def tx_push():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s tx push -s -t --skip --no-interactive' %
                env, capture=False)


def build_sphinx():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py build_sphinx' %
                env, capture=False)


def build_css():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py build_css' % env, capture=False)


def build_js():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py build_js' % env, capture=False)


def build_man():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py build_man' % env, capture=False)


def build():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py build' % env, capture=False)


def clean_css():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean_css' % env, capture=False)


def clean_js():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean_js' % env, capture=False)


def clean_sphinx():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py clean_sphinx' %
                env, capture=False)


def clean_mo():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean_mo' % env, capture=False)


def clean_man():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean_man' % env, capture=False)


def clean_dist():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py clean_dist' %
                env, capture=False)


def clean_pyc():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean_pyc' % env, capture=False)


def clean():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py clean' % env, capture=False)


def sdist():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py sdist' % env, capture=False)


def bdist():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py bdist' % env, capture=False)


def install():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py install' % env, capture=False)


def test():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py test --verbose' %
                env, capture=False)


def report_setup_data():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local(
                '%(command)s python setup.py report_setup_data' %
                env, capture=False)
