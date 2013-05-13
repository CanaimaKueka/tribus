#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  (C) Copyright 2009-2010, GetDeb Team - https://launchpad.net/~getdeb
  --------------------------------------------------------------------
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  --------------------------------------------------------------------
  
  Configuration check functions
"""
import sys
def check_config(config, required_config):
    """ Check if required_config items are contained in config """
    for item in required_config:
        if not item in config:
            print "Config item",item,"is not defined"
            sys.exit(3)
