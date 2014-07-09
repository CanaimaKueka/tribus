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
This module contains directives to manage Docker containers.

This module define funtions to accomplish the following tasks:

- Creating a Debian (stable) minimal base (Docker) image.
- Creating a Tribus environment (Docker) image.
- Execute commands on a Docker image to create commands.
- Destroy all images and/or containers.
- Other management commands (reset, updat, login, etc).

.. versionadded:: 0.2
"""

import sys
import time
import json
import paramiko
from contextlib import nested
from fabric.api import env, local, hide, run, shell_env, cd

from tribus.common.logger import get_logger

log = get_logger()


def docker_kill_all_containers():
    """
    Destroy all containers listed with ``docker ps -aq``.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Listing available containers ...')

        containers = local(('sudo bash -c "%(docker)s ps -aq"') % env,
                           capture=True).split('\n')

        for container in containers:

            if container:

                log.info('Checking if container "%s" exists ...' % container)

                inspect = json.loads(local(('sudo bash -c '
                                            '"%s inspect %s"') % (env.docker,
                                                                  container),
                                           capture=True))
                if inspect:

                    log.info('Destroying container "%s" ...' % container)

                    local(('sudo bash -c '
                           '"%s stop --time 1 %s"') % (env.docker, container),
                          capture=True)
                    local(('sudo bash -c '
                           '"%s rm -fv %s"') % (env.docker, container),
                          capture=True)


def docker_kill_tribus_images():
    """
    Destroy all Docker images made for Tribus.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Listing available images ...')

        images = [env.tribus_base_image, env.tribus_runtime_image,
                  env.debian_base_image]

        for image in images:

            if image:

                log.info('Checking if image "%s" exists ...' % image)

                inspect = json.loads(local(('sudo bash -c '
                                            '"%s inspect %s"') % (env.docker,
                                                                  image),
                                           capture=True))
                if inspect:

                    log.info('Destroying image "%s" ...' % image)

                    local(('sudo bash -c '
                           '"%s rmi -f %s"') % (env.docker, image),
                          capture=True)


def docker_kill_all_images():
    """
    Destroy all Docker images.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Listing available images ...')

        images = local(('sudo bash -c "%(docker)s images -aq"') % env,
                       capture=True).split('\n')

        for image in images:

            if image:

                log.info('Checking if image "%s" exists ...' % image)

                inspect = json.loads(local(('sudo bash -c '
                                            '"%s inspect %s"') % (env.docker,
                                                                  image),
                                           capture=True))
                if inspect:

                    log.info('Destroying image "%s" ...' % image)

                    local(('sudo bash -c '
                           '"%s rmi -f %s"') % (env.docker, image),
                          capture=True)


def docker_generate_debian_base_image():
    """
    Generate a Debian base (Docker) image.

    This function generates a minimal Debian (stable) chroot using debootstrap.

    .. versionadded:: 0.2
    """
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Creating a new Debian base image ...')

        local(('sudo bash %(debian_base_image_script)s '
               'luisalejandro/debian-%(arch)s '
               'wheezy %(arch)s') % env, capture=False)

    docker_stop_container()


def docker_generate_tribus_base_image():
    """
    Generate a Tribus environment (Docker) image.

    This function generates a minimal Debian (stable) chroot using debootstrap.

    .. versionadded:: 0.2
    """
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Creating a new Tribus base image ...')

        local(('sudo bash -c '
               '"%(docker)s run -it --name %(tribus_runtime_container)s '
               '%(mounts)s %(dvars)s %(debian_base_image)s '
               'bash %(tribus_base_image_script)s"') % env, capture=False)

        log.info('Creating the runtime container ...')

        local(('sudo bash -c '
               '"%(docker)s commit %(tribus_runtime_container)s '
               '%(tribus_base_image)s"') % env, capture=True)

    docker_stop_container()


def docker_pull_debian_base_image():
    """
    Pull the Debian base image from the Docker index.

    .. versionadded:: 0.2
    """
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Downloading the Debian base image ...')

        local(('sudo bash -c '
               '"%(docker)s pull %(debian_base_image)s"') % env, capture=False)

    docker_stop_container()


def docker_pull_tribus_base_image():
    """
    Pull the Tribus environment image from the Docker index.

    .. versionadded:: 0.2
    """
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Downloading the Tribus base image ...')

        local(('sudo bash -c '
               '"%(docker)s pull %(tribus_base_image)s"') % env, capture=False)

        log.info('Creating the runtime container ...')

        local(('sudo bash -c '
               '"%(docker)s run -it --name %(tribus_runtime_container)s '
               '%(tribus_base_image)s true"') % env, capture=False)

    docker_stop_container()


def generate_debian_base_image_i386():
    """
    Shortcut function to ``docker_generate_debian_base_image()`` (i386).

    .. versionadded:: 0.2
    """
    env.arch = 'i386'
    docker_generate_debian_base_image()


def generate_debian_base_image_amd64():
    """
    Shortcut function to ``docker_generate_debian_base_image()`` (amd64).

    .. versionadded:: 0.2
    """
    env.arch = 'amd64'
    docker_generate_debian_base_image()


def generate_tribus_base_image_i386():
    """
    Shortcut function to ``docker_generate_tribus_base_image()`` (i386).

    .. versionadded:: 0.2
    """
    env.arch = 'i386'
    env.debian_base_image = 'luisalejandro/debian-i386:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-i386:wheezy'
    docker_pull_debian_base_image()
    docker_generate_tribus_base_image()


