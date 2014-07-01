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

import json
from fabric.api import local, env


def docker_kill_all_containers():
    """
    """

    containers = local(('sudo bash -c '
                        '"%(docker)s ps -aq"') % env, capture=True)

    if containers:
        env.docker_containers_to_kill = containers.replace('\n', ' ')
        local(('sudo bash -c '
               '"%(docker)s stop --time 1 '
               '%(docker_containers_to_kill)s"') % env,
              capture=False)
        local(('sudo bash -c '
               '"%(docker)s rm -fv %(docker_containers_to_kill)s"') % env,
              capture=False)


def docker_kill_all_images():
    """
    """

    images = local(('sudo bash -c '
                    '"%(docker)s images -aq"') % env, capture=True)

    if images:
        env.docker_images_to_kill = images.replace('\n', ' ')
        local(('sudo bash -c '
               '"%(docker)s rmi -f %(docker_images_to_kill)s" || true') % env,
              capture=False)


def docker_kill_tribus_images():
    """
    """

    local(('sudo bash -c '
           '"%(docker)s rmi -f %(tribus_runtime_image)s '
           '%(tribus_base_image)s %(debian_base_image)s" || true') % env,
          capture=False)


def docker_generate_debian_base_image():
    """
    """

    docker_stop_container()
    local(('sudo bash %(debian_base_image_script)s '
           'luisalejandro/debian-%(arch)s '
           'wheezy %(arch)s') % env, capture=False)
    docker_stop_container()


def generate_tribus_base_image_script():
    """
    """

    local(('echo "#!/usr/bin/env bash\n'
           '%(preseed_env)s\n'
           'debconf-set-selections %(preseed_debconf)s\n'
           'apt-get update\n'
           'apt-get install %(debian_run_dependencies)s\n'
           'apt-get install %(debian_build_dependencies)s\n'
           'python %(tribus_get_pip_script)s\n'
           'pip install %(python_dependencies)s\n'
           'echo \\"root:tribus\\" | chpasswd\n'
           'echo \\"postgres:tribus\\" | chpasswd\n'
           'echo \\"openldap:tribus\\" | chpasswd\n'
           'echo \\"redis:tribus\\" | chpasswd\n'
           '%(start_services)s\n'
           'sudo -i -u postgres bash -c \\"psql -f \'%(preseed_db)s\'\\"\n'
           'ldapadd %(ldap_args)s -f \\"%(preseed_ldap)s\\"\n'
           'apt-get purge %(debian_build_dependencies)s\n'
           'apt-get autoremove\n'
           'apt-get autoclean\n'
           'apt-get clean\n'
           '%(clean)s\n'
           'exit 0'
           '" > %(tribus_base_image_script)s') % env, capture=False)


def docker_generate_tribus_base_image():
    """
    """

    docker_stop_container()
    generate_tribus_base_image_script()
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(mounts)s %(debian_base_image)s '
           'bash %(tribus_base_image_script)s"') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_base_image)s"') % env, capture=False)
    docker_stop_container()


def docker_pull_debian_base_image():
    """
    """

    docker_stop_container()
    local(('sudo bash -c '
           '"%(docker)s pull %(debian_base_image)s"') % env, capture=False)
    docker_stop_container()


def docker_pull_tribus_base_image():
    """
    """

    docker_stop_container()
    local(('sudo bash -c '
           '"%(docker)s pull %(tribus_base_image)s"') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(tribus_base_image)s true"') % env, capture=False)
    docker_stop_container()


def generate_debian_base_image_i386():
    """
    """
    env.arch = 'i386'
    docker_generate_debian_base_image()


def generate_debian_base_image_amd64():
    """
    """
    env.arch = 'amd64'
    docker_generate_debian_base_image()


def generate_tribus_base_image_i386():
    """
    """
    env.arch = 'i386'
    env.debian_base_image = 'luisalejandro/debian-i386:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-i386:wheezy'
    docker_pull_debian_base_image()
    docker_generate_tribus_base_image()


def generate_tribus_base_image_amd64():
    """
    """
    env.arch = 'amd64'
    env.debian_base_image = 'luisalejandro/debian-amd64:wheezy'
    env.tribus_base_image = 'luisalejandro/tribus-amd64:wheezy'
    docker_pull_debian_base_image()
    docker_generate_tribus_base_image()


def docker_check_container():
    """
    """

    if local(('sudo bash -c '
              '"%(docker)s ps -a '
              '| grep %(tribus_runtime_container)s" || true') % env,
             capture=True):

        if not json.loads(local(('sudo bash -c '
                                 '"%(docker)s inspect '
                                 '%(tribus_runtime_container)s"') % env,
                                capture=True))[0]['State']['Running']:
            docker_stop_container()
            docker_start_container()

    else:

        docker_start_container()


def docker_start_container():
    """
    """

    local(('echo "#!/usr/bin/env bash\n'
           '%(start_services)s\n'
           'tail -f /dev/null\n'
           '" > %(tribus_start_container_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -d '
           '-p 127.0.0.1:22222:22 '
           '-p 127.0.0.1:8000:8000 '
           '--name %(tribus_runtime_container)s '
           '%(mounts)s %(tribus_runtime_image)s '
           'bash %(tribus_start_container_script)s"') % env, capture=False)


def docker_stop_container():
    """
    """

    if local(('sudo bash -c '
              '"%(docker)s ps -a '
              '| grep %(tribus_runtime_container)s" || true') % env,
             capture=True):
        local(('sudo bash -c '
               '"%(docker)s stop --time 1 '
               '%(tribus_runtime_container)s"') % env,
              capture=False)
        local(('sudo bash -c '
               '"%(docker)s commit %(tribus_runtime_container)s '
               '%(tribus_runtime_image)s"') % env, capture=False)
        local(('sudo bash -c '
               '"%(docker)s rm -fv %(tribus_runtime_container)s"') % env,
              capture=False)


def docker_login_container():
    """
    """

    docker_stop_container()
    local(('sudo bash -c '
           '"%(docker)s run -it '
           '-p 127.0.0.1:22222:22 '
           '-p 127.0.0.1:8000:8000 '
           '--name %(tribus_runtime_container)s '
           '%(mounts)s %(tribus_runtime_image)s bash"') % env, capture=False)
    docker_stop_container()


def docker_update_container():
    """
    """

    docker_stop_container()
    generate_tribus_base_image_script()
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(mounts)s %(tribus_runtime_image)s '
           'bash %(tribus_base_image_script)s"') % env, capture=False)
    docker_stop_container()


def docker_reset_container():
    """
    """

    docker_stop_container()
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(tribus_base_image)s true"') % env, capture=False)
    docker_stop_container()
