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

import os
import sys

def getSourceFiles():
  find = os.popen("find . -name '*.h' -or -name '*.c' -or -name '*.cpp' -or -name '*.hpp' -or -name '*.cc'")
  files = find.readlines()
  stripped_files = list()
  for file in files:
    stripped_files.append(file.strip("\n"))
  return stripped_files

def getUniqHeadersInFiles(files):
  header_list = list()
  file_header_list = list()
  for file in files:
    f = open(file, 'r')
    for line in f.readlines():
      if line[0:8]=="#include" or line.startswith("# include"):
        if line.find("<") != -1 and line.find(">") != -1 and line[9] != '"':
          dummy, header = line.split("<", 1)
          header, dummy = header.split(">", 1)
          header = header.strip()
          if not header in header_list and header != "":
            header_list.append(header)
            file_header_list.append((file,header))
    f.close()
  return file_header_list

def removeSkipHeaders(headers):
  newHeaders = list()
  skip = ["iostream", "string", "vector", "algorithm", "map", "fstream", "sstream", "new", "memory", "cstring", "string.h", "stdint.h", "assert.h", "math.h", "cmath", "cfloat", "cstdlib", "stdlib.h", "stdio.h", "climits", "execinfo.h", "signal.h", "exception", "pthread.h", "sys/ipc.h", "sys/shm.h", "unistd.h", "stddef.h", "pc.h", "limits.h", "config.h", "ctype.h", "fcntl.h", "sys/ioctl.h", "time.h", "linux/fb.h", "sys/mman.h", "sys/time.h"]
  for header in headers:
    if not header[1] in skip:
      newHeaders.append(header)
  return newHeaders

def isInStdLib(dev_lines):
  std_lib_found = 0
  for line in dev_lines:
    if line.find("libc6-dev") <> -1:
      std_lib_found = 1
  return std_lib_found

def getDevPackages(header):
  aptFile = os.popen("apt-file find "+header)
  files = aptFile.readlines()
  stripped_files = list()
  for file in files:
    stripped_file = file.strip("\r\n")
    dev, dummy = stripped_file.split(":", 1)
    dev = dev.strip()
    alreadyIn = False
    for curStripped_file in stripped_files:
      if curStripped_file.find(dev) <> -1:
        alreadyIn = True
    if not alreadyIn:
      stripped_files.append(stripped_file)
  return stripped_files

def printDevs(devs, dev_list):
  ret = -1
  for i in range(len(devs)):
    line = devs[i]
    
    dev, dummy = line.split(":", 1)
    dev = dev.strip()
    
    if dev in dev_list:
      print "\033[1;31m" + str(i) + ": " + line + "\033[0;m"
      ret = i
    else:
      print str(i) + ": " + line
  return ret

def chooseDevPackage(devs, current, nMax, defaultSelection):
  if defaultSelection == -1:
    chosenDev = raw_input('['+str(current)+'/'+str(nMax)+'] Choose the right dev Package [0:'+str(len(devs)-1)+'] or press [enter] to skip: ')
    if chosenDev == "": return None
    dev = devs[int(chosenDev)]
    dev, dummy = dev.split(":", 1)
    dev = dev.strip()
    return dev
  
  chosenDev = raw_input('['+str(current)+'/'+str(nMax)+'] Choose the right dev Package [0:'+str(len(devs)-1)+'] or press [enter] for default '+ str(defaultSelection) +': ')
  if chosenDev == "":  chosenDev = defaultSelection
  dev = devs[int(chosenDev)]
  dev, dummy = dev.split(":", 1)
  dev = dev.strip()
  return dev

def buildDepends(dev_list):
  builddeps = "Build-Depends: debhelper (>=6),"
  for i in range(len(dev_list)):
    builddeps+=" " + dev_list[i]

    if i < len(dev_list)-1:
      builddeps+=","

  print "\n\n\n"
  print builddeps

def findUselessHeaders(dev, header_list):
  aptFile = os.popen("apt-file list "  + dev + " | cut -d\  -f2")
  headers = aptFile.readlines()
  useless_header_list = list()
  for header in headers:
    for found_header in header_list:
      if header.find(found_header + '\n') <> -1:
        useless_header_list.append(found_header)
  return useless_header_list

if __name__=="__main__":
  dev_list = list()
  files = getSourceFiles()
  file_header_list = getUniqHeadersInFiles(files)
  useless_header_list = list()
  usually_installed_headers = ['map', 'algorithm', 'string', 'vector', 'memory', \
    'iostream', 'time.h', 'sys/time.h', 'list', 'stdarg.h', 'ctime', 'set', 'cstring', \
    'stdlib.h', 'stddef.h', 'limits', 'numeric', 'queue', 'sys/stat.h', 'sys/types.h', \
    'memory.h', 'assert.h', 'new', 'float.h', 'cstdarg', 'stdexcept', 'typeinfo', \
    'deque', 'exception', 'cassert', 'cstdlib', 'stack', 'sys/param.h', 'dirent.h', \
    'unistd.h', 'fnmatch.h', 'ctype.h', 'limits.h']
#  file_header_list = removeSkipHeaders(file_header_list)
  existing_headers = list()

  print "Found "+str(len(file_header_list))+" unique headers."

  numHeaders = len(file_header_list)
  i = 1

  for file_header in file_header_list:
    print
    dummy, header = file_header
    if header in useless_header_list:
      print 'Skipped header "' + header + '" already which already is in a dev package'
      i += 1
      continue

    if file_header[1] in usually_installed_headers:
      print 'Skip usual header'
      i += 1
      continue

    devs = getDevPackages(file_header[1])

    if len(devs) == 0:
      print "Warning: no dev package for header '" + file_header[1] + "' in file '" + file_header[0] + "' found!"
      #con = raw_input('Continue (y/n)? ')
      #if con=="n":
      #  sys.exit()
    else:
      if not isInStdLib(devs):
        file_header_devs = (file_header[0], file_header[1], devs)
        existing_headers.append(file_header_devs)
      else:
        print "Header " + file_header[1] + " is in standard lib"

    i = i + 1

  numHeaders = len(existing_headers)
  i = 1

  for file_header_devs in existing_headers:
    file_header = (file_header_devs[0], file_header_devs[1])
    devs = file_header_devs[2]

    print
    dummy, header = file_header
    if header in useless_header_list:
      print 'Skipped header "' + header + '" already which already is in a dev package'
      i += 1
      continue

    defaultSelection = printDevs(devs, dev_list)
    print file_header[0],file_header[1]
    chosenDev = chooseDevPackage(devs, i, numHeaders, defaultSelection)
    if chosenDev != None and not chosenDev in dev_list:
      dev_list.append(chosenDev)
      useless_header_list.extend(findUselessHeaders(chosenDev, [header for (dummy, header) in file_header_list]))

    i = i + 1

  buildDepends(dev_list)
