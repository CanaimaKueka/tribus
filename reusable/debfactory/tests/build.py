#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@copyright: 

  (C) Copyright 2009-2010, GetDeb Team - https://launchpad.net/~getdeb
  --------------------------------------------------------------------
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  --------------------------------------------------------------------

  Build system testring script

"""

dsc_url = "http://archive.ubuntu.com/ubuntu/pool/universe/n/netcat/netcat_1.10-38.dsc"
component = 'apps'

import os
import sys
import commands

from os.path import join, dirname, exists, realpath, abspath
LAUNCH_DIR = abspath(sys.path[0])
LIB_DIR = join(LAUNCH_DIR, '..', 'lib')
sys.path.insert(0, LIB_DIR)

from dpkg_control import DebianControlFile

def run_or_exit(cmd):
    """ executed command with sytem(), quit script if exit code is non zero """
    rc = os.system(cmd)
    if rc != 0:
        sys.exit(rc)

if len(sys.argv) > 1:
    dsc_url = sys.argv[1]
    
release = commands.getoutput('lsb_release -cs')
run_dir = os.getcwd()
if not os.path.isdir('/tmp/build_test'):
    os.mkdir('/tmp/build_test')
os.chdir('/tmp/build_test')

dsc_file = os.path.basename(dsc_url)

# Get and extract, apply the current release, generate a _source changes
run_or_exit('dget -ux '+dsc_url)
debian_control = DebianControlFile(dsc_file)
upstream_version = debian_control.upstream_version()
package_name = debian_control['Source']
os.chdir(join('/tmp/build_test', '%s-%s' % (package_name, upstream_version)))
run_or_exit('dch -D %s Testing package' % release)
run_or_exit('debuild -S -sa -uc')
changes_control = DebianControlFile('/tmp/build_test/%s_%s_source.changes' % (package_name, debian_control.version()))
if not os.path.exists('/tmp/build_incoming/'+release+'/apps'):
    os.makedirs('/tmp/build_incoming/'+release+'/apps')
changes_control.move('/tmp/build_incoming/'+release+'/apps', '/tmp/build_test/')
os.chdir(run_dir)

# Test the process
run_or_exit('build/process_incoming.py --skip-gpg-check -i /tmp/build_incoming -o /tmp/pre_build')
run_or_exit('build/process_pre_build.py --skip-gpg-check -i /tmp/pre_build -o /tmp/post_build')
if not os.environ.get('REPREPRO_BASE_DIR'):
    print "Skipping reprepro test, REPREPRO_BASE_DIR not defined"
else:
    run_or_exit('build/process_post_build.py -i /tmp/post_build')
