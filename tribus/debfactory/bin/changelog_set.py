#!/usr/bin/env python
import os, sys, re
import time, string

"""
Get the latest version from debian/changelog
"""
def changelog_current_version():
    changelog = open('debian/changelog','r')
    data = changelog.readline()
    p = re.compile("(\S+) \((.*)\)")
    info = p.search(data)
    currversion = info.group(2)
    verlist = string.split(currversion, ':')
    if len(verlist) == 2:
        currversion= verlist[1]
    changelog.close()
    return currversion

"""
Get the latest packagename from debian/changelog
"""
def changelog_current_package():
    changelog = open('debian/changelog','r')
    data = changelog.readline()
    p = re.compile("(\S+) \((.*)\)")
    info = p.search(data)
    currversion = info.group(1)
    changelog.close()
    return currversion



if not os.path.exists('debian/changelog'):
  print "debian/changelog not found!";
  sys.exit(2)

currversion = changelog_current_version()
currpackage = changelog_current_package()

fin = open('debian/changelog','r')
fout = open('debian/changelog.new','w')
curr = fin.readline()

print "Current : "+currpackage+" "+currversion

p = re.compile("(\S+)-([0-9].*)")
curr = os.path.basename(os.getcwd())
info = p.search(curr)
package=info.group(1)
version=info.group(2)
release = os.popen('lsb_release -c| cut -f2').read().strip("\r\n")
newversion = version+"-1~getdeb1"

## Create changelog entry
author = os.environ.get('DEBFULLNAME')
if not author:
  print "DEBFULLNAME environment variable must be defined!"
  sys.exit(2)

email = os.environ.get('DEBEMAIL')
if not email:
  print "DEBEMAIL environment variable must be defined!"  
  sys.exit(2)

print "New     : "+package+" "+newversion
if currversion == newversion:
  print "Same version, not adding!"
  fout.close()
  os.unlink('debian/changelog.new');
  sys.exit(2)

# Create new header
ts=time.strftime("%a, %d %b %Y %T", time.localtime())
sign=" -- "+author+" <"+email+">  "+ts+" +0000"
fout.write(package+" ("+newversion+") "+release+"; urgency=low\n\n")
fout.write("  * New upstream version\n\n"+sign+"\n\n")
fout.close()
fin.close()
os.system('cat debian/changelog.new debian/changelog > debian/changelog.new.new')
os.unlink('debian/changelog.new');
os.unlink('debian/changelog');
os.rename("debian/changelog.new.new", "debian/changelog")
