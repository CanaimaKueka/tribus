#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_path

DEBUG = True

DATA­BASES = {
    'de­fault': {
        'EN­GINE': 'django.db.backends.sql­ite3',
        'NAME': get_path([BASEDIR, 'data­base.db']),
        'USER': '',
        'PASS­WORD': '',
        'HOST': '',
        'PORT': '',
    }
}


INSTALLED_APPS = (
	'south',
    'tribus.testing',
)