#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_path

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_path([BASEDIR, 'data­base.db']),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
	'south',
    'tribus.testing',
)