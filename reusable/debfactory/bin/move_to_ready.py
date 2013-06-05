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
#    This script accepts a .dsc file as parameter
#    it will upload all the files listed on it to the abs ready queue

import sys
import os
import os.path
import string
import shutil
import datetime
import smtplib
import glob
import getpass
import dpkg

ready_dir = '/export/abs/ready/'

def uniq(alist):
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

if len(sys.argv) < 2:
  print "Usage: "+sys.argv[0]+" package.dsc"
  sys.exit(2)

package = sys.argv[1]

release = os.path.basename(os.getcwd())

if package.find('.dsc') == -1:
  print "You must provide a .dsc file"
  sys.exit(2)

if not os.path.exists(package):
  print "File "+package+" not found"
  sys.exit(3)

#base_dir = os.path.dirname(package) or '.'
package_name = os.path.basename(package)
package_name_orig = package_name
package_name = package_name.replace(".dsc", "")

file_list = list()

for file in glob.glob(package_name+'_*.changes'):
  for file2 in dpkg.get_files_list(file):
    file_list.append(file2[4])
  file_list.append(file)
  file_list.append(dpkg.getOrigTarGzName(file))

file_list = uniq(file_list)
print "Debian source control",package_name_orig,"contains",len(file_list),"file(s)"

#print package_name+" - Moving "+`len(file_list)`+" file(s)"
for file in file_list:
  if not os.path.exists(file):
	print "Unable to find",file
        sys.exit(4)
  print file
print "Moving files to", ready_dir+release

for file in file_list:
	shutil.move(file, ready_dir+release+"/"+file)

print "Done."
