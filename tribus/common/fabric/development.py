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
from tribus.config.ldap import (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BASE,
                                AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
from tribus.config.pkg import (debian_dependencies, python_dependencies,
                               preseed_db, preseed_debconf, preseed_env,
                               preseed_ldap)
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
    env.arch = get_local_arch()
    env.docker_basedir = get_path([os.sep, 'media', 'tribus'])
    env.docker_from = 'luisalejandro/debian-%(arch)s:wheezy' % env

    if env.arch == 'i386':
        env.docker_image_id = '538beafc4d12'

    elif env.arch == 'amd64':
        env.docker_image_id = '538beafc4d12'

    env.debian_dependencies = ' '.join(debian_dependencies)
    env.python_dependencies = ' '.join(python_dependencies)

    env.preseed_db = '; '.join(preseed_db)
    env.preseed_debconf = '\n'.join(preseed_debconf)
    env.preseed_ldap = '\n'.join(preseed_ldap)
    env.preseed_env = '\n'.join('ENV %s' % i.replace('=', ' ')
                                for i in preseed_env)

    env.ldap_passwd = AUTH_LDAP_BIND_PASSWORD
    env.ldap_writer = AUTH_LDAP_BIND_DN
    env.ldap_server = AUTH_LDAP_SERVER_URI

    mount_volumes = ['/var/cache/apt-cacher-ng:/var/cache/apt-cacher-ng:rw',
                     '/var/cache/apt:/var/cache/apt:rw',
                     '%(basedir)s:%(docker_basedir)s:rw']
    env.mount_volumes = '\n'.join('VOLUME %s' % i
                                  for i in mount_volumes)


def local_configure_sudo():
    run(('su root -c '
         '"echo \'%(user)s ALL= NOPASSWD: ALL\' '
         '> /etc/sudoers.d/tmp"') % env, capture=False)


def local_deconfigure_sudo():
    run(('su root -c "rm -rf /etc/sudoers.d/tmp"') % env, capture=False)


def generate_dockerfile():
    run(('echo "'
         'FROM %(docker_base_image)s\n'
         'MAINTAINER Luis A. Martínez F. <luis@huntingbears.com.ve>\n'
         '%(docker_preseed_env)s\n'
         '%(mount_volumes)s\n'
         'WORKDIR %(docker_basedir)s\n'
         'RUN echo $\'%(preseed_debconf)s\' | debconf-set-selections\n'
         'RUN apt-get update\n'
         'RUN apt-get install %(apt_args)s %(debian_dependencies)s\n'
         'RUN echo "postgres:tribus" | chpasswd\n'
         'RUN sudo -i -u postgres /bin/sh -c "psql -c \'%(preseed_db)s\'"\n'
         'RUN echo $\'%(preseed_ldap)s\' | '
         'ldapadd -x -w "%(ldap_passwd)s" '
         '-D "%(ldap_writer)s" -H "%(ldap_server)s"\n'
         'RUN pip install %(python_dependencies)s\n'
         'RUN python manage.py syncdb'
         'RUN python manage.py migrate'
         '" > %(dockerfile_path)s') % env, capture=False)


# def generate_docker_image():

#     pass


# def pull_docker_image():

#     containers = run(('sudo /bin/bash -c "docker.io ps -aq"'), capture=True)

#     if containers:
#         run(('sudo /bin/bash -c '
#              '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
#             capture=False)


# def docker_pull_base_image():

#     containers = run(('sudo /bin/bash -c "docker.io ps -aq"'), capture=True)

#     if containers:
#         run(('sudo /bin/bash -c '
#                '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
#               capture=False)

#     if env.docker_base_image_id not in run(('sudo /bin/bash -c '
#                                               '"docker.io images -aq"'),
#                                              capture=True):
#         run(('sudo /bin/bash -c '
#                '"docker.io pull %(docker_base_image)s"') % env, capture=False)

#     run(('sudo /bin/bash -c '
#            '"docker.io run -it '
#            '--name %(docker_container)s '
#            '%(docker_env_args)s '
#            '%(docker_env_vol)s '
#            '%(docker_base_image)s '
#            'apt-get install '
#            '%(apt_args)s '
#            '%(docker_env_packages)s"') % env, capture=False)

#     run(('sudo /bin/bash -c '
#            '"docker.io commit '
#            '%(docker_container)s %(docker_env_image)s"') % env, capture=False)

#     run(('sudo /bin/bash -c '
#           '"docker.io rm -fv %(docker_container)s"') % env, capture=False)
