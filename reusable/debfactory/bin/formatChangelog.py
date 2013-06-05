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

  This script will read an unformated changelog from stdin and shorten each
  line to a specifed maximum length by splitting it up into multiple lines.
  It also appends spaces properly at the beginning of each line to make the new
  changelog fit in debian/changelog. The new changelog is written to the
  beginning of debian/changelog so this script has to be executed from the
  source tree.
"""
import tempfile
import os
import commands
import shutil

# The maximum line length
LINELENGTH = 78

if __name__ == "__main__":
    changelog = []
    line = ""
    # Read the changelog from stdin until "end"
    while line != "end":
        line = raw_input()
        if line != "end":
            changelog.append(line)
    new_changelog = []
    for line in changelog:
        # Replace tabs with spaces. We so avoid mis-identation
        line = line.replace("\t", "    ")
        # Sweet, isn't it ? :)
        leading_spaces = len(line) - len(line.lstrip())
        leading_spaces = " "*leading_spaces
        # Add four spaces to the line for the debian/changelog identation
        line = "    %s%s\n" % (leading_spaces, line.lstrip())
        if len(line) <= LINELENGTH:
            if len(line.strip()) == 0:
                new_changelog.append("\n")    
            else:
                new_changelog.append(line)
        else:
            # generate new lines for the changelog until the line is short enough
            while len(line) > LINELENGTH:
                # we only seperate the string on a space character. Let's hope
                # there is one on the "left side" of the string with max. LINELENGTH chars
                space_pos = line.rfind(" ", 0, LINELENGTH)
                # in case we have no luck here we add a warning and continue
                if space_pos == -1:
                    new_changelog.append("WARNING: THE FOLLOWING LINE COULD NOT BE SHORTENED\n")
                    new_changelog.append("%s\n" % line)
                    break
                left_line = line[:space_pos]
                # the part on the right side of the string gets prefixed with the same number
                # of spaces as the line itself. So it gets aligned in debian/changelog properly.
                line = "    %s%s" % (leading_spaces, line[space_pos+1:])
                new_changelog.append("%s\n" % left_line)
                # in case the line which is left is too short the while loop won't execute again
                # so we have to append the line here.
                if len(line) <= LINELENGTH:
                    # TODO: if the lines in the upstream changelog are already limited to a length
                    # we may want to also append the next line if it belongs there.
                    # At the moment this changelog:
                    #     This text is already limited in
                    #     length.
                    # May become this one if we split the line before the "in":
                    #     This text is already limited
                    #     in
                    #     length.
                    new_changelog.append(line)
            

    # We need to write the changelog first to a temporary file in order to append
    # the exiting debian/changelog after it.
    f = open("debian/changelog.new", "w")
    f.writelines(new_changelog)

    # TODO: find a way to append to the beginning of a file without having to create
    # a temporary file and writing the original file line by line to it.
    f2 = open("debian/changelog")
    for line in f2.readlines():
        f.write(line)
    f2.close()
    f.close()
    shutil.move("debian/changelog.new", "debian/changelog")
