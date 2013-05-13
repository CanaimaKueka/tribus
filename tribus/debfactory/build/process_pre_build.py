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

  When a *_source.changes is found, it's contents are verified, files
  are copied to /tmp/release-build and sbuild is called to build the
  package.
  
  The build result is sent via email to the sign author.
  A lock file is used to prevent concurrent runs
  
"""
import os
import sys
import time
import datetime
import glob
import commands
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
check_config(config, ['sender_email', 'base_url'])

Log = Logger()

def check_pre_build_dir():
    """
    Check the pre build directory for release directories
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
    Check a release/component directory
    	*_source.changes will triger a verification/build action
    """
    global options
    Log.log("Checking %s/%s" % (release, component))
    file_list = glob.glob("%s/%s/%s/*_source.changes" \
        % (options.input_dir, release, component))

    for fname in file_list:
        check_source_changes(release, component \
            , os.path.basename(fname))

    Log.log("Done")

def check_source_changes(release, component, filename):
    """
    Check a _source.changes file and proceed as described in the script
    action flow . 
    """
    global config, options
    Log.print_("Building %s/%s/%s" % (release, component, filename))

    source_dir = "%s/%s/%s" \
        % (options.input_dir, release, component)
    destination_dir = "/tmp/build-%s-%s" % (release, component)    
    changes_file = "%s/%s" % (source_dir, filename)

    # Remove previous failed status
    if os.path.exists('%s.failed' % changes_file):
        os.unlink('%s.failed' % changes_file)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, 0755)

    control_file = DebianControlFile(changes_file)
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

    report_title = "%s/%s/%s build FAILED\n" \
        % (release, component, filename)

    try:
        control_file.copy(destination_dir)
    except DebianControlFile.MD5Error, e:
        report_msg = "MD5 mismatch: Expected %s, got %s, file: %s\n" \
            % (e.expected_md5, e.found_md5, e.name)
        Log.print_(report_msg)
	control_file.remove()
        send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)
        return
    except DebianControlFile.FileNotFoundError, e:
        report_msg = "File not found: %s\n" % (e.filename)
        Log.print_(report_msg)
	control_file.remove()
        send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)
        return
    dsc_file = "%s/%s_%s.dsc" \
        % (destination_dir, control_file['Source'] \
        , control_file.version())
    if not os.path.exists(dsc_file):
        report_msg = ".dsc file not found: %s\n" % (dsc_file)
        Log.print_(report_msg)
	control_file.remove()
        send_mail(config['sender_email'], gpg_sign_author, report_title, report_msg)
        return

    full_post_build_dir = "%s/%s/%s" % (options.output_dir,  release \
        , component)
    if not os.path.exists(full_post_build_dir):
        os.makedirs(full_post_build_dir, 0755)

    version = control_file.version()
    os.chdir(destination_dir)
    i386_rc = sbuild_package(release, component, control_file, 'i386')
    if i386_rc == 0:
        sbuild_package(release, component, control_file, 'amd64')

        # Only move the source to post_build after building something
        control_file.move(full_post_build_dir)
    else:
        control_file.remove()

def sbuild_package(release, component, control_file, arch):
    """Attempt to build package using sbuild """
    global config, options
    target_email = control_file['Changed-By']
    name_version = "%s_%s" % (control_file['Source']
        , control_file.version())
    dsc_file = "%s.dsc" % name_version
    dsc_controlfile = DebianControlFile(dsc_file)
    destination_dir = "%s/%s/%s" % (options.output_dir,  release,  component)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, 0755)
    print "Building: %s" % dsc_file
    log_name = "%s_%s_%s.log" % (name_version \
        , datetime.datetime.now().strftime("%Y_%m_%d_%M_%S"), arch)
    start_time = time.time()
    if arch == "i386":
        arch_str = "i386 -A"
        arch_list = ['i386','all']
    else:
        arch_str = arch
        arch_list = ['amd64']
        if dsc_controlfile['Architecture'] == 'all':
            print "Skipping Architecture= 'all' "
            return 0
    rc = os.system('sbuild -d %s -c %s-%s %s' % 
        (release, release, arch_str, dsc_file))
    log_link = "%s_%s.build" % (name_version, arch)
    if not os.path.exists(log_link):
        print "Unable to find build log symbolic link"
        return -1 
    try:
        log_filename = os.readlink(log_link)
    except OSError:
        print "Unable to find build log symbolic link"
        return -1
    elapsed_time = `int(time.time() - start_time)`
    (dummy, build_tail) = commands.getstatusoutput('tail -2 ' + log_filename)
    report_msg = "List of files:\n"
    report_msg += "--------------\n"
    if rc == 0:
        status = "SUCCESSFUL"
        for arch_str in arch_list:
            # We really need the "./" because we have no base dir
            arch_changes = "./%s_%s.changes" % (name_version,  arch_str)
            report_title = "Build for %s/%s/%s (%s) %s\n" \
                % (release, component, name_version, arch, "FAILED")
            if os.path.exists(arch_changes):
                changes_file = DebianControlFile(arch_changes)
                file_list = changes_file.files_list()
                for file_info in file_list:
                    report_msg += "%s (%s) MD5: %s \n" \
                        % (file_info.name, file_info.size, file_info.md5sum)
                    (dummy, lintian_output) = commands.getstatusoutput('lintian -i -I -E --pedantic ./%s' % (file_info.name))
                    report_msg += "Lintian output:\n%s\n\n" % (unicode(lintian_output, 'utf-8'))
                try:
                    changes_file.move(destination_dir)
                except DebianControlFile.MD5Error,e:
                    report_msg = "MD5 mismatch: Expected %s, got %s, file: %s\n" \
                        % (e.expected_md5, e.found_md5, e.name)
                    Log.print_(report_msg)
                    send_mail(config['sender_email'], target_email, report_title, report_msg)
                    return
                except DebianControlFile.FileNotFoundError, e:
                    report_msg = "File not found: %s" % (e.filename)
                    Log.print_(report_msg)
                    send_mail(config['sender_email'], target_email, report_title, report_msg)
                    return
                finally:
                    changes_file.remove()
    else:
        status = "FAILED"
    report_title = "Build for %s/%s/%s (%s) %s\n" \
        % (release, component, name_version, arch, status)
    report_msg += '\n' + build_tail + '\n'
    report_msg += "Log file: %s%s\n" % (config['base_url'], log_filename)
    Log.print_(report_title)
    send_mail(config['sender_email'], target_email.decode('utf-8'), report_title, report_msg)
    return rc

def main():
    global options
    parser = OptionParser()
    parser.add_option("-g", "--skip-gpg-check",
        action="store_true", dest="skip_gpg", default=False,
        help="Check only, don't move packages")
    parser.add_option("-q", "--quiet",
        action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")
    parser.add_option("-i", "--input-dir",
        action="store", dest="input_dir", default='/build/pre_build',
        help="Input directory that will contain the *_source.changes files")
    parser.add_option("-o", "--output-dir",
        action="store", dest="output_dir", default='/build/post_build',
        help="Output directory")            
        
    (options, args) = parser.parse_args()
    Log.verbose=options.verbose
    try:
        lock = LockFile("build")
    except LockFile.AlreadyLockedError:
        Log.log("Unable to acquire lock, exiting")
        return

    # Check and process the incoming directoy
    check_pre_build_dir()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'User requested interrupt'
        sys.exit(1)

