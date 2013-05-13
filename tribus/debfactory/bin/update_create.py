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

import sys
import os
import glob

if len(sys.argv) != 2:
  print "Usage: "+sys.argv[0]+" package.dsc"
  sys.exit(2)

package = sys.argv[1]

if not os.path.exists(package):
  print "Could not find "+package
  os.sys.exit(2)

def dsc_get_field(dsc_file, field):
  pgrep = os.popen('grep ^'+field+" "+dsc_file)
  pgrep_line = pgrep.readline().strip('\r\n')
  dummy, value = pgrep_line.split(":", 1)
  return value.strip(' ') 

package_name = dsc_get_field(package, "Source:")
package_version = dsc_get_field(package, "Version:")
if package_version.find(":") != -1:
  epoch, package_version = package_version.split(":",1)

# determine uploader from changes file
uploader = None
for file in glob.glob(package_name+'*_source.changes'):
  uploader = dsc_get_field(file, 'Changed-By:')
uploader, dummy = uploader.split('<', 1)
uploader = uploader.strip(' ')

print "Package name:", package_name
print "Package version:", package_version
print "Uploader:", uploader
base_version, extra = package_version.split("-",1)
new_base_version = raw_input('Release version ['+base_version+'] ')
if new_base_version: base_version = new_base_version
print "Release version:", base_version
print 'Please type the version changelog, end with "end"'
full_desc = []
desc = ""
while desc != "end":
  desc = raw_input()
  if desc != "end":
    full_desc.append(desc)
#print "Full Description:"
#print full_desc
update_file = package_name+"_"+package_version+".update"
print "Creating "+update_file
f = open(update_file, "w")
f.write(package_name+" "+package_version+" "+base_version+"\n")
f.write(uploader+"\n")
for line in full_desc:
  f.write(line+"\n")
f.close()
print "Done"
