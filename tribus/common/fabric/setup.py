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

from fabric.api import run, env
from tribus.common.fabric.docker import docker_check_container


def update_catalog():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py update_catalog' % env,
        capture=False)


def extract_messages():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py extract_messages' % env,
        capture=False)


def compile_catalog():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py compile_catalog' % env,
        capture=False)


def init_catalog():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py init_catalog' % env, capture=False)


def tx_pull():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && tx pull -a --skip' % env, capture=False)


def tx_push():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && tx push -s -t --skip --no-interactive' % env,
        capture=False)


def build_sphinx():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py build_sphinx' % env, capture=False)


def build_css():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py build_css' % env, capture=False)


def build_js():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py build_js' % env, capture=False)


def build_man():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py build_man' % env, capture=False)


def build():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py build' % env, capture=False)


def clean_css():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_css' % env, capture=False)


def clean_js():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_js' % env, capture=False)


def clean_sphinx():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_sphinx' % env, capture=False)


def clean_mo():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_mo' % env, capture=False)


def clean_man():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_man' % env, capture=False)


def clean_dist():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_dist' % env, capture=False)


def clean_pyc():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean_pyc' % env, capture=False)


def clean():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py clean' % env, capture=False)


def sdist():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py sdist' % env, capture=False)


def bdist():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py bdist' % env, capture=False)


def install():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py install' % env, capture=False)


def test():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py test --verbose' % env,
        capture=False)


def report_setup_data():
    '''
    '''

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    run('cd %(basedir)s && python setup.py report_setup_data' % env,
        capture=False)
