#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''

Tribus setuptools script
========================

This script invokes the setup script for Tribus.

For more information about this file, see documentation on tribus/common/setup/utils.py

'''

from setuptools import setup

from tribus import BASEDIR
from tribus.common.setup.utils import get_setup_data

setup(**get_setup_data(BASEDIR))
# try:
#     setup(**get_setup_data(BASEDIR))
# except Exception, e:
#     print e
