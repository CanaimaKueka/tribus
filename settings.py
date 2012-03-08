#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
#os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
conffiles = glob.glob(os.path.join(os.path.dirname(__file__), 'setup', '*.py'))
conffiles.sort()

for f in conffiles:
    print f
    execfile(os.path.abspath(f))
