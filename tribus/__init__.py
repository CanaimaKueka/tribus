#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tribus.common.config import readconfig
from tribus.common.utils import get_packages, get_packages_data, get_data_files, get_path

BASEDIR = get_path([__file__, '..'])
EXCLUDE_PATTERNS = readconfig(filename=get_path([BASEDIR, 'data', 'dist', 'exclude-patterns.list']),
					   conffile=True)
SOURCE_FILES = 
EXCLUDE_PACKAGES = ['tools', 'tests', 'tribus.console']
METADATA = readconfig(filename=get_path([BASEDIR, 'METADATA']), conffile=True)
METADATA['long_description'] = open(os.path.join(BASEDIR, 'README')).read()
METADATA['packages'] = get_packages(exclude_packages=EXCLUDE_PACKAGES, path=BASEDIR)
METADATA['packages_data'] = get_packages_data(exclude_packages=EXCLUDE_PACKAGES,
											  exclude_files=GITIGNORE+SOURCE_FILES,
											  path=BASEDIR)
METADATA['data_files'] = [
	get_data_files(path=os.path.join(BASEDIR, 'tribus', 'console'),
		           dest='/usr/share/tribus/', pattern='*.*')
	get_data_files(path=os.path.join(BASEDIR, 'scripts'), dest='/usr/bin/', pattern='*.*')
]

get_data_files(packages_data=, excludeBASEDIR)
METADATA['classifiers'] = []
METADATA['install_requires'] = []

for cls in open(os.path.join(BASEDIR, 'tribus', 'data', 'dist', 'python-classifiers.list')):
    METADATA['classifiers'].append(cls)

for req in open(os.path.join(BASEDIR, 'tribus', 'data', 'dist', 'python-dependencies.list')):
    if '#egg=' in req:
        METADATA['dependency_links'].append(req)
        METADATA['install_requires'].append(req.split('#egg=')[1])
    else:
        METADATA['install_requires'].append(req)
