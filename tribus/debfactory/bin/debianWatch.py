#!/usr/bin/python
import re
import os

if __name__ == "__main__":
	f = open("debian/changelog", "r")
	line = f.readlines()[0].strip("\r\n")
	f.close()

	prog = re.compile("(?P<source>.*) \((?P<version>.*)(?P<tmp>\d)\).*")
	match = prog.match(line)
	source = match.group("source")
	version = match.group("version")
	tmp = int(match.group("tmp"))
	tmp += 1
	new_version = version + str(tmp)

	os.system("dch -v \"" + new_version + "\" \"Added debian/watch file\"")
	os.system("sed -i 's/Standards-Version: .*/Standards-Version: 3\.9\.1/g' debian/control")
	f = open("debian/watch", "w+")
	f.write("version=3\n")
	f.close()


	prog = re.compile(".*(?P<html>http://[^ >]*).*")
	f = open("debian/copyright", "r")
	for line in f.readlines():
		line = line.strip("\r\n")
		match = prog.match(line)
		if match:
			os.system("x-www-browser " + match.group("html"))
			break
	f.close()
	os.system("nano debian/watch")
