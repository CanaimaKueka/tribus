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


def celery_purge_tasks():
    """
    """

    docker_check_container()

    env.host_string = '127.0.0.1'
    env.user = 'root'
    env.port = '22222'
    env.password = 'tribus'

    with cd(env.basedir):
        with shell_env(**env.fvars):
            run('python manage.py celery purge')
