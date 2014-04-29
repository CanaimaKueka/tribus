#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mongoengine
from tribus import BASEDIR
from tribus.common.utils import get_path

DEBUG = True

try:
    from tribus.config.ldap import AUTH_LDAP_BASE
except:
    pass

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
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tribus',
        'USER': 'tribus',
        'PASSWORD': 'tribus',
        'HOST': 'localhost',
        'PORT': '',
=======
        'ENGINE': 'django.db.backends.sqlite3'
>>>>>>> 855b0b4a85af16a758c7137dc47cef24cd37f09a
    }
}

INSTALLED_APPS = (
<<<<<<< HEAD
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
=======
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_auth_ldap',
    'django_static',
>>>>>>> 855b0b4a85af16a758c7137dc47cef24cd37f09a
    'tribus.testing',
    'tribus.web.cloud',
    'south',
    'haystack',
)

ROOT_URLCONF = 'tribus.web.urls'
<<<<<<< HEAD
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
=======

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

>>>>>>> 855b0b4a85af16a758c7137dc47cef24cd37f09a
