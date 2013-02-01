#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Luis Alejandro Martínez Faneyth', 'luis@huntingbears.com.ve'),
)

MANAGERS = ADMINS

SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

TIME_ZONE = 'America/Caracas'

#_ = lambda s: s

#LANGUAGES = (
#  ('en', _('English')),
#)

LANGUAGE_CODE = 'es-ve'

DATABASE_OPTIONS = {'charset': 'utf8'} 

DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

MEDIA_ROOT = ''

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

STATIC_ROOT = ''

STATIC_URL = '/skins/'

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'skins', ''),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = os.path.join(SITE_ROOT, 'skins', APP_SKIN, '')

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tribus.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.viewer',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'tribus.processors.tribusconf',
)

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'viewer.UserProfile'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
