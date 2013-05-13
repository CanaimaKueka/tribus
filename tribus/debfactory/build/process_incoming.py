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
  
  This script will check the ftp incoming directory for debian source
  packages. 
  When *_source.changes is found, it's contents are verified and
  the files are moved to the pre_build queue.
  
  The expected structure is input_dir/ftp_incoming_dirrelease/component 
    eg: /home/ftp/incoming/jaunty/apps
  
  Files will be verified with the following rules
		...		
  A lock file is used to prevent concurrent runs
"""
import os
import sys
import time
import glob
from optparse import OptionParser
from configobj import ConfigObj

from os.path import join, dirname, exists, realpath, abspath
LAUNCH_DIR = abspath(sys.path[0])
LIB_DIR = join(LAUNCH_DIR, '..', 'lib')
sys.path.insert(0, LIB_DIR)

from log import Logger
from mail import send_mail
from dpkg_control import DebianControlFile
from lockfile import LockFile
from config import check_config


config_file = "%s/debfactory/etc/debfactory.conf" % os.environ['HOME']
config = ConfigObj(config_file)

# Check for required configuration
check_config(config, ['sender_email'])

# Clean up all files older than 24h
CLEANUP_TIME = 24*3600

Log = Logger()

def check_incoming_dir():
    """
    Check the ftp incoming directory for release directories
    """
    global options
    file_list = glob.glob("%s/*" % options.input_dir)
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
    Check a release/component directory
    	*_source.changes will triger a verification/move action
    	files older than CLEANUP_TIME will be removed
    """
    global options
    Log.log("Checking %s/%s" % (release, component))
    file_list = glob.glob("%s/%s/%s/*" \
        % (options.input_dir, release, component))

    for fname in file_list:
        if not os.path.exists(fname): # File was removed ???
            continue
        if fname.endswith("_source.changes"):
            check_source_changes(release, component, os.path.basename(fname))
            # There could be an error, remove it anyway
            if not options.check_only and os.path.exists(fname):
                os.unlink(fname)
        else:
            if not options.check_only and time.time() - os.path.getmtime(fname) > CLEANUP_TIME:
                print "Removing old file: %s" % fname
                os.unlink(fname)
    Log.log("Done")

def check_source_changes(release, component, filename):
    """
    Check a _source.changes file and proceed as described in the script
    action flow . 
    """
    global options
    global config
    Log.print_("Checking %s/%s/%s" % (release, component, filename))

    source_dir = "%s/%s/%s" \
        % (options.input_dir, release, component)
        
    full_pre_build_dir = "%s/%s/%s" \
        % (options.output_dir, release, component)
    changes_file = "%s/%s" % (source_dir, filename)

    if not os.path.exists(full_pre_build_dir):
        os.makedirs(full_pre_build_dir, 0755)

    control_file = DebianControlFile("%s/%s" % (source_dir, filename))

    if not options.skip_gpg:    
        gpg_sign_author = control_file.verify_gpg(os.environ['HOME'] \
            +'/debfactory/keyrings/uploaders.gpg ', Log.verbose)

        if not gpg_sign_author:
            Log.print_("ERROR: Unable to verify GPG key for %s" % changes_file)
            return
    else:
        gpg_sign_author = control_file['Changed-By']
        if not gpg_sign_author:
            Log.print_("ERROR: Changed-By was not found in %s" % changes_file)
            return

    name_version = "%s_%s" % (control_file['Source'] \
        , control_file.version())

    package_release = control_file['Distribution']
    if package_release != release:
        report_title = "Upload for %s/%s/%s FAILED\n" \
            % (release, component, name_version)
        report_msg = u"The release %s on debian/changelog does noth match"\
            " the target %s\n" % (package_release, release)
        Log.print_(report_msg)
        Log.print_(report_title)
        send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)
        return

    report_title = "Upload for %s/%s/%s FAILED\n" \
        % (release, component, name_version)
    report_msg = u"File: %s/%s/%s\n" % (release, component, filename)
    report_msg  += '-----------------\n'
    
    report_msg  = u"Signed By: %s\n\n" % gpg_sign_author

    orig_file_extensions = [ "gz", "bz2", "lzma", "xz" ]
    found_orig_file = False

    # Check if orig_file is available
    for orig_file_extension in orig_file_extensions:
        orig_file = "%s_%s.orig.tar.%s" % (control_file['Source'], \
            control_file.upstream_version(), orig_file_extension)

        if not orig_file:
            Log.print_("FIXME: This should never happen")
            # FIXME: This should never happen but we should send a message
            # anyway
            return

        if os.path.exists("%s/%s" % (source_dir, orig_file)):
            found_orig_file = True
        else:
            pre_build_orig = "%s/%s" % (full_pre_build_dir, orig_file)
            if os.path.exists(pre_build_orig):
                found_orig_file = True
                Log.print_('No orig.tar.%s, using %s ' % (orig_file_extension, pre_build_orig))

    if not found_orig_file:
        print "report_msg:\n", report_msg
        report_msg += u"ERROR: Missing orig.tar.[gz,bz2,lzma,xz] for %s\n" \
            % (changes_file)
        Log.print_(report_msg)
        send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)
        return

    # Get list of files described on the changes
    report_msg += u"List of files:\n"
    report_msg += u"--------------\n"
    file_list = control_file.files_list()
    for file_info in file_list:
        report_msg += u"%s (%s) MD5: %s \n" \
            % (file_info.name, file_info.size, file_info.md5sum)
    try:
        if not options.check_only:
            control_file.move(full_pre_build_dir)
    except DebianControlFile.MD5Error, e:
        report_msg = u"MD5 mismatch: Expected %s, got %s, file: %s\n" \
            % (e.expected_md5, e.found_md5, e.name)
    except DebianControlFile.FileNotFoundError, e:
        report_msg = u"File not found: %s" % (e.filename)
    else:
        report_title = u"Upload for %s/%s/%s SUCCESSFUL\n" \
            % (release, component, name_version)
    finally:
        if not options.check_only:
            control_file.remove()
    Log.print_(report_title)
    send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)

def main():
    global options
    
    parser = OptionParser()
    parser.add_option("-c", "--check-only",
        action="store_true", dest="check_only", default=False,
        help="Check only, don't move packages")
    parser.add_option("-g", "--skip-gpg-check",
        action="store_true", dest="skip_gpg", default=False,
        help="Check only, don't move packages")
    parser.add_option("-q", "--quiet",
        action="store_false", dest="verbose", default=True,
        help="Do not print status messages to stdout")
    parser.add_option("-i", "--input-dir",
        action="store", dest="input_dir", default='/home/ftp/incoming',
        help="Input directory that will contain the *_source.changes files")
    parser.add_option("-o", "--output-dir",
        action="store", dest="output_dir", default='/build/pre_build',
        help="Output directory")            
    (options, args) = parser.parse_args()
    Log.verbose = options.verbose
    check_only = options.check_only
    try:
        lock = LockFile("process_incoming")
    except LockFile.AlreadyLockedError:
        Log.log("Unable to acquire lock, exiting")
        return
    
    # Check and process the incoming directoy
    check_incoming_dir()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'User requested interrupt'
        sys.exit(1)

