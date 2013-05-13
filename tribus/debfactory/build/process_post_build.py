#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
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

  This script will check the post_build directory
  When *_.changes is found, it's contents are verified and
  the files are included in the testing_repository
  
  The expected structure is post_build dir/release/component 
  
  Files will be verified with the following rules
		...		
  A lock file is used to prevent concurrent runs
"""
import os
import sys
import time
import glob
import commands
import shutil
from optparse import OptionParser
from configobj import ConfigObj

from os.path import join, dirname, exists, realpath, abspath
LAUNCH_DIR = abspath(sys.path[0])
LIB_DIR = join(LAUNCH_DIR, '..', 'lib')
sys.path.insert(0, LIB_DIR)

from log import Logger
from dpkg_control import DebianControlFile
from lockfile import LockFile
from config import check_config

config_file = "%s/debfactory/etc/debfactory.conf" % os.environ['HOME']
config = ConfigObj(config_file)

# Check for required configuration
check_config(config, ['sender_email'])

Log = Logger()

def extract_changelog(changes_file, component, pool_dir):
    """ 
    Extract the changelog according to the changes_file
    If handling a _source.changes, extract the real changelog
    If handling binary .changes just creat a link for each of the binaries
    """
    global config, options

    extract_dir = '/tmp/changelog_extract'
    control_file = DebianControlFile(changes_file)
    name = control_file['Source']
    name_version = name + '_' + control_file.version()
    if name.startswith('lib'):
        prefix = name[:4]
    else:
        prefix = name[0]

    pool_dir = join(options.output_dir, 'pool', \
                                 component, prefix, name)
    dirname = os.path.dirname(changes_file)
    if changes_file.endswith('_source.changes'): # Really extract
        if os.path.isdir(extract_dir):
            shutil.rmtree(extract_dir)
        for file in control_file.files_list():
            if file.name.endswith('.dsc'):
                (rc, output) = commands.getstatusoutput('dpkg-source -x %s %s' % \
                          (join(pool_dir, file.name), extract_dir))
                if rc <> 0 or not os.path.isdir(extract_dir):
                    Log.print_(output)
                    Log.print_("Unable to extract source to retrieve changelog")
                else:
                    extacted_changelog = os.path.join(extract_dir, 'debian', 'changelog')
                    if not exists(extacted_changelog):
                        Log.print_("Unable to find changelog on source")
                    if not os.path.exists(pool_dir):
                        os.makedirs(pool_dir, 0755)
                    print pool_dir
                    changelog_fn = join(pool_dir, os.path.basename(changes_file).rsplit('.',1)[0]+'.changelog')
                    shutil.copy(extacted_changelog, changelog_fn)
        if os.path.isdir(extract_dir):
            shutil.rmtree(extract_dir)
    else: # binary build .changes, create a link to the corresponding source
        files = control_file.files_list()
        for file in files:
            if file.name.endswith('.deb'):
                try:
                    os.symlink(name_version+"_source.changelog", \
                        join(pool_dir, file.name.rsplit('.', 1)[0]+'.changelog'))
                except OSError: # Already exists ?
                    pass

def check_changes(release, component, filename):
    """
    Check a _.changes file and include it into the repository
    """
    global config, options
    source_dir = "%s/%s/%s" \
        % (options.input_dir, release, component)
    changes_file = "%s/%s" % (source_dir, filename)
    if not os.path.exists(changes_file):
        return 1
    Log.print_("Including %s/%s/%s" % (release, component, filename))

    # Remove previous failed status
    if exists('%s.failed' % changes_file):
        os.unlink('%s.failed' % changes_file)

    control_file = DebianControlFile(changes_file)

    name = control_file['Source'] 
    version = control_file.version()
    name_version = "%s_%s" % (control_file['Source'] \
        , control_file.version())

    report_title = "Include on testing for %s/%s/%s FAILED\n" \
        % (release, component, name_version)
    report_msg = "File: %s/%s/%s\n" % (release, component, filename)
    report_msg  += '-----------------\n'

    #target_mails.append(control_file['Changed-By'])
    report_msg  += "Signed By: %s\n\n" % control_file['Changed-By']

    # Get list of files described on the changes
    report_msg += "List of files:\n"
    report_msg += "--------------\n"
    file_list = control_file.files_list()
    for file_info in file_list:
        report_msg += "%s (%s) MD5: %s \n" \
            % (file_info.name, file_info.size, file_info.md5sum)

    if name.startswith('lib'):
        prefix = name[:4]
    else:
        prefix = name[0]

    pool_dir = join(options.output_dir, 'pool', \
                    component, prefix, name)
    file_on_dest = "%s/%s" % ( pool_dir, filename )

    # Remove all packages related to source package
    if(filename.endswith("_source.changes")):
        os.system("reprepro removesrc %s-getdeb-testing %s %s"
            % (release, name,  control_file['Version']))
        # Delete orphaned changelogs
        changelogs = glob.glob("%s/*.changelog" % (pool_dir))
        for changelog in changelogs:
            deb = changelog.rsplit('.', 1)[0]+'.deb'
            if not os.path.exists(deb):
                Log.print_("Removing changelog: %s" % (changelog))
                os.unlink(changelog)
    # Include the package (use standard as "normal" does not exist due to Debian policy)
    # (LP: #735381, #735428)
    command = "reprepro -P standard --ignore=wrongdistribution -C %s include %s-getdeb-testing %s" \
        % (component,  release, changes_file)
    (rc, output) = commands.getstatusoutput(command)
    print output
    report_msg += output
    if rc == 0:
        extract_changelog(changes_file, component, pool_dir)
        status = "SUCCESSFUL"
        control_file.remove()
    else:
        status = "FAILED"
        shutil.move(changes_file, "%s.failed" % changes_file)

    report_title = "Included on testing %s/%s/%s %s\n" \
        % (release, component, name_version, status)
    Log.print_(report_title)
    return rc

def check_post_build_dir():
    """
    Check the ftp incoming directory for release directories
    """
    global options
    file_list = glob.glob("%s/*" \
        % (options.input_dir))
    for file in file_list:
        if os.path.isdir(file):
            release = os.path.basename(file)
            check_release_dir(release)

def check_release_dir(release):
    """
    Check a release directory for components
    """
    global options
    file_list = glob.glob("%s/%s/*" \
        % (options.input_dir, release))
    for file in file_list:
        if os.path.isdir(file):
            component = os.path.basename(file)
            check_release_component_dir(release, component)

def check_release_component_dir(release, component):
    """ 
    Check a release/component directory, first process _source.changes
    then process the corresponding _i386 and _amd64 changes
    """
    global options
    Log.log("Checking %s/%s" % (release, component))
    file_list = glob.glob("%s/%s/%s/*_source.changes" \
        % (options.input_dir, release, component))

    # First we process _source.changes 
    # If the import is successful we then import the corresponding binary packages
    for fname in file_list: 
        if check_changes(release, component, os.path.basename(fname)) == 0:
            i386_changes = fname.replace('_source','_i386')
            if exists(i386_changes):
                check_changes(release, component, os.path.basename(i386_changes))
            amd64_changes = fname.replace('_source','_amd64')
            if exists(amd64_changes):
                check_changes(release, component, os.path.basename(amd64_changes))

    Log.log("Done")

def main():
    global options
    parser = OptionParser()
    parser.add_option("-q", "--quiet",
        action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")
    parser.add_option("-i", "--input-dir",
        action="store", dest="input_dir", default='/build/post_build',
        help="Input directory that will contain the *_source.changes files")
    parser.add_option("-o", "--output-dir",
        action="store", dest="output_dir", default='/archive/getdeb/ubuntu',
        help="Output directory")       
    (options, args) = parser.parse_args()
    Log.verbose=options.verbose
    try:
        lock = LockFile("ftp_incoming")
    except LockFile.AlreadyLockedError:
        Log.log("Unable to acquire lock, exiting")
        return

    # Check and process the incoming directoy
    check_post_build_dir()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'User requested interrupt'
        sys.exit(1)

