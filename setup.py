#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_setup_data
from setuptools import setup

setup(**get_setup_data(BASEDIR))
# try:
# except Exception, e:
#     print e
