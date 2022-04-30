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

CPU = Gem::Platform.local.cpu
CURDIR = File.dirname(__FILE__)


Vagrant.configure('2') do |config|

    if CPU == 'x86_64'
        config.vm.box = 'luisalejandro/debian-amd64'
    elsif CPU == 'x86'
        config.vm.box = 'luisalejandro/debian-i386'
    end

    config.vm.synced_folder '.', '/vagrant', disabled: true
    config.vm.synced_folder '/tmp', '/tmp'
    config.vm.synced_folder CURDIR, CURDIR
    config.vm.network 'forwarded_port', guest: 22, host: 22222
    config.vm.network 'forwarded_port', guest: 8000, host: 8000

    config.vm.provision :shell do |shell|
        shell.path = 'tribus/data/scripts/tribus-base-image.sh'
        shell.args = ''
    end

end
