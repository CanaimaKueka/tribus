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

from fabric.api import run, env, cd, shell_env
from tribus.common.fabric.docker import docker_check_container


def get_selected():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py get_selected',
                shell_escape=False)


def install_repository():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py install_repository',
                shell_escape=False)


def get_sample_packages():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py get_sample_packages',
                shell_escape=False)


def select_sample_packages():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py select_sample_packages',
                shell_escape=False)


def index_selected():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py index_selected',
                shell_escape=False)


def index_sample_packages():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py index_sample_packages',
                shell_escape=False)


def wipe_repo():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py wipe_repo',
                shell_escape=False)


def filldb_from_remote():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py filldb_from_remote',
                shell_escape=False)


def filldb_from_local():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py filldb_from_local',
                shell_escape=False)


def create_cache_from_remote():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python manage.py create_cache_from_remote',
                shell_escape=False)
