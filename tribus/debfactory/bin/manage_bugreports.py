#!/usr/bin/python
#
#    (C) Copyright 2009, GetDeb Team - https://launchpad.net/~getdeb
#    --------------------------------------------------------------------
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    --------------------------------------------------------------------

# To setup the LP API Access you have to launch this:
#import os
#import sys
#home = os.environ['HOME']
#cachedir = home + '/.launchpadlib/cache/'
#from launchpadlib.launchpad import Launchpad, EDGE_SERVICE_ROOT
#launchpad = Launchpad.get_token_and_login('GetDeb.net Bug Manager', EDGE_SERVICE_ROOT, cachedir)
#launchpad.credentials.save(file("some-file.txt", "w"))

import os
import sys
import re
from launchpadlib.launchpad import Launchpad, EDGE_SERVICE_ROOT
from launchpadlib.credentials import Credentials

def get_changelog(i, filename):
	changelog = file(filename, "r")
	current_changelog = 0
	changelog_dict = {'package' : '', 'version' : '', 'release' : '', 'bugs_to_be_closed' : [], 'changelog_entry' : ''}

	for line in changelog.readlines():
		line = line.strip('\r\n')
		if not line:
			if current_changelog == i:
				changelog_dict['changelog_entry'] += '\n'
			continue
		if not line.startswith(' '):
			current_changelog += 1
			if current_changelog == i:
				parts = line.split()
				changelog_dict['changelog_entry'] += line + '\n'
				changelog_dict['package'] = parts[0]
				changelog_dict['version'] = parts[1].strip('()')
				changelog_dict['release'] = parts[2].strip(';')
		if current_changelog > i:
			break
		if line.startswith('  ') and current_changelog == i:
			changelog_dict['changelog_entry'] += line + '\n'
		if line.startswith(' -- ') and current_changelog == i:
			changelog_dict['changelog_entry'] += line + '\n'

	line_matches = re.finditer('\(LP:\s*(?P<buglist>.+?\))', changelog_dict['changelog_entry'], re.DOTALL)
	for line_match in line_matches:
		bug_matches = re.finditer('#(?P<bugnum>\d+)', line_match.group('buglist'))
		for bug_match in bug_matches:
			bugnum = bug_match.group('bugnum')
			if not bugnum in changelog_dict['bugs_to_be_closed']:
				changelog_dict['bugs_to_be_closed'].append(bugnum)

	return changelog_dict

