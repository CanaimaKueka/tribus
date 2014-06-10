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


def generate_debian_base_image(env):
    '''
    '''

    local(('sudo bash %(debian_base_image_script)s '
           'luisalejandro/debian-%(arch)s '
           'wheezy %(arch)s') % env, capture=False)


def generate_tribus_base_image(env):
    '''
    '''

    local(('echo "'
           '%(preseed_env)s\n'
           'debconf-set-selections %(preseed_debconf)s\n'
           'apt-get update\n'
           'apt-get install %(debian_run_dependencies)s\n'
           'apt-get install %(debian_build_dependencies)s\n'
           'easy_install pip\n'
           'pip install %(python_dependencies)s\n'
           'echo \"root:tribus\" | chpasswd\n'
           'echo \"postgres:tribus\" | chpasswd\n'
           '%(restart_services)s\n'
           'sudo -iu postgres bash -c \'psql -f %(preseed_db)s\'\n'
           'ldapadd %(ldap_args)s -f \"%(preseed_ldap)s\"\n'
           'apt-get purge %(debian_build_dependencies)s\n'
           'apt-get autoremove\n'
           'apt-get autoclean\n'
           'apt-get clean\n'
           'find /usr -name "*.pyc" -print0 | xargs -0r rm -rf\n'
           'find /var/cache/apt -type f -print0 | xargs -0r rm -rf\n'
           'find /var/lib/mongodb/journal -type f -print0 | xargs -0r rm -rf\n'
           'find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/man -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/doc -type f -print0 | xargs -0r rm -rf\n'
           'find /usr/share/locale -type f -print0 | xargs -0r rm -rf\n'
           'find /var/log -type f -print0 | xargs -0r rm -rf\n'
           'find /var/tmp -type f -print0 | xargs -0r rm -rf\n'
           'find /tmp -type f -print0 | xargs -0r rm -rf\n'
           'find /src -type f -print0 | xargs -0r rm -rf\n'
           'exit 0'
           '" > %(tribus_base_image_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"docker.io run -it --name %(tribus_runtime_container)s '
           '%(mounts)s %(debian_base_image)s '
           'bash %(tribus_base_image_script)s"') % env, capture=False)
    local(('sudo bash -c '
           '"docker.io commit %(tribus_runtime_container)s '
           '%(tribus_base_image)s"') % env)


def pull_debian_base_image(env):
    '''
    '''

    containers = local(('sudo bash -c '
                        '"docker.io ps -aq"'), capture=True)
    imagestat = local(('sudo bash -c '
                       '"docker.io inspect %(debian_base_image)s"') % env,
                      capture=True)

    if containers:
        local(('sudo bash -c '
               '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
              capture=False)

    if imagestat.return_code:
        local(('sudo bash -c '
               '"docker.io pull %(debian_base_image)s"') % env)


def pull_tribus_base_image(env):
    '''
    '''

    containers = local(('sudo bash -c "docker.io ps -aq"'), capture=True)
    imagestat = local(('sudo bash -c '
                       '"docker.io inspect %(tribus_base_image)s"'),
                      capture=True)

    if containers:
        local(('sudo bash -c '
               '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
              capture=False)

    if imagestat.return_code:
        local(('sudo bash -c '
               '"docker.io pull %(tribus_base_image)s"') % env)
        local(('sudo bash -c '
               '"docker.io run --name="%(tribus_runtime_container)s" '
               '%(tribus_base_image)s" /bin/true') % env)
        local(('sudo bash -c '
               '"docker.io commit %(tribus_runtime_container)s '
               '%(tribus_runtime_image)s"') % env)


def django_syncdb(env):
    '''
    '''

    local(('echo "'
           'cd %(basedir)s\n'
           'python manage.py syncdb\n'
           'python manage.py migrate\n'
           'exit 0'
           '" > %(tribus_django_syncdb_script)s') % env, capture=False)

    local(('sudo bash -c '
           '"docker.io run -it --name="%(tribus_runtime_container)s" '
           '%(mounts)s %(tribus_runtime_image)s '
           'bash %(tribus_django_syncdb_script)s"') % env)

    local(('sudo bash -c '
           '"docker.io commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)


def django_runserver(env):
    '''
    '''

    local(('echo "'
           'cd %(basedir)s\n'
           'ln -s %(tribus_nginx_config)s /etc/nginx/sites-enabled/\n'
           'ln -s %(tribus_uwsgi_config)s /etc/uwsgi/apps-enabled/\n'
           '%(restart_services)s\n'
           'exit 0'
           '" > %(tribus_django_syncdb_script)s') % env, capture=False)

    local(('sudo bash -c '
           '"docker.io run -it --name="%(tribus_runtime_container)s" '
           '%(mounts)s %(tribus_runtime_image)s '
           'bash %(tribus_django_syncdb_script)s"') % env)

    local(('sudo bash -c '
           '"docker.io commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)


def django_stopserver(env):
    '''
    '''
    pass


def django_restartserver(env):
    '''
    '''
    pass
# def docker_pull_base_image():

#     containers = local(('sudo bash -c "docker.io ps -aq"'), capture=True)

#     if containers:
#         local(('sudo bash -c '
#                '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
#               capture=False)

#     if env.docker_base_image_id not in local(('sudo bash -c '
#                                               '"docker.io images -aq"'),
#                                              capture=True):
#         local(('sudo bash -c '
#                '"docker.io pull %(docker_base_image)s"') % env)

#     local(('sudo bash -c '
#            '"docker.io run -it '
#            '--name %(docker_container)s '
#            '%(docker_env_args)s '
#            '%(docker_env_vol)s '
#            '%(docker_base_image)s '
#            'apt-get install '
#            '%(apt_args)s '
#            '%(docker_env_packages)s"') % env)

#     local(('sudo bash -c '
#            '"docker.io commit '
#            '%(docker_container)s %(docker_env_image)s"') % env)

#     local(('sudo bash -c '
#           '"docker.io rm -fv %(docker_container)s"') % env)
