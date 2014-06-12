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

from fabric.api import local


def docker_kill_all_containers(env):
    '''
    '''

    containers = local(('sudo bash -c '
                        '"%(docker)s ps -aq"') % env, capture=True)

    if containers:
        env.docker_containers_to_kill = containers.replace('\n', ' ')
        local(('sudo bash -c '
               '"%(docker)s stop %(docker_containers_to_kill)s"') % env,
              capture=False)
        local(('sudo bash -c '
               '"%(docker)s rm -fv %(docker_containers_to_kill)s"') % env,
              capture=False)


def generate_debian_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('sudo bash %(debian_base_image_script)s '
           'luisalejandro/debian-%(arch)s '
           'wheezy %(arch)s') % env, capture=False)


def generate_tribus_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('echo "#!/usr/bin/env bash\n'
           'debconf-set-selections %(preseed_debconf)s\n'
           'apt-get update\n'
           'apt-get install %(debian_run_dependencies)s\n'
           'apt-get install %(debian_build_dependencies)s\n'
           'easy_install pip\n'
           'pip install %(python_dependencies)s\n'
           'mkdir -p /var/log/tribus\n'
           'mkdir -p /var/run/tribus\n'
           'mkdir -p /var/run/sshd\n'
           'chown -R www-data:www-data /var/log/tribus\n'
           'chown -R www-data:www-data /var/run/tribus\n'
           'echo \"root:tribus\" | chpasswd\n'
           'echo \"postgres:tribus\" | chpasswd\n'
           '%(start_services)s\n'
           'sudo -iu postgres bash -c \'psql -f %(preseed_db)s\'\n'
           'ldapadd %(ldap_args)s -f \"%(preseed_ldap)s\"\n'
           'apt-get purge %(debian_build_dependencies)s\n'
           'apt-get autoremove\n'
           'apt-get autoclean\n'
           'apt-get clean\n'
           'find / -name "*.pyc" -print0 | xargs -0r rm -rf\n'
           'find /var/cache/apt -type f -print0 | xargs -0r rm -rf\n'
           'find /var/lib/mongodb/ -type f -print0 | xargs -0r rm -rf\n'
           'find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/man -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/doc -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/locale -type f -print0 | xargs -0r rm -rf\n'
           'find /var/log -type f -print0 | xargs -0r rm -rf\n'
           'find /var/tmp -type f -print0 | xargs -0r rm -rf\n'
           'find /tmp -type f -print0 | xargs -0r rm -rf\n'
           'exit 0'
           '" > %(tribus_base_image_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(preseed_env)s %(mounts)s %(debian_base_image)s '
           'bash %(tribus_base_image_script)s"') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_base_image)s"') % env)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)


def pull_debian_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('sudo bash -c '
           '"%(docker)s pull %(debian_base_image)s"') % env)


def pull_tribus_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('sudo bash -c '
           '"%(docker)s pull %(tribus_base_image)s"') % env)
    local(('sudo bash -c '
           '"%(docker)s run --name="%(tribus_runtime_container)s" '
           '%(tribus_base_image)s" /bin/true') % env)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)
