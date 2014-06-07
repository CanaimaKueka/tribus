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


def generate_tribus_base_image(env):
    local(('sudo /bin/bash -c "echo -e \''
           'FROM %(debian_base_image)s\n'
           'MAINTAINER %(docker_maintainer)s\n'
           '%(preseed_env)s\n'
           'RUN echo -e \\"%(preseed_db)s\\" > preseed-db.sql\n'
           'RUN echo -e \\"%(preseed_ldap)s\\" > preseed-ldap.ldif\n'
           'RUN echo -e \\"%(preseed_debconf)s\\" > preseed-debconf.conf\n'
           'RUN debconf-set-selections preseed-debconf.conf\n'
           'RUN apt-get update\n'
           'RUN apt-get install %(debian_dependencies)s\n'
           '%(restart_services)s\n'
           'RUN pip install %(python_dependencies)s\n'
           'RUN echo \\"postgres:tribus\\" | chpasswd\n'
           'RUN sudo -iu postgres /bin/bash -c \\"psql -f preseed-db.sql\\"\n'
           'RUN ldapadd %(ldap_args)s -f \\"preseed-ldap.ldif\\"\n'
           'RUN apt-get autoremove\n'
           'RUN apt-get autoclean\n'
           'RUN apt-get clean\n'
           'RUN find /usr -name "*.pyc" -print0 | xargs -0r rm -rf\n'
           'RUN find /var/cache/apt -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /usr/share/man -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /usr/share/doc -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /usr/share/locale -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /var/log -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /var/tmp -type f -print0 | xargs -0r rm -rf\n'
           'RUN find /tmp -type f -print0 | xargs -0r rm -rf\n'
           '\' > /tmp/Dockerfile"') % env, capture=False)
    local(('sudo /bin/bash -c '
           '"docker.io build -t %(tribus_base_image)s '
           '- < /tmp/Dockerfile"') % env, capture=False)


def pull_tribus_base_image(env):

    containers = local(('sudo /bin/bash -c "docker.io ps -aq"'), capture=True)

    if containers:
        local(('sudo /bin/bash -c '
               '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
              capture=False)

    if env.tribus_base_image_id not in local(('sudo /bin/bash -c '
                                              '"docker.io images -aq"'),
                                             capture=True):
        local(('sudo /bin/bash -c '
               '"docker.io pull %(tribus_base_image)s"') % env)


# def docker_pull_base_image():

#     containers = local(('sudo /bin/bash -c "docker.io ps -aq"'), capture=True)

#     if containers:
#         local(('sudo /bin/bash -c '
#                '"docker.io rm -fv %s"') % containers.replace('\n', ' '),
#               capture=False)

#     if env.docker_base_image_id not in local(('sudo /bin/bash -c '
#                                               '"docker.io images -aq"'),
#                                              capture=True):
#         local(('sudo /bin/bash -c '
#                '"docker.io pull %(docker_base_image)s"') % env)

#     local(('sudo /bin/bash -c '
#            '"docker.io run -it '
#            '--name %(docker_container)s '
#            '%(docker_env_args)s '
#            '%(docker_env_vol)s '
#            '%(docker_base_image)s '
#            'apt-get install '
#            '%(apt_args)s '
#            '%(docker_env_packages)s"') % env)

#     local(('sudo /bin/bash -c '
#            '"docker.io commit '
#            '%(docker_container)s %(docker_env_image)s"') % env)

#     local(('sudo /bin/bash -c '
#           '"docker.io rm -fv %(docker_container)s"') % env)
