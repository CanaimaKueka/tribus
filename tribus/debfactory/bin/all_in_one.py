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
import shutil

absDir="/export/abs"

def askToContinue():
  con = raw_input('Continue (y/n)? ')
  if con=="n":
    sys.exit()

def printChangeLog(dsc):
  source = dsc.replace(".dsc", "_source.changes")
  f=open(source, 'r')
  inchanges = 0
  counter = 0
  for line in f.readlines():
    line = line.strip('\r\n')
    if inchanges and line[0]!=" ": break
    if line[0:8]=="Changes:":
       inchanges = 1
    elif inchanges:
       if counter < 2:
         counter = counter + 1
       else:
         print line
  f.close()

def callCreateUpdate(dsc):
  os.system('update_create.py ' + dsc)

def getUpdateFile(dsc):
  update = dsc.replace(".dsc", ".update")
  return update

def getUpdateDir():
  release = os.path.basename(os.getcwd())
  return absDir+"/updates/"+release

def moveUpdate(update):
  updateDir=getUpdateDir()
  shutil.move(update, updateDir)

def callMoveToReady(dsc):
  os.system('move_to_ready.py ' + dsc)
  

if __name__=="__main__":
  if len(sys.argv) != 2:
    print "Usage: "+sys.argv[0]+" dsc"
    sys.exit(2)

  dsc = sys.argv[1]

  printChangeLog(dsc)
  askToContinue()
  callCreateUpdate(dsc)
  print ".update file created. Move to updates directory?"
  askToContinue()
  moveUpdate(getUpdateFile(dsc))
  print ".update file moved. run move_to_ready?"
  askToContinue()
  callMoveToReady(dsc)
