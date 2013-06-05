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

from socket import *
import re
from httplib import HTTPSConnection
from httplib import HTTPConnection

channels = "#GetDeb"
bot_nick = "gbotu"
ircaddr=("irc.freenode.net", 6667)
commands = { "policy" : "We have our own policy whether an application can be published on getdeb.net. Have a look at: http://wiki.getdeb.net/GetDebPackagePolicy", \
             "workflow" : "The workflow from a package request to the package being published on getdeb.net can be found here: http://wiki.getdeb.net/PackagingGuide/Workflow", \
             "request" : "Please read the /topic and file a bug in Launchpad if you want to report a package request." }

def get_bug_ids(msg):
	bug_matches = re.finditer('bug [#]?(?P<bug_id>\d+)', msg, re.DOTALL)
	bug_ids = []
	for bug_match in bug_matches:
		bug_ids.append(bug_match.group('bug_id'))

	bug_matches = re.finditer('bugs\.launchpad.net/.*?/(?P<bug_id>\d+)', msg, re.DOTALL)
	for bug_match in bug_matches:
		bug_id = bug_match.group('bug_id')
		if not bug_id in bug_ids:
			bug_ids.append(bug_id)

	return bug_ids

def get_bug_information(bug_ids):
	bug_information = []
	http_connection = HTTPSConnection('bugs.launchpad.net')
	for bug_id in bug_ids:
		http_connection.request('GET', '/bugs/' + bug_id + '/+text')
		http_response = http_connection.getresponse()
		if http_response.status != 200:
			print "Error occured when fetching data"
			continue
		data = http_response.read()
		data = data.split('\n')
		bug = {}
		bug_title = bug_task = bug_status = bug_importance = None
		for line in data:
			if line.startswith('title:'):
				bug_title = line.split(' ', 1)[1]
			elif line.startswith('task:'):
				bug_task = line.split(' ', 1)[1]
			elif line.startswith('status:'):
				bug_status = line.split(' ', 1)[1]
			elif line.startswith('importance:'):
				bug_importance = line.split(' ', 1)[1]
			elif line.startswith('Content-Type'): break
		bug['id'] = bug_id
		bug['title'] = bug_title
		bug['task'] = bug_task
		bug['status'] = bug_status
		bug['importance'] = bug_importance
		bug_information.append(bug)
	http_connection.close()
	return bug_information

def send_bug_information(bug_information, sock):
	global channels
	for bug in bug_information:
		msg = "Launchpad bug " + bug['id'] + " in " + \
		      bug['task'] + " \"" + bug['title'] + "\" [" + \
		      bug['status'] + "," + bug['importance'] + "] " + \
		      "https://bugs.launchpad.net/bugs/" + bug['id']
		sock.send("PRIVMSG " + channels + " :" + msg + "\r\n")


def send_information(msg, sock):
	global bot_nick, channels
	msg = msg.strip(' ')
	if not msg[0] == '!': return

	matches = re.finditer('^!(?P<command>\w+)\s*(?P<pipe>[>|]?)\s*(?P<receiver>\w*)$', msg)
	for match in matches:
		command = match.group('command')
		pipe = match.group('pipe')
		receiver = match.group('receiver')

		if receiver == bot_nick: return

		if not command: return
		if not command in commands: return
		if pipe == "|":
			if not receiver: return
			sock.send("PRIVMSG " + channels + " :" + receiver + ": " + commands[command] + "\r\n")
			return
		if pipe == ">":
			if not receiver: return
			sock.send("PRIVMSG " + receiver + " :" + commands[command] + "\r\n")
			return

		sock.send("PRIVMSG " + channels + " :" + commands[command] + "\r\n")

def send_youtube_information(msg, sock):
	global channels

	matches = re.finditer('youtube\.com(?P<link>/watch\S*)', msg)
	if not matches: return

	for match in matches:
		http_connection = HTTPConnection('www.youtube.com')
		http_connection.request('GET', match.group('link'))
		http_response = http_connection.getresponse()
		if http_response.status != 200:
			print "Error occured when fetching data"
			continue
		data = http_response.read(4096)

		titles = re.finditer('<title>(?P<title>.*)</title>', data, re.DOTALL)

		for title in titles:
			video_title = title.group('title')
			video_title = video_title.split('-', 1)
			video_title = video_title[1].strip()
			msg = "PRIVMSG " + channels + u" :\u0002" + video_title + \
			          u"\u000F www.youtube.com" + match.group('link') + "\r\n"
			sock.send(msg)

		http_connection.close()
	return

def start_bot():
	global channels, bot_nick, ircaddr
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(ircaddr)

	sock.send("NICK " + bot_nick + "\r\n")
	sock.send("USER " + bot_nick + " 0 * :python bot\r\n")

	sock.send("JOIN " + channels + "\r\n")

	while 1:
		data = sock.recv(4096)
		if data != "":
			if data.startswith('PING'):
				data = data.replace('PING', 'PONG')
				sock.send(data + "\r\n")
			data_lowercase = data.lower()
			channel_list = channels.split(',')
			for channel in channel_list:
				channel_lower = channel.lower()
				if data_lowercase.find('privmsg ' + channel_lower) != -1:
					msg = data.split(':', 2)[2].strip('\r\n')
					bug_ids = get_bug_ids(msg)
					bug_information = get_bug_information(bug_ids)
					send_bug_information(bug_information, sock)
					send_information(msg, sock)
					send_youtube_information(msg, sock)
	sock.shutdown(SHUT_RDWR)
	sock.close()

if __name__ == "__main__":
	start_bot()
