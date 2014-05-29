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
from tribus.config.pkg import (debian_system_dependencies,
                               debian_docker_dependencies, f_workenv_preseed,
                               f_sql_preseed, f_users_ldif,
                               f_python_dependencies)
from tribus.common.logger import get_logger
from tribus.config.waffle_cfg import SWITCHES_CONFIGURATION

logger = get_logger()


def development():
    # env.user = pwd.getpwuid(os.getuid()).pw_name
    # env.root = 'root'
    # env.environment = 'development'
    # env.hosts = ['localhost']
    # env.basedir = BASEDIR
    # env.virtualenv_dir = os.path.join(env.basedir, 'virtualenv')
    # env.virtualenv_cache = os.path.join(BASEDIR, 'virtualenv_cache')
    # env.virtualenv_site_dir = os.path.join(
    #     env.virtualenv_dir, 'lib', 'python%s' %
    #     sys.version[:3], 'site-packages')
    # env.virtualenv_args = ' '.join(['--clear', '--no-site-packages',
    #                                 '--setuptools', '--unzip-setuptools'])
    # env.virtualenv_activate = os.path.join(
    #     env.virtualenv_dir, 'bin', 'activate')
    # env.settings = 'tribus.config.web'
    # env.sudo_prompt = 'Executed'
    # env.f_python_dependencies = f_python_dependencies
    # env.xapian_destdir = os.path.join(
    #     env.virtualenv_dir, 'lib', 'python%s' %
    #     sys.version[:3], 'site-packages', 'xapian')
    # env.xapian_init = os.path.join(
    #     os.path.sep,
    #     'usr',
    #     'share',
    #     'pyshared',
    #     'xapian',
    #     '__init__.py')
    # env.xapian_so = os.path.join(
    #     os.path.sep,
    #     'usr',
    #     'lib',
    #     'python%s' % sys.version[:3],
    #     'dist-packages',
    #     'xapian',
    #     '_xapian.so')
    # env.reprepro_dir = os.path.join(BASEDIR, 'test_repo')
    # env.sample_packages_dir = os.path.join(BASEDIR, 'package_samples')
    # env.distributions_path = os.path.join(BASEDIR, 'tribus', 'config',
    #                                       'data', 'dists-template')
    # env.selected_packages = os.path.join(BASEDIR, 'tribus', 'config',
    #                                      'data', 'selected_packages.list')
    # env.f_workenv_preseed = f_workenv_preseed

    # System Config
    env.debian_system_dependencies = ' '.join(debian_system_dependencies)

    # Docker config
    env.debian_docker_dependencies = ' '.join(debian_docker_dependencies)
    env.docker_image = 'debian:latest'


def environment():
    configure_sudo(env.user)
    docker_pull_image(env.docker_image)
    docker_preseed_packages(env.docker_image)
    docker_install_packages(env.docker_image,
                            env.debian_docker_dependencies)
    docker_drop_mongo(env.docker_image)
    docker_configure_postgres(env.docker_image)
    # populate_ldap()
    # create_virtualenv()
    # include_xapian()
    # update_virtualenv()
    # configure_django()
    # deconfigure_sudo()


def configure_sudo(user):
    local('su root -c \
        "echo \'%s ALL= NOPASSWD: ALL\' > /etc/sudoers.d/tribus; \
        chmod 0440 /etc/sudoers.d/tribus"' % user, capture=False)


def docker_pull_image(image):
    local('sudo /bin/bash -c \
        "docker.io pull %s"' % image, capture=False)


def docker_preseed_packages(image):
    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'slapd slapd/purge_database boolean true\' \
        | debconf-set-selections"' % image, capture=False)

    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'slapd slapd/domain string tribus.org\' \
        | debconf-set-selections"' % image, capture=False)

    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'slapd shared/organization string tribus\' \
        | debconf-set-selections"' % image, capture=False)

    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'slapd slapd/password1 password tribus\' \
        | debconf-set-selections"' % image, capture=False)

    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'slapd slapd/password2 password tribus\' \
        | debconf-set-selections"' % image, capture=False)


def docker_install_packages(image, dependencies):
    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        aptitude install \
        -o Aptitude::CmdLine::Assume-Yes=true \
        -o Aptitude::CmdLine::Ignore-Trust-Violations=true \
        -o DPkg::Options::=--force-confmiss \
        -o DPkg::Options::=--force-confnew \
        -o DPkg::Options::=--force-overwrite \
        -o DPkg::Options::=--force-unsafe-io \
        %s"' % (image, dependencies), capture=False)


def docker_drop_mongo(image, db):
    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        mongo %s --eval \'db.dropDatabase()\'"' % (image, db), capture=False)


def docker_configure_postgres(image, pg_user, pg_passwd):
    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        echo \'%s:%s\' | chpasswd"' % (image, pg_user, pg_passwd),
        capture=False)

    local('sudo /bin/bash -c \
        "docker.io run -it \
        --env DEBIAN_FRONTEND=noninteractive \
        %s \
        sudo -i -u postgres /bin/sh -c \'psql -f /tmp/preseed-db.sql\'"' % (pg_user, pg_passwd), capture=False)

