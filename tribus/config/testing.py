#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mongoengine
from tribus import BASEDIR
from tribus.common.utils import get_path

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tribus',
        'USER': 'tribus',
        'PASSWORD': 'tribus',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.testing',
    'tribus.web',
    'tribus.web.registration',
    'tribus.web.cloud',
    'tribus.web.profile',
    'ldapdb',
    'django_auth_ldap',
    #'social_auth',
    'djcelery',
    'south',
    'django_static',
    'tastypie',
    'tastypie_mongoengine',
    'haystack',
    'celery_haystack',
    'registration',
    'tribus.testing',
)

ROOT_URLCONF = 'tribus.web.urls'
STATIC_URL = '/static/'
SITE_ID = 1
EDIA_URL = '/media/'
STATICFILES_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'static'])]
TEMPLATE_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'templates'])]


AUTH_LDAP_SERVER_URI = "ldap://localhost"
AUTH_LDAP_BASE = "dc=tribus,dc=org"
AUTH_LDAP_BIND_DN = "cn=admin," + AUTH_LDAP_BASE
AUTH_LDAP_BIND_PASSWORD = "tribus"
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,' + AUTH_LDAP_BASE


XAPIAN_INDEX = os.path.join(BASEDIR, 'xapian_index/')
HAYSTACK_LOGGING = True
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': XAPIAN_INDEX,
        'HAYSTACK_XAPIAN_LANGUAGE': 'spanish'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'


try:
    mongoengine.connect(db='tribus')
except:
    pass
