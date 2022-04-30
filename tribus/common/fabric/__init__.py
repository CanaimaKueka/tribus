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

import sys
from fabric.api import task

from tribus.config.base import CONTAINERS
from tribus.common.logger import get_logger
from tribus.common.fabric.map import FABRIC_FUNCTION_MAP

log = get_logger()

if CONTAINERS in FABRIC_FUNCTION_MAP:

    log.info('Using "%s" as container backend.' % CONTAINERS)
    env = FABRIC_FUNCTION_MAP[CONTAINERS]['enable_environment']()

else:
    log.info('Container backend "%s" not supported.' % CONTAINERS)
    sys.exit(1)


@task
def generate_debian_base_image_i386():
    """
    """
    env.arch = 'i386'
    FABRIC_FUNCTION_MAP[CONTAINERS]['generate_debian_base_image']()


@task
def generate_debian_base_image_amd64():
    """
    """
    env.arch = 'amd64'
    FABRIC_FUNCTION_MAP[CONTAINERS]['generate_debian_base_image']()


@task
def generate_tribus_base_image_i386():
    """
    """
    env.arch = 'i386'
    env.debian_base_image = 'luisalejandro/debian-i386'
    env.tribus_base_image = 'luisalejandro/tribus-i386'
    FABRIC_FUNCTION_MAP[CONTAINERS]['generate_tribus_base_image']()


@task
def generate_tribus_base_image_amd64():
    """
    """
    env.arch = 'amd64'
    env.debian_base_image = 'luisalejandro/debian-amd64'
    env.tribus_base_image = 'luisalejandro/tribus-amd64'
    FABRIC_FUNCTION_MAP[CONTAINERS]['generate_tribus_base_image']()


@task
def kill_all_containers():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['kill_all_containers']()


@task
def kill_all_images():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['kill_all_images']()


@task
def kill_tribus_images():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['kill_tribus_images']()


@task
def environment():
    """
    Reproduce the Tribus developer environment.

    This function takes care of downloading and installing the software that
    is needed to develop and maintain Tribus.

    .. versionadded:: 0.2
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['pull_debian_base_image']()
    FABRIC_FUNCTION_MAP[CONTAINERS]['pull_tribus_base_image']()


@task
def stop():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['stop_container']()


@task
def login():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['login_container']()


@task
def reset():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['reset_container']()


@task
def update():
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['update_container']()


@task
def django(command):
    """
    """

    FABRIC_FUNCTION_MAP[CONTAINERS]['check_container']()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):

        if command == 'syncdb':

            run('bash %(tribus_django_syncdb_script)s' % env)

        elif command == 'runserver':

            run('bash %(tribus_django_runserver_script)s' % env)

        elif command == 'shell':

            log.info('Opening a django shell inside the runtime container ...')
            log.info('(When you are done, press CTRL+D to get out).')

            run('python manage.py shell')

        else:

            run('python manage.py %s' % command)


@task
def setuptools(command):
    """
    """
    FABRIC_FUNCTION_MAP[CONTAINERS]['check_container']()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):

        run('python setup.py %s' % command)


@task
def tx(command):
    """
    """

    FABRIC_FUNCTION_MAP[CONTAINERS]['check_container']()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):

        if command == 'pull':

            run('tx pull -a --skip')

        elif command == 'push':

            run('tx push -s -t --skip --no-interactive')
