#!/usr/bin/env python
# -*- coding: utf-8 -*-


def readconfig(filename, optionchar='=', commentchar='#', options=[], conffile=False):
    f = open(filename)

    if conffile:
        options = {}

    for line in f:
        if commentchar in line:
            line, comment = line.split(commentchar, 1)
        if optionchar in line and conffile:
            option, value = line.split(optionchar, 1)
            options[option.strip()] = value.strip()
        elif optionchar not in line and conffile:
            options['orphaned'].append(line.strip())
        else:
            options.append(line.strip())

    f.close()
    return options