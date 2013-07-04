#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.config import get_setup_data
from setuptools import setup
print get_setup_data(BASEDIR)
try:
    setup(**get_setup_data(BASEDIR))
except Exception, e:
    print e
