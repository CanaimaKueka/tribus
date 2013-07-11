#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_setup_data
from setuptools import setup

try:
	setup(**get_setup_data(BASEDIR))
except Exception, e:
    print e
