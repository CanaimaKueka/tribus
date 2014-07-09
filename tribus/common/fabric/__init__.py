#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

"""

This package contains remote execution scripts based on Fabric.

This package is intended to serve as an automation library. It is designed to
execute (local) operations on Tribus's development environment (Docker,
Vagrant, chroot, etc), and also on (remote) servers when deploying Charms.

"""

import os
import pwd
from fabric.api import env

from tribus import BASEDIR
from tribus.config.base import CONFDIR, AUTHOR, AUTHOR_EMAIL
from tribus.config.ldap import (AUTH_LDAP_SERVER_URI,
                                AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
from tribus.config.switches import SWITCHES_CONFIGURATION
from tribus.config.pkg import (python_dependencies, debian_run_dependencies,
                               debian_build_dependencies)
from tribus.common.utils import get_path
from tribus.common.system import get_local_arch
from tribus.common.fabric.docker import *
from tribus.common.fabric.django import *
from tribus.common.fabric.setup import *


# Fabric environment configuration
env.basedir = BASEDIR
env.host_string = '127.0.0.1'
env.user = str(pwd.getpwuid(os.getuid()).pw_name)
env.user_id = str(pwd.getpwuid(os.getuid()).pw_uid)
env.port = 22222
env.password = 'tribus'
env.warn_only = True
env.output_prefix = False

# Docker config
env.docker = 'docker.io'
env.arch = get_local_arch()
env.docker_maintainer = '%s <%s>' % (AUTHOR, AUTHOR_EMAIL)

env.debian_base_image = 'luisalejandro/debian-%(arch)s:wheezy' % env
env.tribus_base_image = 'luisalejandro/tribus-%(arch)s:wheezy' % env
env.tribus_runtime_image = 'luisalejandro/tribus-run-%(arch)s:wheezy' % env
env.tribus_runtime_container = 'tribus-run-container'

env.debian_base_image_script = get_path([BASEDIR, 'tribus',
                                         'data', 'scripts',
                                         'debian-base-image.sh'])
env.tribus_base_image_script = get_path([BASEDIR, 'tribus',
                                         'data', 'scripts',
                                         'tribus-base-image.sh'])
env.tribus_django_syncdb_script = get_path([BASEDIR, 'tribus',
                                            'data', 'scripts',
                                            'django-syncdb.sh'])
env.tribus_django_runserver_script = get_path([BASEDIR, 'tribus',
                                               'data', 'scripts',
                                               'django-runserver.sh'])
env.tribus_start_container_script = get_path([BASEDIR, 'tribus',
                                              'data', 'scripts',
                                              'start-container.sh'])

waffle_switches = SWITCHES_CONFIGURATION.keys()
mounts = ['%(basedir)s:%(basedir)s:rw' % env, '/tmp:/tmp:rw']
start_services = ['ssh', 'postgresql', 'slapd']
change_passwd = ['root:tribus', 'postgres:tribus', 'openldap:tribus']

env.mounts = ' '.join('--volume %s' % i for i in mounts)

env.fvars = {
    'BASEDIR': '%(basedir)s' % env,
    'PYTHONPATH': '%(basedir)s' % env,
    'DJANGO_SETTINGS_MODULE': 'tribus.config.web',
    'DEBIAN_FRONTEND': 'noninteractive',
    'PRESEED_DEBCONF': get_path([CONFDIR, 'data', 'preseed-debconf.conf']),
    'PRESEED_DB': get_path([CONFDIR, 'data', 'preseed-db.sql']),
    'PRESEED_LDAP': get_path([CONFDIR, 'data', 'preseed-ldap.ldif']),
    'PYTHON_DEPENDENCIES': ' '.join(python_dependencies),
    'DEBIAN_RUN_DEPENDENCIES':  ' '.join(debian_run_dependencies),
    'DEBIAN_BUILD_DEPENDENCIES': ' '.join(debian_build_dependencies),
    'LDAP_ARGS': ('-x -w %s -D %s -H %s' % (AUTH_LDAP_BIND_PASSWORD,
                                            AUTH_LDAP_BIND_DN,
                                            AUTH_LDAP_SERVER_URI)),
    'START_SERVICES': ' '.join(start_services),
    'CHANGE_PASSWD': ' '.join(change_passwd),
    'WAFFLE_SWITCHES': ' '.join(waffle_switches),
    'HOST_USER': env.user,
    'HOST_USER_ID': env.user_id
}

env.dvars = ' '.join('--env %s=\\"%s\\"' % (i, j)
                     for i, j in env.fvars.items())
