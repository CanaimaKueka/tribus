#!/usr/bin/env python
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

# This file was copied from REVU (https://launchpad.net/revu)
# and adapted for the getdeb-uploaders group  

import sys
import os
import shutil
from rdflib import Namespace
from rdflib.Graph import Graph

from optparse import OptionParser

class RevuKeyUpdater:
    """ Retrieves Fingerprints from a Launchpad group by parsing the group's RDF
       and stores the corresponding keys in a new GPG keyring. """
    
    def __init__(self, lpgroup, revubase):
        "Initializes this class."
        self.lpgroup = lpgroup
        self.keyserver = 'keyserver.ubuntu.com'
        self.keyring = "%s/uploaders.gpg" % revubase
        self.gpgopts = "--no-options --no-default-keyring "
#        self.gpgopts += "--secret-keyring %s/secring.gpg" % revubase
#        self.gpgopts += " --trustdb-name %s/trustdb.gpg" % revubase
        self.gpgopts += " --keyring %s" % self.keyring
        self.gpgopts += " --keyserver keyserver.ubuntu.com"
        self.gpgopts += " --no-auto-check-trustdb --trust-model always"
        self.fingerprints = []
	self.revubase = revubase
    
    def get_fingerprints(self):
	uploaders_key_ring = "%s/uploaders.gpg" % self.revubase
	if os.path.exists(uploaders_key_ring):
		os.unlink(uploaders_key_ring)
        "Parses fingerprints from the RDF."
 		# We got our user; now query launchpad and retrieve their GPG keys
        g = Graph()
        g.parse('https://launchpad.net/people/%s/+rdf' % self.lpgroup)
        results = g.query("SELECT ?member WHERE { ?any foaf:member ?member . }",
             initNs=dict( foaf=Namespace("http://xmlns.com/foaf/0.1/")))

        for statement in results:
            print statement[0]
            g2 = Graph()
            g2.parse('https://launchpad.net/%s' % statement[0])
            results2 = g2.query("SELECT ?fingerprint WHERE { ?any wot:fingerprint ?fingerprint . }", 
                 initNs=dict( wot=Namespace("http://xmlns.com/wot/0.1/")))
            for statement2 in results2:
                print statement2[0]
                self.fingerprints.append(statement2[0])
            print
    
    def do_update(self):
        "Handles calling GPG for all found fingerprints."
        self.get_fingerprints()
        for fingerprint in self.fingerprints:
            # get the keyid from the fingerprint
            key = fingerprint[-8:]
            print key
            os.system("gpg %s --recv-key %s" % (self.gpgopts, key))

    def add_fingerprint(self, fingerprint):
		key = fingerprint[-8:]
		os.system("gpg %s --recv-key %s" % (self.gpgopts, key))

def main():
    parser = OptionParser()
    parser.add_option("-g", "--launchpad-group", dest="group", type="string")
    parser.add_option("-b", "--revu-base", dest="base", type="string")

    (options, args) = parser.parse_args()

    
    updater = RevuKeyUpdater(lpgroup = options.group or 'getdeb-uploaders',
        revubase = options.base or os.environ['HOME']+'/debfactory/keyrings'    )
    updater.do_update()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'User requested interrupt'
		sys.exit(1)
