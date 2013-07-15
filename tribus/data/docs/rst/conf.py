#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)

from tribus.config.sphinx import *