def check_not_empty(bugs):
	if len(bugs) == 0:
		print "No bugs found to fix"
		sys.exit(3)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: "+sys.argv[0]+" s[tart] | b[uild] | t[ested] [jaunty|hardy].[amd64|i386] | r[eleased] | i[nvalid]"
		sys.exit(1)

	changelog = 'debian/changelog'

	if not os.path.exists(changelog):
		print "File "+changelog+" not found"
		sys.exit(2)

	home = os.environ['HOME']
	cachedir = home + '/.launchpadlib/cache/'

	launchpad_key = home + "/.launchpadlib/key.txt"

	credentials = Credentials()
	credentials.load(open(launchpad_key))
	#launchpad = Launchpad(credentials, EDGE_SERVICE_ROOT, cachedir)
	launchpad = Launchpad.login_with('GetDeb.net Bug Manager', 'production')

	me = launchpad.me

	project_name = "GetDeb Software Portal"

	if sys.argv[1] == 'start' or sys.argv[1].startswith('s'):
		current_changelog = get_changelog(1, changelog)
		previous_changelog = get_changelog(2, changelog)

		bug_ids = current_changelog['bugs_to_be_closed']
		check_not_empty(bug_ids)

		for bug_id in bug_ids:
			bug = launchpad.bugs[bug_id]
			bug_title = bug.title
			subject_text = "Re: " + bug_title

			wrote_task = False

			for task in bug.bug_tasks:
				if task.bug_target_display_name == project_name:
					task.importance="Medium"
					task.status="In Progress"
					task.assignee=me
					task.lp_save()
					wrote_task = True

			if wrote_task:
				if previous_changelog['version'] == '':
					bug.newMessage(content="Starting from scratch.", \
					 subject=subject_text)
				else:
					bug.newMessage(content="Taking " + previous_changelog['package'] \
					 + " " + previous_changelog['version'] + " as starting point.", \
					 subject=subject_text)
				bug.lp_save()
				print 'Bug "' + bug_title + '" has been changed.'
			else:
				print 'No task for "' + project_name + '" has been found in bug "' + bug_title + '".'
	elif sys.argv[1] == 'build' or sys.argv[1].startswith('b'):
		current_changelog = get_changelog(1, changelog)
		bug_ids = current_changelog['bugs_to_be_closed']
		check_not_empty(bug_ids)

		for bug_id in bug_ids:
			bug = launchpad.bugs[bug_id]
			bug_title = bug.title
			subject_text = "Re: " + bug_title

			wrote_task = False

			for task in bug.bug_tasks:
				if task.bug_target_display_name == project_name:
					task.status="Fix Committed"
					task.lp_save()
					wrote_task = True

			if wrote_task:
				bug.newMessage(content="Package has been built for " + current_changelog['release'] + ".", \
				  subject=subject_text)
				bug.lp_save()
				print 'Bug "' + bug_title + '" has been changed.'
			else:
				print 'No task for "' + project_name + '" has been found in bug "' + bug_title + '".'
	elif sys.argv[1] == 'tested' or sys.argv[1].startswith('t'):
		if len(sys.argv) < 3:
			print "The release the package has been tested for is missing."
			sys.exit(4)

		current_changelog = get_changelog(1, changelog)
		bug_ids = current_changelog['bugs_to_be_closed']
		check_not_empty(bug_ids)

		for bug_id in bug_ids:
			bug = launchpad.bugs[bug_id]
			bug_title = bug.title
			has_task = False

			for task in bug.bug_tasks:
				if task.bug_target_display_name == project_name:
					has_task = True

			if has_task:
				tags = bug.tags
				tags.append('tested-' + sys.argv[2])
				bug.tags = tags
				bug.lp_save()
				print 'Bug "' + bug_title + '" has been changed.'
			else:
				print 'No task for "' + project_name + '" has been found in bug "' + bug_title + '".'
	elif sys.argv[1] == 'released' or sys.argv[1].startswith('r'):
		current_changelog = get_changelog(1, changelog)
		bug_ids = current_changelog['bugs_to_be_closed']
		check_not_empty(bug_ids)

		for bug_id in bug_ids:
			bug = launchpad.bugs[bug_id]
			bug_title = bug.title
			subject_text = "Re: " + bug_title
			wrote_task = False

			for task in bug.bug_tasks:
				if task.bug_target_display_name == project_name:
					task.status="Fix Released"
					task.lp_save()
					wrote_task = True

			if wrote_task:
				bug.newMessage(content="Published.\n\nThanks.\n\n\n" + \
				 "---------------\n" + \
				 current_changelog['changelog_entry'].strip('\r\n'), \
				 subject=subject_text)
				bug.lp_save()
				print 'Bug "' + bug_title + '" has been changed.'
			else:
				print 'No task for "' + project_name + '" has been found in bug "' + bug_title + '".'
	elif sys.argv[1] == 'invalid' or sys.argv[1].startswith('i'):
		current_changelog = get_changelog(1, changelog)
		bug_ids = current_changelog['bugs_to_be_closed']
		check_not_empty(bug_ids)

		for bug_id in bug_ids:
			bug = launchpad.bugs[bug_id]
			bug_title = bug.title
			subject_text = "Re: " + bug_title
			wrote_task = False

			for task in bug.bug_tasks:
				if task.bug_target_display_name == project_name:
					task.status="Invalid"
					task.lp_save()
					wrote_task = True

			if wrote_task:
				print 'Please type the comment, end with "end"'
				full_desc = []
				desc = ""
				while desc != "end":
					desc = raw_input()
					if desc != "end":
						full_desc.append(desc)
				comment = ""
				for line in full_desc:
					comment += line + "\n"
				bug.newMessage(content=comment, subject=subject_text)
				bug.lp_save()
				print 'Bug "' + bug_title + '" has been changed.'
			else:
				print 'No task for "' + project_name + '" has been found in bug "' + bug_title + '".'
