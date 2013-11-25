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
import lsb_release
from fabric.api import *
from tribus import BASEDIR
from tribus.config.ldap import (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BASE, AUTH_LDAP_BIND_DN,
                               AUTH_LDAP_BIND_PASSWORD)
from tribus.config.pkg import (debian_run_dependencies, debian_build_dependencies,
                              debian_maint_dependencies, f_workenv_preseed, f_sql_preseed,
                              f_users_ldif, f_python_dependencies)

def development():
    env.user = pwd.getpwuid(os.getuid()).pw_name
    env.root = 'root'
    env.environment = 'development'
    env.hosts = ['localhost']
    env.basedir = BASEDIR
    env.virtualenv_dir = os.path.join(env.basedir, 'virtualenv')
    env.virtualenv_args = ' '.join(['--clear', '--no-site-packages', '--setuptools'])
    env.virtualenv_activate = os.path.join(env.virtualenv_dir, 'bin', 'activate')
    env.settings = 'tribus.config.web'
    env.sudo_prompt = 'Executed'
    env.f_python_dependencies = f_python_dependencies
    env.xapian_destdir = os.path.join(env.virtualenv_dir, 'lib', 'python%s' % sys.version[:3], 'site-packages', 'xapian')
    env.xapian_init = os.path.join(os.path.sep, 'usr', 'share', 'pyshared', 'xapian', '__init__.py')
    env.xapian_so = os.path.join(os.path.sep, 'usr', 'lib', 'python%s' % sys.version[:3], 'dist-packages', 'xapian', '_xapian.so')
    env.reprepro_dir = os.path.join(BASEDIR, 'test_repo')
    env.reprepro_conf_dir = os.path.join(BASEDIR, 'test_repo', 'conf')
    env.distributions_dir = os.path.join(BASEDIR, 'tribus', 'config' ,'data')
    env.sample_packages_dir = os.path.join(BASEDIR, 'package_samples', 'packages')
    
    
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

# 1) Crear repositorio e inicializarlo

def install_repository():
    with settings(command='rm -rf %(reprepro_dir)s' % env):
        local('%(command)s' % env, capture=False)
    
    with settings(command='mkdir -p %(reprepro_conf_dir)s' % env):
        local('%(command)s' % env, capture=False)
    
    with settings(command='cp %(distributions_dir)s/dists-template  %(reprepro_conf_dir)s/distributions' % env):
        local('%(command)s' % env, capture=False)
    
    with lcd('%(reprepro_dir)s' % env):
        with settings(command='reprepro -VVV export'):
            local('%(command)s' % env, capture=False)
    
    
# 2) Seleccionar muestra de paquetes

def select_sample_packages():
    py_activate_virtualenv()
    from tribus.common.recorder import init_sample_packages
    init_sample_packages() 
    
# 3) Descargar muestra de paquetes

def get_sample_packages():
    py_activate_virtualenv()
    from tribus.common.recorder import download_sample_packages
    download_sample_packages()
    
# 4) Indexar los paquetes descargados en el repositorio
    
def index_sample_packages():
    from tribus.common.utils import find_dirs, list_dirs
    dirs = filter(lambda dir: "binary" in dir, find_dirs(env.sample_packages_dir))
    dists = filter(None, list_dirs(env.sample_packages_dir))
    with lcd('%(reprepro_dir)s' % env):
        for d in dirs:      
            # No se me ocurre una mejor forma (dinamica) de hacer esto      
            dist = [dist_name for dist_name in dists if dist_name in d][0]
            try:
                with settings(command='reprepro includedeb %s %s/*.deb' % (dist, d)):
                    local('%(command)s' % env, capture=False)
            except:
                print "No hay paquetes en el directorio %s" % d
    
    with settings(command='cp %(distributions_dir)s/distributions %(reprepro_dir)s' % env):
        local('%(command)s' % env, capture=False)
    
# -----------------------------------------------------------------------------

# TRIBUS DATABASE TASKS -------------------------------------------------------

def filldb_from_local():
    py_activate_virtualenv()
    from tribus.common.recorder import create_cache_dirs, fill_db_from_cache
    from tribus.config.pkgrecorder import LOCAL_ROOT
    create_cache_dirs(LOCAL_ROOT)
    fill_db_from_cache(LOCAL_ROOT)
    rebuild_index()
    
def filldb_from_remote():
    py_activate_virtualenv()
    from tribus.common.recorder import create_cache_dirs, fill_db_from_cache
    from tribus.config.pkgrecorder import CANAIMA_ROOT
    create_cache_dirs(CANAIMA_ROOT)
    fill_db_from_cache(CANAIMA_ROOT)
    rebuild_index()
    
