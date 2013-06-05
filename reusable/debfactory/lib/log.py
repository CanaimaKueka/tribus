#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    (C) Copyright 2009-2010, GetDeb Team - https://launchpad.net/~getdeb
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
"""
Logger class
"""
import time

class Logger:
    """ Small helper class for logging """    
    def __init__(self, verbose=True):
        self.verbose = verbose
        
    def log(self, message, verbose=None):
        """
        If verbose is True print the message
        """
        verbose = verbose or self.verbose
        if self.verbose:
            print "%s: %s" % (time.strftime('%c'), message)
            
    def print_(self, message):
        """
        always print a message
        """
        print "%s: %s" % (time.strftime('%c'), message)
