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
import string
import shutil
import datetime
import smtplib
import glob
import dpkg
import time

build_dir=os.environ['HOME']+'/build'
logs_dir=os.environ['HOME']+'/abs/build_log'
#ready_dir=os.environ['HOME']+'/var/post_build'
ready_dir=os.environ['HOME']+'/abs/post_build'
logs_url='http://abs.getdeb.net/build_log'
ready_url='http://abs.getdeb.net/post_build'
prebuilddir = os.environ['HOME']+'/abs/pre_build'
gpg_ops = '--no-options --no-default-keyring --keyring '+os.environ['HOME']+'/debfactory/keyrings/uploaders.gpg '

os.putenv('LANG', 'C') # We use system commands reply check, use a reliable language

def uniq(alist):
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

def send_email(toaddrs, message):
    fromaddr = '"GetDeb Automated Builder" <autobuild@getdeb.net>'
    server = smtplib.SMTP('localhost')
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()

if len(sys.argv) != 3:
  print "Usage: "+sys.argv[0]+" release package"
  sys.exit(2)

release = sys.argv[1]
package = sys.argv[2]

build_dir+='-'
build_dir+=release

pgrep=os.popen('grep "Changed-By:" '+package,'r')
change_author_line=pgrep.readline().strip('\r\n')
pgrep.close()

dummy, change_author = change_author_line.split(":")
pcheck=os.popen('gpg '+gpg_ops+' --verify --logger-fd=1 '+package)
lines = pcheck.readlines()
sign_author = None
for line in lines:
  if line.find("gpg: Good signature from") != -1:
      dummy, sign_author, dummy = line.split('"')
rc=pcheck.close()
  
if not sign_author:
  print "Unable to determine key owner"
  sys.exit(2)

if not change_author:
  print "Unable to determine change author"
  sys.exit(2)

if rc != None:
  print "Failed security check"

print "Building", release ,package
file_list = dpkg.get_files_list(package)
pck_files = list()
dsc_file = None
orig_file = None
for file in file_list:
  if file[4].find('.dsc') != -1: dsc_file = file[4]
  if file[4].find('orig.tar.gz') != -1: orig_file = file[4]
  pck_files.append(file[4])
if not dsc_file:
  print "ERROR: Package without a .dsc file"
  sys.exit(2)
if not orig_file:
  orig_file = dpkg.getOrigTarGzName(package)
  if not os.path.exists(prebuilddir+"/"+release+"/"+orig_file):
    print "ERROR: Package without a .orig.tar.gz file"
    sys.exit(2)
  else:
    pck_files.append(orig_file)

base_dir = os.path.dirname(package)
pck_files.append(os.path.basename(package))
for file in pck_files:
  print "Copying", base_dir+"/"+file,"to", build_dir
  shutil.copyfile(base_dir+"/"+file, build_dir+"/"+file)
os.chdir(build_dir)
pck_basename=dsc_file.replace('.dsc','')
log_name=pck_basename+datetime.datetime.now().strftime("_%Y_%M_%d_%m_%s_i386.log")
log_name_i386=log_name
start_time=time.time()
rc_i386=os.system('sbuild -d '+release+' -c '+release+'.i386 -A '+dsc_file)
elapsed_time_i386=`int(time.time() - start_time)`
shutil.copyfile('current', logs_dir+'/'+log_name)
print "Saved log to", logs_dir+'/'+log_name
print "Time elapsed = ",elapsed_time_i386, "seconds"
if rc_i386 != 0:
   shutil.copyfile('current', package+'.failed')
else:
   log_name=pck_basename+datetime.datetime.now().strftime("_%Y_%M_%d_%m_%s_amd64.log")
   log_name_amd64=log_name
   start_time=time.time()
   rc_amd64=os.system('sbuild -d '+release+' -c '+release+'.amd64 '+dsc_file)
   elapsed_time_amd64=`int(time.time() - start_time)`
   print rc_amd64
   shutil.copyfile('current', logs_dir+'/'+log_name)
   print "Saved log to", logs_dir+'/'+log_name
   print "Time elapsed = ", elapsed_time_amd64, "seconds"


# We handle file handling here
if rc_i386 == 0:
  #  Move ready files
  move_list = list()
  changes = glob.glob(build_dir+'/'+pck_basename+'_*.changes')
  for file in changes:
     for con_file in dpkg.get_files_list(file):
       move_list.append(con_file[4])
     move_list.append(file)
     move_list.append(dpkg.getOrigTarGzName(file))
  move_list = uniq(move_list) # We need because of the duplicated .all files
  for file in move_list:
     print "Moving ", file,"to", ready_dir+'/'+release
     shutil.move(file, ready_dir+'/'+release)

  # Remove prebuild files
  for file in pck_files:
    os.unlink(base_dir+"/"+file)

if rc_i386 == 0:
  message = "Subject: Package Build Success - "+os.path.basename(package)
  message += "\n\nYour package was succesfully built for "+release+' (i386)\r\n'
  message += "Build log: "+logs_url+'/'+log_name_i386+"\r\n"
  message += "Build time: "+elapsed_time_i386+" seconds"
  if rc_amd64 == 0:
    message += "\r\n\r\nYour package was succesfully built for "+release+' (amd64)\r\n'
  else:
    message += "\r\n\r\nYour package failed to build for "+release+' (amd64)\r\n'
  message += "Build log: "+logs_url+'/'+log_name_amd64+"\r\n"
  message += "Build time: "+elapsed_time_amd64+" seconds"
else:
  message = "Subject: Package Build Failure - "+os.path.basename(package)
  message += "\n\nYour package failed to build for "+release+' (i386)\r\n'
  message += "Build log: "+logs_url+'/'+log_name_i386+"\r\n"
  message += "Build time: "+elapsed_time_i386+" seconds"

if rc_i386 == 0:
  message += "\r\n\r\nFiles are available for verification at:\r\n"
  message += ready_url+'/'+release

send_email(change_author, message)