def resetdb():
    configure_sudo()
    drop_mongo()
    configure_postgres()
    configure_django()
    deconfigure_sudo()

# -----------------------------------------------------------------------------

def rebuild_index():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py rebuild_index --noinput --verbosity 3 --traceback' % env, capture=False)

def include_xapian():
    with settings(command='mkdir -p %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)

    with settings(command='ln -fs %(xapian_init)s %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)

    with settings(command='ln -fs %(xapian_so)s %(xapian_destdir)s' % env):
        local('%(command)s' % env, capture=False)

def configure_sudo():
    with settings(command='su root -c "echo \'%(user)s ALL= NOPASSWD: ALL\' > /etc/sudoers.d/tribus; chmod 0440 /etc/sudoers.d/tribus"' % env):
        local('%(command)s' % env, capture=False)


def deconfigure_sudo():
    with settings(command='sudo /bin/bash -c "rm -rf /etc/sudoers.d/tribus"' % env):
        local('%(command)s' % env, capture=False)


def preseed_packages():
    with settings(command='sudo /bin/bash -c "debconf-set-selections %s"' % f_workenv_preseed):
        local('%(command)s' % env, capture=False)


def install_packages(dependencies):
    with settings(command='sudo /bin/bash -c "DEBIAN_FRONTEND=noninteractive \
aptitude install --assume-yes --allow-untrusted \
-o DPkg::Options::=--force-confmiss \
-o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite \
%s"' % ' '.join(dependencies)):
        local('%(command)s' % env, capture=False)


def configure_postgres():
    with settings(command='sudo /bin/bash -c "echo \'postgres:tribus\' | chpasswd"'):
        local('%(command)s' % env, capture=False)

    with settings(command='cp %s /tmp/' % f_sql_preseed):
        local('%(command)s' % env, capture=False)

    with settings(command='sudo /bin/bash -c "sudo -i -u postgres /bin/sh -c \'psql -f /tmp/preseed-db.sql\'"'):
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
        with settings(command='virtualenv %(virtualenv_args)s %(virtualenv_dir)s' % env):
            local('%(command)s' % env, capture=False)


def update_virtualenv():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s pip install -r %(f_python_dependencies)s' % env, capture=False)


def py_activate_virtualenv():
    os.environ['PATH'] = os.path.join(env.virtualenv_dir, 'bin') + os.pathsep + os.environ['PATH']
    site.addsitedir(os.path.join(env.virtualenv_dir, 'lib', 'python%s' % sys.version[:3], 'site-packages'))
    sys.prefix = env.virtualenv_dir
    sys.path.insert(0, env.virtualenv_dir)


def configure_django():
    syncdb_django()
    createsuperuser_django()

def drop_mongo():
    with settings(command='mongo tribus --eval \'db.dropDatabase()\'' % env):
        local('%(command)s' % env, capture=False)


def createsuperuser_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py createsuperuser --noinput --username admin --email admin@localhost.com --verbosity 3 --traceback' % env, capture=False)

    py_activate_virtualenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")
    from django.contrib.auth.models import User

    u = User.objects.get(username__exact='admin')
    u.set_password('tribus')
    u.save()


def syncdb_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py syncdb --noinput --verbosity 3 --traceback' % env, capture=False)
            local('%(command)s python manage.py migrate --verbosity 3 --traceback' % env, capture=False)


def runserver_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py runserver --verbosity 3 --traceback' % env, capture=False)
            
            
def runcelery_daemon():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py celeryd -l INFO' % env, capture=False)
            
            
def runcelery_worker():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py celery beat -s celerybeat-schedule ' % env, capture=False)
            
            
def shell_django():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python manage.py shell --verbosity 3 --traceback' % env, capture=False)


def update_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py update_catalog' % env, capture=False)


def extract_messages():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py extract_messages' % env, capture=False)


def compile_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py compile_catalog' % env, capture=False)


def init_catalog():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py init_catalog' % env, capture=False)


def tx_pull():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s tx pull -a --skip' % env, capture=False)


def tx_push():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s tx push -s -t --skip --no-interactive' % env, capture=False)


def build_sphinx():
    with cd('%(basedir)s' % env):
        with settings(command='. %(virtualenv_activate)s;' % env):
            local('%(command)s python setup.py build_sphinx' % env, capture=False)


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
            local('%(command)s python setup.py clean_sphinx' % env, capture=False)


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
            local('%(command)s python setup.py clean_dist' % env, capture=False)


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
