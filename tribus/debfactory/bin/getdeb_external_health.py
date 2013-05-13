#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  (C) Copyright 2010, GetDeb Team - https://launchpad.net/~getdeb
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
#
#  This file provides several functions to handle debian packages
#  control files.
import sys
import os
import re
import time
import random
import operator
import cgi
from threading import Thread
from xml.dom import minidom

data = []
archiveUrl = ""
nowatch = []
warning = []
uptodate = []
needsupdate = []

class testit(Thread):
	def __init__ (self,source):
		Thread.__init__(self)
		self._source = source
	def exe(self, command):
		#print command
		os.system(command)
	def run(self):
		global archiveUrl, nowatch, warning, uptodate, needsupdate
		self._source["Warning"] = []

		rand = random.randint(0,9999999)
		directory = self._source["Package"] + str(rand)
		diff = "/tmp/"+directory+"/bla.diff.gz"
		# Always name the file debian.tar.gz (Although it may be a debian.tar.bz2)
		debianTarGz = "/tmp/"+directory+"/"+directory+"/debian.tar.gz"
		xmlfile = "/tmp/"+directory+"/dehs.xml"

		self.exe("cd /tmp ; rm -rf "+directory)

		self.exe("cd /tmp ; mkdir "+directory)
		if self._source["patch"][1].endswith("diff.gz"):
			self.exe("cd /tmp/"+directory+" ; wget -q -O "+diff+" "+archiveUrl+self._source["Directory"]+"/"+self._source["patch"][1])
			p = os.popen("cd /tmp/"+directory+" ; lsdiff -z "+diff+" | grep debian/watch")
			watch = p.readline().strip('\r\n')
			p.close()
			if watch == "":
				#print "No debian/watch file found. Skipping."
				#print
				nowatch.append(self._source)
				self.exe("cd /tmp/ ; rm -rf "+directory)
				return

			self.exe("cd /tmp/"+directory+" ; mkdir "+directory)
			self.exe("cd /tmp/"+directory+"/"+directory+" ; filterdiff -z -i\"*/debian/*\" "+diff+" | patch -f -s -p1 2>&1 > /dev/null")
		else:
			if self._source["patch"][1].endswith("debian.tar.bz2"):
				extractFlag = 'j'
			else:
				extractFlag = 'z'
			self.exe("cd /tmp/"+directory+" ; mkdir "+directory)
			self.exe("cd /tmp/"+directory+"/"+directory+" ; wget -q -O "+debianTarGz+" "+archiveUrl+self._source["Directory"]+"/"+self._source["patch"][1] + " ; tar x"+extractFlag+"f " + debianTarGz)
			p = os.popen("cd /tmp/"+directory+"/"+directory+" ; ls debian/watch 2>/dev/null")
			watch = p.readline().strip('\r\n')
			p.close()
			if watch == "":
				#print "No debian/watch file found. Skipping."
				#print
				nowatch.append(self._source)
				self.exe("cd /tmp/ ; rm -rf "+directory)
				return
		p = os.popen("cd /tmp/"+directory+"/"+directory+" ; uscan --report-status --dehs > "+xmlfile)
		p.close()

		xmldoc = minidom.parse(xmlfile)

		testAdded = False

		if len(xmldoc.firstChild.childNodes) == 1:
			self._source["Warning"].append("Unknown warning. Uscan reports nothing.")
		else:
			for entry in xmldoc.firstChild.childNodes:
				if entry.nodeName == "status":
					status = entry.firstChild.data
					self._source["Status"] = status
					if status == "Newer version available":
						needsupdate.append(self._source)
						testAdded = True
					elif status == "up to date":
						uptodate.append(self._source)
						testAdded = True
					else:
						self._source["Warning"].append("Unknown status: %s" % status)
				if entry.nodeName == "debian-uversion":
					self._source["DebianUVersion"] = entry.firstChild.data
				if entry.nodeName == "debian-mangled-uversion":
					self._source["DebianMangledUVersion"] = entry.firstChild.data
				if entry.nodeName == "upstream-version":
					self._source["UpstreamVersion"] = entry.firstChild.data
				if entry.nodeName == "upstream-url":
					self._source["UpstreamURL"] = entry.firstChild.data
				if entry.nodeName == "warnings":
					self._source["Warning"].append(entry.firstChild.data)

		if len(self._source["Warning"]) > 0:
			warning.append(self._source)
			testAdded = True

		if not testAdded:
			print self._source["Package"]
			os.system("cat " + xmlfile)

		self.exe("cd /tmp ; rm -rf "+directory)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Usage: "+sys.argv[0]+" <archiveUrl> <Sources.gz>"
		print "Example: "+sys.argv[0]+" \"http://archive.getdeb.net/getdeb/ubuntu/\""+ \
		      " \"http://archive.getdeb.net/getdeb/ubuntu/dists/karmic-getdeb/apps/source/Sources.gz\""
		sys.exit(1)

	archiveUrl = sys.argv[1]
	sources = sys.argv[2]
	numberOfThreads = 7
	threads = []

	os.chdir("/tmp")
	if os.path.isfile("/tmp/Sources.gz"): os.remove("/tmp/Sources.gz")
	if os.path.isfile("/tmp/Sources"): os.remove("/tmp/Sources")
	os.system("wget -q "+sources+" > /dev/null")
	os.system("gunzip -d Sources.gz")

	source = {}
	infiles = False

	sources = open("Sources", "r")
	for line in sources.readlines():
		line = line.strip("\n\r")
		if line == "":
			data.append(source)
			infiles = False
			source = {}
		if line.startswith("Package:"):
			source["Package"] = line.split(" ")[1]
		if line.startswith("Version:"):
			source["Version"] = line.split(" ")[1]
		if line.startswith("Directory:"):
			source["Directory"] = line.split(" ")[1]
		if line.startswith("Files:"):
			infiles = True
			continue
		if line.startswith(" ") and infiles:
			parts = line.split(" ")
			md5sum = parts[1]
			filename = parts[3]
			if filename.endswith("tar.gz"): source["tar.gz"] = (md5sum, filename)
			if filename.endswith("diff.gz"): source["patch"] = (md5sum, filename)
			if filename.endswith("debian.tar.gz"): source["patch"] = (md5sum, filename)
			if filename.endswith("debian.tar.bz2"): source["patch"] = (md5sum, filename)
			if filename.endswith("dsc"): source["dsc"] = (md5sum, filename)
		if infiles and line.find(":") != -1: infiles = False

	sources.close()

	if os.path.isfile("/tmp/Sources.gz"): os.remove("/tmp/Sources.gz")
	if os.path.isfile("/tmp/Sources"): os.remove("/tmp/Sources")

	for source in data:
		if len(threads) < numberOfThreads:
			thread = testit(source)
			thread.start()
			threads.append(thread)
		else:
			threadAdded = False
			while not threadAdded:
				for i,t in enumerate(threads):
					if not t.isAlive():
						thread = testit(source)
						thread.start()
						threads[i] = thread
						threadAdded = True
						break
				if not threadAdded: time.sleep(0.010)
		#print "Package: %s" % source["Package"]
		#print "Version: %s" % source["Version"]
		#print "Directory: %s" % source["Directory"]
		#print "tar.gz: %s %s" % (source["tar.gz"][0], source["tar.gz"][1])
		#print "patch: %s %s" % (source["patch"][0], source["patch"][1])
		#print "dsc: %s %s" % (source["dsc"][0], source["dsc"][1])

	threadsFinished = False
	while not threadsFinished:
		threadsFinished = True
		for t in threads:
			if t.isAlive():
				threadsFinished = False
		if not threadsFinished: time.sleep(0.1)

	nowatch.sort(key=operator.itemgetter('Package'))
	warning.sort(key=operator.itemgetter('Package'))
	needsupdate.sort(key=operator.itemgetter('Package'))
	uptodate.sort(key=operator.itemgetter('Package'))

	htmlfile = "/tmp/report"+str(random.randint(0,1000))+".html"
	if os.path.isfile(htmlfile): os.remove(htmlfile)
	html = open(htmlfile, "w+")
	html.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
	html.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n")
	html.write("<head>\n")
	html.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
	html.write("<title>APT repository external health status report ("+str(len(data))+" packages)</title>\n")
	html.write("</head>\n")
	html.write("<body>\n")
	html.write("<h1>Needs Update ("+str(len(needsupdate))+")</h1><br/>\n")
	html.write("<table>\n")
	html.write("<tr><td>Package</td><td>Debian version</td><td>Upstream version</td></tr>\n")
	for source in needsupdate:
		html.write("<tr>")
		html.write("    <td>"+source["Package"]+" <a href=\""+archiveUrl+source["Directory"]+"/"+source["patch"][1]+"\">patch</a> <a href=\""+archiveUrl+source["Directory"]+"/"+source["dsc"][1]+"\">dsc</a></td>")
		html.write("    <td>"+source["DebianUVersion"]+" ("+source["DebianMangledUVersion"]+")</td>")
		html.write("    <td><a href=\""+cgi.escape(source["UpstreamURL"])+"\">"+source["UpstreamVersion"]+"</a></td>")
		html.write("</tr>\n")
	html.write("</table>")

	html.write("<br/><br/><br/>\n")
	html.write("<h1>Warnings ("+str(len(warning))+")</h1><br/>\n")
	html.write("<table>\n")
	html.write("<tr><td>Package</td><td>Warnings</td></tr>\n")
	for source in warning:
		html.write("<tr>")
		html.write("    <td valign=\"top\"><a href=\""+archiveUrl+source["Directory"]+"/"+source["dsc"][1]+"\">"+source["Package"]+"</a></td>")
		html.write("    <td valign=\"top\">")
		for warning in source["Warning"]:
			html.write(warning+"<br/>")
		html.write("    </td>")
		html.write("</tr>\n")
	html.write("</table>")

	html.write("<br/><br/><br/>\n")
	html.write("<h1>No watch ("+str(len(nowatch))+")</h1><br/>\n")
	for source in nowatch:
		html.write("<a href=\""+archiveUrl+source["Directory"]+"/"+source["dsc"][1]+"\">"+source["Package"]+"</a><br/>\n")

	html.write("<br/><br/><br/>\n")
	html.write("<h1>Up to Date ("+str(len(uptodate))+")</h1><br/>\n")
	html.write("<table>\n")
	html.write("<tr><td>Package</td><td>Debian version</td><td>Upstream version</td></tr>\n")
	for source in uptodate:
		html.write("<tr>")
		html.write("    <td>"+source["Package"]+" <a href=\""+archiveUrl+source["Directory"]+"/"+source["patch"][1]+"\">patch</a> <a href=\""+archiveUrl+source["Directory"]+"/"+source["dsc"][1]+"\">dsc</a></td>")
		html.write("    <td>"+source["DebianUVersion"]+" ("+source["DebianMangledUVersion"]+")</td>")
		html.write("    <td><a href=\""+cgi.escape(source["UpstreamURL"])+"\">"+source["UpstreamVersion"]+"</a></td>")
		html.write("</tr>\n")
	html.write("</table>")

	html.write("</body></html>")
	html.close()

	os.system("x-www-browser "+htmlfile)
