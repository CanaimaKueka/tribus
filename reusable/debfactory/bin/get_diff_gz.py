#!/usr/bin/python
import glob
import os
import sys
from httplib import HTTPConnection
import re
from subprocess import Popen, PIPE
import commands
from functools import cmp_to_key

MIRROR_URL = "188.138.90.189"
GETDEB_SUBDIR = ""

# If the package does not start with lib it is
# the first character. Else it is lib and the first character.
def get_package_subdir(orig):
	if orig.startswith('lib'):
		return orig[0:4]
	return orig[0]

def download(p,d):
	tmp = glob.glob('./' + p + '*.diff.gz')
	if tmp: return
	print 'wget -q ' + d
	os.system('wget -q ' + d)

def get_base_package_name():
	tmp = glob.glob('./*.orig.tar.gz')
	if not tmp:
		tmp = glob.glob('./*.orig.tar.bz2')
	if not tmp:
		tmp = glob.glob('./*.orig.tar.xz')
	if not tmp: return None
	return os.path.basename(tmp[0])

def search_on_getdeb(orig_file):
	global MIRROR_URL, GETDEB_SUBDIR
	http_connection = HTTPConnection(MIRROR_URL)
	basename = orig_file.split('_')[0]
	download_dir = 'http://' + MIRROR_URL + '/' + GETDEB_SUBDIR + '/ubuntu/pool/apps/' + get_package_subdir(orig_file) + \
	  '/' + basename + '/'
	http_connection.request('GET', download_dir)
	http_response = http_connection.getresponse()
	if http_response.status != 200: return None
	data = http_response.read()
	http_connection.close()
	data = data.split('\n')
	package_lines = list()
	for line in data:
		if basename in line:
			package_lines.append(line)
	if len(package_lines) == 0: return None
	p_d = list()
	package_re = re.compile('<a .*?>(?P<orig>.*?)(?:\.diff\.gz|\.debian\.tar\.gz)<')
	download_re = re.compile('<a href="(?P<download>.*?)">')
	for line in package_lines:
		search_result = re.search(package_re, line)
		if not search_result: continue
		orig = search_result.group('orig') 
		search_result = re.search(download_re, line)
		download = download_dir + search_result.group('download')
		p_d.append((orig,download))
	return p_d

def search_on_playdeb(orig_file):
	global MIRROR_URL, GETDEB_SUBDIR
	http_connection = HTTPConnection(MIRROR_URL)
	basename = orig_file.split('_')[0]
	download_dir = 'http://' + MIRROR_URL + '/' + GETDEB_SUBDIR + '/ubuntu/pool/games/' + get_package_subdir(orig_file) + \
	  '/' + basename + '/'
	http_connection.request('GET', download_dir)
	http_response = http_connection.getresponse()
	if http_response.status != 200: return None
	data = http_response.read()
	http_connection.close()
	data = data.split('\n')
	package_lines = list()
	for line in data:
		if basename in line:
			package_lines.append(line)
	if len(package_lines) == 0: return None
	p_d = list()
	package_re = re.compile('<a .*?>(?P<orig>.*?)(?:\.diff\.gz|\.debian\.tar\.gz)<')
	download_re = re.compile('<a href="(?P<download>.*?)">')
	for line in package_lines:
		search_result = re.search(package_re, line)
		if not search_result: continue
		orig = search_result.group('orig') 
		search_result = re.search(download_re, line)
		download = download_dir + search_result.group('download')
		p_d.append((orig,download))
	return p_d

def applyDiff(p,orig):
	package_name = orig.split('_')[0]
	version = orig.split('_')[1].split('.orig')[0]
	dir_name = package_name + '-' + version
	if not os.path.exists(dir_name):
		if orig.endswith(".gz"):
			print 'tar xzf ' + orig
			os.system('tar xzf ' + orig)
		elif orig.endswith(".bz2"):
			print 'tar xjf ' + orig
			os.system('tar xjf ' + orig)
		elif orig.endswith(".xz"):
			print 'tar xJf ' + orig
			os.system('tar xJf ' + orig)
		if not os.path.exists(dir_name):
			tmp = glob.glob('./' + package_name + '*')
			for t in tmp:
				if os.path.isdir(t):
					os.rename(t, dir_name)
	if not os.path.exists(dir_name + '/debian'):
		tmp = glob.glob(p + '*.diff.gz')

		cwd = os.getcwd()
		os.chdir(os.path.join(cwd, dir_name))
		if tmp:
			print 'zcat ../' + p + '*.diff.gz | patch -p1'
			os.system('zcat ../' + p + '*.diff.gz | patch -p1')
		else:
			print 'tar xzf ../' + p + '*.debian.tar.gz'
			os.system('tar xzf ../' + p + '*.debian.tar.gz')

		# Take the same release as the previous/current changelog entry
		p1 = Popen(["dpkg-parsechangelog"], stdout=PIPE)
		p2 = Popen(["grep", "^Distribution:"], stdin=p1.stdout, stdout=PIPE)
		p3 = Popen(["sed", "s/^Distribution: //"], stdin=p2.stdout, stdout=PIPE)
		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
		release = p3.communicate()[0].strip("\r\n")

		print 'dch -D ' + release + ' --newversion "'+version+'-1~getdeb1" "New upstream version"'
		os.system('dch -D ' + release + ' --newversion "'+version+'-1~getdeb1" "New upstream version"')

def diffVersionCompare(a,b):
	v1 = a[0].split("_")[1]
	v2 = b[0].split("_")[1]
	com="dpkg --compare-versions '%s' lt '%s' "%(v1,v2)
	if v1==v2: return 0
	(rc, output) = commands.getstatusoutput(com)
	if rc == 0: return -1
	return 1

if __name__ == "__main__":
	orig_file = get_base_package_name()
	if not orig_file:
		print "No orig.tar.gz file has been found."
		sys.exit(1)

	result = search_on_getdeb(orig_file) or []
	result2 = search_on_playdeb(orig_file) or []
	result.extend(result2)

	result.sort(key=cmp_to_key(diffVersionCompare))

	i = 0
	for r in result:
		p,d = r
		print i,p
		i += 1

	c = raw_input('Choose:')
	p,d = result[int(c)]
	download(p, d)
	applyDiff(p, orig_file)
