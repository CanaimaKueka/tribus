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


def update_catalog():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py update_catalog', shell_escape=False)


def extract_messages():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py extract_messages', shell_escape=False)


def compile_catalog():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py compile_catalog', shell_escape=False)


def init_catalog():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py init_catalog', shell_escape=False)


def tx_pull():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('tx pull -a --skip', shell_escape=False)


def tx_push():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('tx push -s -t --skip --no-interactive', shell_escape=False)


def build_sphinx():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py build_sphinx', shell_escape=False)


def build_css():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py build_css', shell_escape=False)


def build_js():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py build_js', shell_escape=False)


def build_man():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py build_man', shell_escape=False)


def build():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py build', shell_escape=False)


def clean_css():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_css', shell_escape=False)


def clean_js():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_js', shell_escape=False)


def clean_sphinx():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_sphinx', shell_escape=False)


def clean_mo():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_mo', shell_escape=False)


def clean_man():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_man', shell_escape=False)


def clean_dist():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_dist', shell_escape=False)


def clean_pyc():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean_pyc', shell_escape=False)


def clean():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py clean', shell_escape=False)


def sdist():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py sdist', shell_escape=False)


def bdist():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py bdist', shell_escape=False)


def install():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py install', shell_escape=False)


def test():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py test', shell_escape=False)


def report_setup_data():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.preseed_env_dict):
            run('python setup.py report_setup_data', shell_escape=False)
