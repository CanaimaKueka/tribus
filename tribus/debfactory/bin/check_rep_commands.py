#!/usr/bin/python
#
#  (C) Copyright 2009, GetDeb Team - https://launchpad.net/~getdeb
#  --------------------------------------------------------------------
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  --------------------------------------------------------------------
"""
  This script will check the rep_commands directory
  It will call a reprepro command and email the output to the command
  requestor. Commands are files with the following format:
  email remove codename source-package version
	will do a reprepro removesrc
  email copy destination-codename source-codename source-package version
	will do a reprepro copysrc
"""
import os
import sys
import time
import glob
import commands
from optparse import OptionParser
from configobj import ConfigObj

from os.path import join, dirname, exists, realpath, abspath
LAUNCH_DIR = abspath(sys.path[0])
LIB_DIR = join(LAUNCH_DIR, '..', 'lib')
sys.path.insert(0, LIB_DIR)

from log import Logger
from mail import send_mail_message
from lockfile import LockFile

config_file = "%s/debfactory/etc/debfactory.conf" % os.environ['HOME']
config = ConfigObj(config_file)

# Load configuration
try:
	archive_admin_email = config['archive_admin_email']	
	rep_commands_dir = config['rep_commands_dir']
except Exception:
	print "Configuration error"
	print `sys.exc_info()[1]`
	sys.exit(3)

Log = Logger()	

def check_command(filename):
	"""
	Check a release directory for components
	"""
	
	Log.print_("Found %s" % filename)
	f = open(filename, 'r')
	failed = False
	email = None
	for cmdline in f.readlines():
		fields = cmdline.split(' ')
		if len(fields) < 3:
			failed = True
			Log.log("Invalid, < 3 fields")
			continue
		email = fields[0]
		action = fields[1]
		if action == "remove":
			if len(fields) != 5:
				failed = True
				Log.log("Invalid, remove action != 5 fields")
				break
			codename = fields[2]
			source_package = fields[3]
			version = fields[4]
			command = "reprepro removesrc %s %s %s " \
				% (codename,  source_package, version)

			if source_package.startswith('lib'):
				prefix = source_package[:4]
			else:
				prefix = source_package[0]

			components = ["apps", "games"]
			for component in components:
				pool_dir = join(config['pool_dir'], 'pool', \
						component, prefix, source_package)
				changelogs = glob.glob("%s/*.changelog" % (pool_dir))
				for changelog in changelogs:
					deb = changelog.rsplit('.', 1)[0]+'.deb'
					if not os.path.exists(deb):
						os.unlink(changelog)

		elif action == "copy":
			if len(fields) != 6:
				failed = True
				Log.log("Invalid, copy action != 6 fields")
				break
			destination_codename = fields[2]
			source_codename = fields[3]
			source_package = fields[4]
			version = fields[5]
			command = "reprepro copysrc %s %s %s %s " \
				% (destination_codename, source_codename \
					, source_package, version)
			# email copy destination-codename source-codename source-package version	
		else: # action was not valid
			continue
		# Execute and send mail
		print command
		(rc, output) = commands.getstatusoutput(command)	
		print output
		report_title = "REPOS ACTION: %s" % ' '.join(fields[1:])
		report_msg = "ACTION: %s\n" % cmdline
		report_msg += "FILE: %s\n\n" % filename				
		report_msg += "Command output:\n"+output+"\n\n"
		report_msg += "Return code: %d\n" % rc
		target_emails = archive_admin_email.split(",")
		target_emails.append(email)
		send_mail_message(target_emails, report_title, report_msg)		
	if failed:
		shutil.move(filename, "%s.failed" % filename)
	else:
		os.unlink(filename)
		
def check_rep_commands_dir(rep_commands_dir):
	""" 
	Check a release/component directory
	"""
	Log.log("Checking rep_commands")
	file_list = glob.glob("%s/*" % rep_commands_dir)
		
	for fname in file_list:
		if not fname.endswith(".failed"):
			check_command(fname)
									
	Log.log("Done")
	
def main():
	
	parser = OptionParser()
	parser.add_option("-q", "--quiet",
		action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")
	(options, args) = parser.parse_args()
	Log.verbose=options.verbose	
	try:
		lock = LockFile("check_rep_incoming")
	except LockFile.AlreadyLockedError:
		Log.log("Unable to acquire lock, exiting")
		return
	
	# Check and process the incoming directoy
	check_rep_commands_dir(rep_commands_dir)
	
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'User requested interrupt'
		sys.exit(1)

