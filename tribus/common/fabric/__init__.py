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

'''

tribus.common.fabric
====================


'''

import os
import pwd
from fabric.api import env
from tribus import BASEDIR
from tribus.config.base import CONFDIR
from tribus.config.ldap import (AUTH_LDAP_SERVER_URI,
                                AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
from tribus.config.pkg import (python_dependencies, debian_run_dependencies,
                               debian_build_dependencies, preseed_db,
                               preseed_debconf, preseed_env, preseed_ldap)
from tribus.common.logger import get_logger
from tribus.common.utils import get_path
from tribus.common.system import get_local_arch
from tribus.common.fabric.docker import (pull_debian_base_image,
                                         pull_tribus_base_image,
                                         generate_debian_base_image,
                                         generate_tribus_base_image,
                                         django_restartserver,
                                         django_runserver, django_stopserver,
                                         django_syncdb)

logger = get_logger()


def development():
    '''
    '''

    # Fabric environment configuration
    env.user = pwd.getpwuid(os.getuid()).pw_name
    env.root = 'root'
    env.basedir = BASEDIR
    env.hosts = ['localhost']
    env.environment = 'development'

    # Docker config
    env.arch = get_local_arch()
    env.docker_basedir = get_path([os.sep, 'media', 'tribus'])
    env.docker_maintainer = ('Luis Alejandro Martínez Faneyth '
                             '<luis@huntingbears.com.ve>')

    env.debian_base_image = 'luisalejandro/debian-%(arch)s:wheezy' % env
    env.tribus_base_image = 'luisalejandro/tribus-%(arch)s:wheezy' % env
    env.tribus_runtime_image = 'luisalejandro/tribus-run-%(arch)s:wheezy' % env
    env.tribus_runtime_container = 'tribus-run-container'

    if env.arch == 'i386':
        env.debian_base_image_id = '7902e3f5c3f8'
        env.tribus_base_image_id = '538beafc4d12'

    elif env.arch == 'amd64':
        env.debian_base_image_id = '7a4e3d67f626'
        env.tribus_base_image_id = '538beafc4d12'

    env.debian_base_image_script = get_path([BASEDIR, 'tribus',
                                             'data', 'scripts',
                                             'debian-base-image.sh'])
    env.tribus_base_image_dockerfile = get_path([CONFDIR, 'dockerfile',
                                                 ('tribus-base-image-%(arch)s.conf'
                                                  '' % env)])

    env.debian_run_dependencies = ' '.join(debian_run_dependencies)
    env.debian_build_dependencies = ' '.join(debian_build_dependencies)
    env.python_dependencies = ' '.join(python_dependencies)

    env.preseed_db = '\\\\\\n'.join(preseed_db)
    env.preseed_debconf = '\\\\\\n'.join(preseed_debconf)
    env.preseed_ldap = '\\\\\\n'.join(preseed_ldap)
    env.preseed_env = '\n'.join('ENV %s' % i.replace('=', ' ')
                                for i in preseed_env)

    env.ldap_passwd = AUTH_LDAP_BIND_PASSWORD
    env.ldap_writer = AUTH_LDAP_BIND_DN
    env.ldap_server = AUTH_LDAP_SERVER_URI
    env.ldap_args = ('-x '
                     '-w \\"%(ldap_passwd)s\\" '
                     '-D \\"%(ldap_writer)s\\" '
                     '-H \\"%(ldap_server)s\\"') % env

    mounts = ['%(basedir)s:%(docker_basedir)s:ro']
    env.mounts = ' --volume='.join('VOLUME %s' % i for i in mounts)


def generate_debian_base_image_i386():
    '''
    '''
    env.arch = 'i386'
    generate_debian_base_image(env)


def generate_debian_base_image_amd64():
    '''
    '''
    env.arch = 'amd64'
    generate_debian_base_image(env)


def generate_tribus_base_image_i386():
    '''
    '''
    env.arch = 'i386'
    env.debian_base_image = 'luisalejandro/debian-i386:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-i386:wheezy'
    env.tribus_base_image_dockerfile = get_path([CONFDIR, 'dockerfile',
                                                 'tribus-base-image-i386.conf'])
    generate_tribus_base_image(env)


def generate_tribus_base_image_amd64():
    '''
    '''
    env.arch = 'amd64'
    env.debian_base_image = 'luisalejandro/debian-amd64:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-amd64:wheezy'
    env.tribus_base_image_dockerfile = get_path([CONFDIR, 'dockerfile',
                                                 'tribus-base-image-amd64.conf'])
    generate_tribus_base_image(env)


def environment():
    '''
    '''
    pull_debian_base_image(env)
    pull_tribus_base_image(env)


def syncdb():
    '''
    '''
    django_syncdb(env)


def runserver():
    '''
    '''
    django_runserver(env)


def stopserver():
    '''
    '''
    django_stopserver(env)


def restartserver():
    '''
    '''
    django_restartserver(env)
