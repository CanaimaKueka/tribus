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

import os
from contextlib import nested
from fabric.api import env, local, lcd, shell_env, hide

from tribus.common.logger import get_logger

log = get_logger()


def vagrant_generate_debian_base_image():
    """
    Generate a Debian base (Vagrant) image.

    This function generates a minimal Debian (stable) vagrant image using
    veewee.

    .. versionadded:: 0.2
    """
    vagrant_stop_container()

    with nested(lcd(env.veeweedir), shell_env(PATH=os.getenv('PATH'))):

        log.info('Generating a fresh Debian image for Vagrant ...')

        local(('veewee vbox build debian-%(arch)s '
               '--force --nogui --auto') % env, capture=False)
        local(('veewee vbox export debian-%(arch)s '
               '--force') % env, capture=False)

    vagrant_stop_container()


def vagrant_generate_tribus_base_image():
    """
    Generate a Tribus environment (Docker) image.

    This function generates a minimal Debian (stable) chroot using debootstrap.

    .. versionadded:: 0.2
    """
    vagrant_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Creating a new Tribus base image ...')

        local('vagrant provision', capture=False)

    vagrant_stop_container()


def vagrant_kill_all_containers():
    """
    Destroy all containers listed with ``docker ps -aq``.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Listing available containers ...')

        containers = local('vagrant box list', capture=True).split('\n')
        print containers

        # for container in containers:

        #     if container:

        #         log.info('Checking if container "%s" exists ...' % container)

        #         local('vagrant box remove %s %s' % (env.docker, container),
        #               capture=True)


def vagrant_stop_container():
    """
    Stop & commit the runtime container. Removes intermediate container.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Checking if the runtime container is up ...')

        local('vagrant halt' % env, capture=False)


def vagrant_kill_all_images():
    pass
def vagrant_kill_tribus_images():
    pass
def vagrant_pull_debian_base_image():
    pass
def vagrant_pull_tribus_base_image():
    pass
def vagrant_check_container():
    pass
def vagrant_login_container():
    pass
def vagrant_reset_container():
    pass
def vagrant_update_container():
    pass



# def vagrant_check_container():
#     """
#     Check if the runtime container is up, start if not.

#     .. versionadded:: 0.2
#     """
#     with hide('warnings', 'stderr', 'running'):

#         log.info('Checking if the runtime container is up ...')

#         state = json.loads(local(('sudo bash -c '
#                                   '"%(vagrant)s inspect '
#                                   '%(tribus_runtime_container)s"') % env,
#                                  capture=True))
#     if state:
#         if not state[0]['State']['Running']:

#             vagrant_stop_container()
#             vagrant_start_container()

#     else:

#         vagrant_start_container()

#     vagrant_check_ssh_to_container()
