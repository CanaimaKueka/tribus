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
from fabric.api import run, env
from tribus import BASEDIR
from tribus.config.pkg import (debian_docker_dependencies,
                               f_preseed_debconf)
from tribus.common.logger import get_logger
from tribus.common.utils import get_path
from tribus.common.system import get_local_arch

logger = get_logger()


def development():

    # Fabric environment configuration
    env.basedir = BASEDIR
    env.hosts = ['localhost']
    env.environment = 'development'

    # Docker config
    env.docker_arch = get_local_arch()
    env.docker_basedir = get_path([os.sep, 'media', 'tribus'])
    env.docker_preseed_debconf_file = env.docker_basedir + \
        f_preseed_debconf.replace(env.basedir, '')
    env.debian_docker_dependencies = ' '.join(debian_docker_dependencies)
    env.docker_container = 'container'
    env.docker_env_image = 'environment'
    env.docker_env_vol = ('--volume /var/cache/apt-cacher-ng:'
                          '/var/cache/apt-cacher-ng:rw '
                          '--volume /var/cache/apt:/var/cache/apt:rw '
                          '--volume %(basedir)s:%(docker_basedir)s:rw') % env
    env.docker_env_args = ('--env DEBIAN_FRONTEND=noninteractive')
    env.docker_base_image = 'luisalejandro/debian-%(docker_arch)s:wheezy' % env

    if env.docker_arch == 'i386':
        env.docker_base_image_id = '538beafc4d12'

    elif env.docker_arch == 'amd64':
        env.docker_base_image_id = '538beafc4d12'


def environment():
    local_configure_sudo()
    docker_pull_base_image()
    docker_preseed_packages()
    # docker_install_packages(env.docker_env_image,
    #                         env.debian_docker_dependencies)
    # docker_drop_mongo(env.docker_image)
    # docker_configure_postgres(env.docker_image)
    # populate_ldap()
    # create_virtualenv()
    # include_xapian()
    # update_virtualenv()
    # configure_django()
    # deconfigure_sudo()


def local_configure_sudo():
    run(('su root -c '
         '"echo \'%(user)s ALL= NOPASSWD: ALL\' '
         '> /etc/sudoers.d/tribus"') % env, capture=False)


def docker_pull_base_image():

    containers = run(('sudo /bin/bash -c "docker.io ps -aq"'), capture=True)

    if containers:
        run(('sudo /bin/bash -c '
               '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
              capture=False)

    if env.docker_base_image_id not in run(('sudo /bin/bash -c '
                                              '"docker.io images -aq"'),
                                             capture=True):
        run(('sudo /bin/bash -c '
               '"docker.io pull %(docker_base_image)s"') % env, capture=False)

    run(('sudo /bin/bash -c '
           '"docker.io run -it '
           '--name %(docker_container)s '
           '%(docker_env_args)s '
           '%(docker_env_vol)s '
           '%(docker_base_image)s '
           'apt-get install '
           '%(apt_args)s '
           '%(docker_env_packages)s"') % env, capture=False)

    run(('sudo /bin/bash -c '
           '"docker.io commit '
           '%(docker_container)s %(docker_env_image)s"') % env, capture=False)

    run(('sudo /bin/bash -c '
          '"docker.io rm -fv %(docker_container)s"') % env, capture=False)


def docker_preseed_packages():
    run(('sudo /bin/bash -c '
           '"docker.io run -it '
           '--name %(docker_container)s '
           '%(docker_env_args)s '
           '%(docker_env_vol)s '
           '%(docker_base_image)s '
           'ls /media/tribus"') % env, capture=False)

    run(('sudo /bin/bash -c '
           '"docker.io commit '
           '%(docker_container)s %(docker_env_image)s"') % env, capture=False)

    run(('sudo /bin/bash -c '
          '"docker.io rm -fv %(docker_container)s"') % env, capture=False)

    # run(('sudo /bin/bash -c '
    #       '"docker.io run -it '
    #       '--env DEBIAN_FRONTEND=noninteractive '
    #       '%s '
    #       'echo \'slapd slapd/purge_database boolean true\' '
    #       '| debconf-set-selections"') % image, capture=False)

    # run(('sudo /bin/bash -c '
    #       '"docker.io run -it '
    #       '--env DEBIAN_FRONTEND=noninteractive '
    #       '%s '
    #       'echo \'slapd slapd/domain string tribus.org\' '
    #       '| debconf-set-selections"') % image, capture=False)

    # run(('sudo /bin/bash -c '
    #       '"docker.io run -it '
    #       '--env DEBIAN_FRONTEND=noninteractive '
    #       '%s '
    #       'echo \'slapd shared/organization string tribus\' '
    #       '| debconf-set-selections"') % image, capture=False)

    # run(('sudo /bin/bash -c '
    #       '"docker.io run -it '
    #       '--env DEBIAN_FRONTEND=noninteractive '
    #       '%s '
    #       'echo \'slapd slapd/password1 password tribus\' '
    #       '| debconf-set-selections"') % image, capture=False)

    # run(('sudo /bin/bash -c '
    #       '"docker.io run -it '
    #       '--env DEBIAN_FRONTEND=noninteractive '
    #       '%s '
    #       'echo \'slapd slapd/password2 password tribus\' '
    #       '| debconf-set-selections"') % image, capture=False)


def docker_install_packages(image, dependencies):
    run(('sudo /bin/bash -c '
          '"docker.io run -it '
          '--env DEBIAN_FRONTEND=noninteractive '
          '%s '
          'aptitude install '
          '-o Aptitude::CmdLine::Assume-Yes=true '
          '-o Aptitude::CmdLine::Ignore-Trust-Violations=true '
          '-o DPkg::Options::=--force-confmiss '
          '-o DPkg::Options::=--force-confnew '
          '-o DPkg::Options::=--force-overwrite '
          '-o DPkg::Options::=--force-unsafe-io '
          '%s"') % (image, dependencies), capture=False)


# def docker_drop_mongo(image, db):
#     run(('sudo /bin/bash -c '
#           '"docker.io run -it '
#           '--env DEBIAN_FRONTEND=noninteractive '
#           '%s '
#           'mongo %s --eval \'db.dropDatabase()\'"') % (image, db), capture=False)


# def docker_configure_postgres(image, pg_user, pg_passwd):
#     run(('sudo /bin/bash -c '
#           '"docker.io run -it '
#           '--env DEBIAN_FRONTEND=noninteractive '
#           '%s '
#           'echo \'%s:%s\' | chpasswd"') % (image, pg_user, pg_passwd),
#           capture=False)

#     run(('sudo /bin/bash -c '
#           '"docker.io run -it '
#           '--env DEBIAN_FRONTEND=noninteractive '
#           '%s '
#           'sudo -i -u postgres /bin/sh -c '
#           '\'psql -f /tmp/preseed-db.sql\'"') % (pg_user, pg_passwd), capture=False)


# DROP DATABASE IF EXISTS test_tribus;
# DROP DATABASE IF EXISTS tribus;
# DROP ROLE IF EXISTS tribus;
# CREATE ROLE tribus PASSWORD 'md51a2031d64cd6f9dd4944bac9e73f52dd' NOSUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
# CREATE DATABASE tribus OWNER tribus;
# GRANT ALL PRIVILEGES ON DATABASE tribus to tribus;