def generate_tribus_base_image_amd64():
    """
    Shortcut function to ``docker_generate_tribus_base_image()`` (amd64).

    .. versionadded:: 0.2
    """
    env.arch = 'amd64'
    env.debian_base_image = 'luisalejandro/debian-amd64:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-amd64:wheezy'
    docker_pull_debian_base_image()
    docker_generate_tribus_base_image()


def docker_check_image():
    """
    Check if the runtime image exists, build environment if not.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Checking if we have a runtime image ...')

        state = json.loads(local(('sudo bash -c '
                                  '"%(docker)s inspect '
                                  '%(tribus_runtime_image)s"') % env,
                                 capture=True))
    if not state:
        environment()


def docker_check_container():
    """
    Check if the runtime container is up, start if not.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Checking if the runtime container is up ...')

        state = json.loads(local(('sudo bash -c '
                                  '"%(docker)s inspect '
                                  '%(tribus_runtime_container)s"') % env,
                                 capture=True))
    if state:
        if not state[0]['State']['Running']:

            docker_stop_container()
            docker_start_container()

    else:

        docker_start_container()

    docker_check_ssh_to_container()


def docker_check_ssh_to_container():
    """
    Test if SSH is up inside the runtime container.

    .. versionadded:: 0.2
    """
    log.info('Testing communication with container ...')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    tries = 0

    while True:
        tries += 1
        try:
            time.sleep(2)
            ssh.connect(hostname=env.host_string, port=env.port,
                        username=env.user, password=env.password)
        except Exception, e:
            log.info('SSH is not ready yet: %s' % e)
        else:
            break
        finally:
            ssh.close()

        if tries == 10:
            log.error('Failed to connect to the container.')
            sys.exit(1)

    log.info('Communication with the container succeded!')


def docker_start_container():
    """
    Start the runtime container.

    .. versionadded:: 0.2
    """
    docker_check_image()

    with hide('warnings', 'stderr', 'running'):

        log.info('Starting the runtime container ...')

        local(('sudo bash -c '
               '"%(docker)s run -d '
               '-p 127.0.0.1:22222:22 '
               '-p 127.0.0.1:8000:8000 '
               '--name %(tribus_runtime_container)s '
               '%(mounts)s %(dvars)s %(tribus_runtime_image)s '
               'bash %(tribus_start_container_script)s"') % env, capture=True)


def docker_stop_container():
    """
    Stop & commit the runtime container. Removes intermediate container.

    .. versionadded:: 0.2
    """
    with hide('warnings', 'stderr', 'running'):

        log.info('Checking if the runtime container is up ...')

        runtime_id = json.loads(local(('sudo bash -c '
                                       '"%(docker)s inspect '
                                       '%(tribus_runtime_image)s"') % env,
                                      capture=True))

        inspect = json.loads(local(('sudo bash -c '
                                    '"%(docker)s inspect '
                                    '%(tribus_runtime_container)s"') % env,
                                   capture=True))
        if inspect:

            log.info('Stopping the runtime container ...')

            local(('sudo bash -c '
                   '"%(docker)s stop --time 1 '
                   '%(tribus_runtime_container)s"') % env,
                  capture=True)
            local(('sudo bash -c '
                   '"%(docker)s commit %(tribus_runtime_container)s '
                   '%(tribus_runtime_image)s"') % env, capture=True)
            local(('sudo bash -c '
                   '"%(docker)s rm -fv %(tribus_runtime_container)s"') % env,
                  capture=True)

        if runtime_id:

            local(('sudo bash -c '
                   '"%s rmi -f %s"') % (env.docker, runtime_id[0]['Id']),
                  capture=True)


def docker_login_container():
    """
    Login into the runtime container.

    .. versionadded:: 0.2
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):

        log.info('Opening a shell inside the runtime container ...')
        log.info('(When you are done, press CTRL+D to get out).')

        run('bash')


def docker_update_container():
    """
    Update the runtime container with latest changes to dependencies.

    This function executes the script that generates the Tribus environment
    image inside the runtime container so that it picks up the changes
    made to the environment dependencies.

    .. versionadded:: 0.2
    """
    docker_check_image()
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Updating the Tribus base image ...')

        local(('sudo bash -c '
               '"%(docker)s run -it --name %(tribus_runtime_container)s '
               '%(mounts)s %(dvars)s %(tribus_runtime_image)s '
               'bash %(tribus_base_image_script)s"') % env, capture=False)

    docker_stop_container()


def docker_reset_container():
    """
    Restore the Tribus environment image to its original state.

    .. versionadded:: 0.2
    """
    from tribus.common.fabric.django import django_syncdb

    docker_check_image()
    docker_stop_container()

    with hide('warnings', 'stderr', 'running'):

        log.info('Restoring the Tribus base image ...')

        local(('sudo bash -c '
               '"%(docker)s run -it --name %(tribus_runtime_container)s '
               '%(tribus_base_image)s true"') % env, capture=False)

    docker_stop_container()
    django_syncdb()


def environment():
    """
    Reproduce the Tribus developer environment.

    This function takes care of downloading and installing the software that
    is needed to develop and maintain Tribus.

    .. versionadded:: 0.2
    """
    from tribus.common.fabric.django import django_syncdb

    docker_pull_debian_base_image()
    docker_pull_tribus_base_image()
    django_syncdb()
