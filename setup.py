#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import METADATA
from distutils.core import setup

try:
	setup(**METADATA)
except:
	raise "Something failed on setup"