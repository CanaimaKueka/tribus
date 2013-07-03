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

import os, ConfigParser



def ConfigMapper(confdir):
    dictionary = {}
    config = ConfigParser.ConfigParser()
    conffiles = listdirfullpath(confdir)
    configuration = config.read(conffiles)
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        for option in options:
            try:
                giveme = config.get(section, option)
                if section == 'array':
                    process = giveme[1:-1].split(',')
                elif section == 'boolean':
                    process = giveme
                elif section == 'integer':
                    process = int(giveme)
                else:
                    process = '"'+giveme+'"'
                dictionary[option] = process
            except:
                dictionary[option] = None
    return dictionary