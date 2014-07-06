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

from contextlib import nested
from fabric.api import run, env, cd, shell_env, hide, settings

from tribus.common.fabric.docker import docker_check_container


def update_catalog():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py update_catalog')


def extract_messages():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py extract_messages')


def compile_catalog():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py compile_catalog')


def init_catalog():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py init_catalog')


def tx_pull():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('tx pull -a --skip')


def tx_push():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('tx push -s -t --skip --no-interactive')


def build_sphinx():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py build_sphinx')


def build_css():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py build_css')


def build_js():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py build_js')


def build_man():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py build_man')


def build():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py build')


def clean_css():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_css')


def clean_js():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_js')


def clean_sphinx():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_sphinx')


def clean_mo():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_mo')


def clean_man():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_man')


def clean_dist():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_dist')


def clean_pyc():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean_pyc')


def clean():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py clean')


def sdist():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py sdist')


def bdist():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py bdist')


def install():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py install')


def test():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py test')


def report_setup_data():
    """
    """

    docker_check_container()

    with nested(cd(env.basedir), shell_env(**env.fvars),
                hide('warnings', 'stderr', 'running'),
                settings(warn_only=True)):
        run('python setup.py report_setup_data')
