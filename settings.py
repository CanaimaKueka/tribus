#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

conffiles = glob.glob(os.path.join(os.path.dirname(__file__), 'setup', '*.conf'))

conffiles.sort()

for f in conffiles:
    execfile(os.path.abspath(f))
