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
Django management commands.

This module will run several Django management commands inside the docker
runtime container.

.. versionadded:: 0.2
"""

from contextlib import nested
from fabric.api import env, run, cd, shell_env, hide

from tribus.common.fabric.docker import docker_check_container
from tribus.common.logger import get_logger

log = get_logger()


def django_syncdb():
    """
    Synchronize the configuration of the container with current codebase.

    This function executes Django's syncdb, configures admin users, registers
    Waffle's switches, among other operations.

    .. versionadded:: 0.2
    """
    docker_check_container()

    log.info('Syncing databases and configuration ...')

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('bash %(tribus_django_syncdb_script)s' % env)


def django_runserver():
    """
    Run the Django development server and other services.

    .. versionadded:: 0.2
    """
    docker_check_container()

    log.info('Starting services ...')

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('bash %(tribus_django_runserver_script)s' % env)


def django_shell():
    """
    Open a Django shell inside the runtime container.

    .. versionadded:: 0.2
    """
    docker_check_container()

    log.info('Opening a django shell inside the runtime container ...')
    log.info('(When you are done, press CTRL+D to get out).')

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py shell')


def celery_purge_tasks():
    """
    Remove all tasks from the Celery queue.

    .. versionadded:: 0.2
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py celery purge')


def haystack_rebuild_index():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py rebuild_index')


def get_selected():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py get_selected')


def install_repository():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py install_repository')


def get_sample_packages():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py get_sample_packages')


def select_sample_packages():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py select_sample_packages')


def index_selected():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py index_selected')


def index_sample_packages():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py index_sample_packages')


def wipe_repo():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py wipe_repo')


def filldb_from_remote():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py filldb_from_remote')


def filldb_from_local():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py filldb_from_local')


def create_cache_from_remote():
    """
    """
    docker_check_container()

    with nested(hide('warnings', 'stderr', 'running'),
                shell_env(**env.fvars), cd(env.basedir)):
        run('python manage.py create_cache_from_remote')
