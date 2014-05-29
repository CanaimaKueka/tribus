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
from tribus.config.ldap import (
    AUTH_LDAP_SERVER_URI, AUTH_LDAP_BASE, AUTH_LDAP_BIND_DN,
    AUTH_LDAP_BIND_PASSWORD)
from tribus.config.pkg import (
    debian_run_dependencies, debian_build_dependencies,
    debian_maint_dependencies, f_workenv_preseed, f_sql_preseed,
    f_users_ldif, f_python_dependencies)
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
    env.f_workenv_preseed = f_workenv_preseed
    env.debian_build_dependencies = ' '.join(debian_build_dependencies)
    env.debian_maint_dependencies = ' '.join(debian_maint_dependencies)
    env.debian_run_dependencies = ' '.join(debian_run_dependencies)

def environment():
    configure_sudo(env.user)
    preseed_packages(env.f_workenv_preseed)
    install_packages(env.debian_build_dependencies)
    install_packages(env.debian_maint_dependencies)
    install_packages(env.debian_run_dependencies)
    drop_mongo()
    configure_postgres()
    populate_ldap()
    create_virtualenv()
    include_xapian()
    update_virtualenv()
    configure_django()
    deconfigure_sudo()


def configure_sudo(user):
    local('su root -c \
        "echo \'%s ALL= NOPASSWD: ALL\' > /etc/sudoers.d/tribus; \
        chmod 0440 /etc/sudoers.d/tribus"' % user, capture=False)


def preseed_packages(preseed_file):
    local('sudo /bin/bash -c \
        "debconf-set-selections %s"' % preseed_file, capture=False)


def install_packages(dependencies):
    with settings(command='' % ' '.join(dependencies)):
        local('sudo /bin/bash -c "DEBIAN_FRONTEND=noninteractive \
aptitude install --assume-yes --allow-untrusted \
-o DPkg::Options::=--force-confmiss \
-o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite \
%s"' % env, capture=False)