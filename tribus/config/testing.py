#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = (
    'south',
    'tribus.testing',
    'tribus.web.cloud',
)
