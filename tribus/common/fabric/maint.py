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


def docker_kill_all_images(env):
    '''
    '''

    images = local(('sudo bash -c '
                    '"%(docker)s images -aq"') % env, capture=True)

    if images:
        env.docker_images_to_kill = images.replace('\n', ' ')
        local(('sudo bash -c '
               '"%(docker)s rmi -f %(docker_images_to_kill)s" || true') % env,
              capture=False)


def docker_kill_tribus_images(env):
    '''
    '''

    local(('sudo bash -c '
           '"%(docker)s rmi -f %(tribus_runtime_image)s '
           '%(tribus_base_image)s %(debian_base_image)s" || true') % env,
          capture=False)


def docker_generate_debian_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('sudo bash %(debian_base_image_script)s '
           'luisalejandro/debian-%(arch)s '
           'wheezy %(arch)s') % env, capture=False)


def docker_generate_tribus_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('echo "#!/usr/bin/env bash\n'
           '%(preseed_env)s\n'
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
           'echo \\"root:tribus\\" | chpasswd\n'
           'echo \\"postgres:tribus\\" | chpasswd\n'
           'echo \\"openldap:tribus\\" | chpasswd\n'
           'echo \\"mongodb:tribus\\" | chpasswd\n'
           'echo \\"redis:tribus\\" | chpasswd\n'
           'echo \\"smallfiles = true\\" >> /etc/mongodb.conf\n'
           '%(restart_services)s\n'
           'sudo -i -u postgres bash -c \\"psql -f \'%(preseed_db)s\'\\"\n'
           'ldapadd %(ldap_args)s -f \\"%(preseed_ldap)s\\"\n'
           'apt-get purge %(debian_build_dependencies)s\n'
           'apt-get autoremove\n'
           'apt-get autoclean\n'
           'apt-get clean\n'
           '%(clean)s\n'
           'exit 0'
           '" > %(tribus_base_image_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -it --name %(tribus_runtime_container)s '
           '%(mounts)s %(debian_base_image)s '
           'bash %(tribus_base_image_script)s"') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_base_image)s"') % env)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)


def docker_pull_debian_base_image(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('sudo bash -c '
           '"%(docker)s pull %(debian_base_image)s"') % env)


def docker_pull_tribus_base_image(env):
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


def docker_commit_tribus_runtime_container(env):
    '''
    '''

    local(('sudo bash -c '
           '"%(docker)s stop %(tribus_runtime_container)s" || true') % env,
          capture=False)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s" || true') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s rm %(tribus_runtime_container)s" || true') % env,
          capture=False)


def docker_startsshd(env):
    '''
    '''
    docker_commit_tribus_runtime_container(env)
    local(('sudo bash -c '
           '"%(docker)s run -d '
           '-p 127.0.0.1:22222:22 '
           '-p 127.0.0.1:8000:8000 '
           '--name=%(tribus_runtime_container)s '
           '%(mounts)s %(tribus_runtime_image)s '
           '/usr/sbin/sshd -D"') % env, capture=False)


def docker_stopsshd(env):
    '''
    '''
    docker_commit_tribus_runtime_container(env)
