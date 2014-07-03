#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
from tribus import BASEDIR
from tribus.common.utils import get_path

DEBUG = True

# try:
#     from tribus.config.ldap import AUTH_LDAP_BASE
# except:
#     pass

SITE_ROOT = get_path([BASEDIR, 'tribus', 'web'])
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'static'])]
TEMPLATE_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'templates'])]

DJANGO_STATIC = not DEBUG
DJANGO_STATIC_MEDIA_ROOTS = [get_path([BASEDIR, 'tribus', 'data'])]
DJANGO_STATIC_FILENAME_GENERATOR = 'tribus.common.utils.filename_generator'
DJANGO_STATIC_NAME_MAX_LENGTH = 200

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_auth_ldap',
    'django_static',
    'tribus.tests',
    'tribus.web.cloud',
    'south',
    'haystack',
)

ROOT_URLCONF = 'tribus.web.urls'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
