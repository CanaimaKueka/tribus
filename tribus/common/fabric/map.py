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

from tribus.common.fabric.docker import (docker_generate_debian_base_image,
                                         docker_generate_tribus_base_image,
                                         docker_kill_all_containers,
                                         docker_kill_all_images,
                                         docker_kill_tribus_images,
                                         docker_pull_debian_base_image,
                                         docker_pull_tribus_base_image,
                                         docker_check_container,
                                         docker_stop_container,
                                         docker_login_container,
                                         docker_reset_container,
                                         docker_update_container)
from tribus.common.fabric.vagrant import (vagrant_generate_debian_base_image,
                                          vagrant_generate_tribus_base_image,
                                          vagrant_kill_all_containers,
                                          vagrant_kill_all_images,
                                          vagrant_kill_tribus_images,
                                          vagrant_pull_debian_base_image,
                                          vagrant_pull_tribus_base_image,
                                          vagrant_check_container,
                                          vagrant_stop_container,
                                          vagrant_login_container,
                                          vagrant_reset_container,
                                          vagrant_update_container)
from tribus.common.fabric.environ import (docker_enable_environment,
                                          vagrant_enable_environment)

FABRIC_FUNCTION_MAP = {
    'docker': {
        'enable_environment': docker_enable_environment,
        'generate_debian_base_image': docker_generate_debian_base_image,
        'generate_tribus_base_image': docker_generate_tribus_base_image,
        'pull_debian_base_image': docker_pull_debian_base_image,
        'pull_tribus_base_image': docker_pull_tribus_base_image,
        'kill_all_containers': docker_kill_all_containers,
        'kill_tribus_images': docker_kill_tribus_images,
        'kill_all_images': docker_kill_all_images,
        'check_container': docker_check_container,
        'stop_container': docker_stop_container,
        'login_container': docker_login_container,
        'reset_container': docker_reset_container,
        'update_container': docker_update_container
    },
    'vagrant': {
        'enable_environment': vagrant_enable_environment,
        'generate_debian_base_image': vagrant_generate_debian_base_image,
        'generate_tribus_base_image': vagrant_generate_tribus_base_image,
        'pull_debian_base_image': vagrant_pull_debian_base_image,
        'pull_tribus_base_image': vagrant_pull_tribus_base_image,
        'kill_all_containers': vagrant_kill_all_containers,
        'kill_tribus_images': vagrant_kill_tribus_images,
        'kill_all_images': vagrant_kill_all_images,
        'check_container': vagrant_check_container,
        'stop_container': vagrant_stop_container,
        'login_container': vagrant_login_container,
        'reset_container': vagrant_reset_container,
        'update_container': vagrant_update_container
    }
}
