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
#
# This file provides several functions to handle debian packaging files

import string

def get_files_list(source):
  file_list = list()
  f=open(source, 'r')
  infiles = 0
  for line in f.readlines():
    line = line.strip('\r\n')
    if infiles and len(line)<3: break
    if line[0:5]=="Files":
       infiles = 1
    elif infiles:
       if line[0] != ' ': continue
       parts = string.split(line)
       file_list.append(parts)
  f.close()
  return file_list

def revi(a, b):
  if not a: return b
  return revi(a[1:], a[0]+b)

def revertString(s):
  return revi(s, "")

def getOrigTarGzName(package):
  f=open(package, 'r')
  source = None
  version = None
  for line in f.readlines():
    line = line.strip('\r\n')
    if line[0:7]=="Source:":
      parts = string.split(line)
      source = parts[1]
    elif line[0:8]=="Version:":
      parts = string.split(line)
      parts = revertString(parts[1])
      parts = parts.split('-', 1)
      version = revertString(parts[1])
      break
  if version.find(":") != -1:
    epoch, version = version.split(":",1)
  f.close()
  return source+"_"+version+".orig.tar.gz"
  

 
