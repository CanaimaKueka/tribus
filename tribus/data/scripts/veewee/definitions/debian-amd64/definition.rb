#!/usr/bin/env ruby
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


Veewee::Definition.declare({
    :cpu_count => '1',
    :memory_size=> '1024',
    :disk_size => '10140',
    :disk_format => 'VMDK',
    :hostiocache => 'off',
    :os_type_id => 'Debian_64',
    :iso_file => "debian-7.5.0-amd64-netinst.iso",
    :iso_src => "http://cdimage.debian.org/debian-cd/7.5.0/amd64/iso-cd/debian-7.5.0-amd64-netinst.iso",
    :iso_md5 => "8fdb6715228ea90faba58cb84644d296",
    :iso_download_timeout => "1000",
    :boot_wait => "10",
    :boot_cmd_sequence => [
        '<Esc>',
        'install ',
        'preseed/url=http://%IP%:%PORT%/preseed.cfg ',
        'debian-installer=en_US ',
        'auto ',
        'locale=en_US ',
        'kbd-chooser/method=us ',
        'netcfg/get_hostname=%NAME% ',
        'netcfg/get_domain=vagrantup.com ',
        'fb=false ',
        'debconf/frontend=noninteractive ',
        'console-setup/ask_detect=false ',
        'console-keymaps-at/keymap=us ',
        'keyboard-configuration/xkb-keymap=us ',
        '<Enter>'
    ],
    :kickstart_port => "7122",
    :kickstart_timeout => "10000",
    :kickstart_file => "preseed.cfg",
    :ssh_login_timeout => "10000",
    :ssh_user => "vagrant",
    :ssh_password => "vagrant",
    :ssh_key => "",
    :ssh_host_port => "22222",
    :ssh_guest_port => "22",
    :sudo_cmd => "echo '%p' | sudo -S bash '%f'",
    :shutdown_cmd => "halt -p",
    :postinstall_files => ["base.sh"],
    :postinstall_timeout => "10000"
})
