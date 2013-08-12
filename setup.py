#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.setup.utils import get_setup_data
from setuptools import setup

setup(**get_setup_data(BASEDIR))
# try:
#     setup(**get_setup_data(BASEDIR))
# except Exception, e:
#     print e
