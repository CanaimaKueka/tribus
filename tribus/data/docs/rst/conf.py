#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',
                                    '..', '..'))
sys.path.insert(0, base)

from tribus.config.sphinx import *
