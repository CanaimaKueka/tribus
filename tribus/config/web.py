#!/usr/bin/env python
# -*- coding: utf-8 -*-

import djcelery
from celery.schedules import crontab

from tribus import BASEDIR
from tribus.common.utils import get_path
from tribus.config.ldap import *

djcelery.setup_loader()


SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'America/Caracas'
LANGUAGE_CODE = 'es'
DATABASE_OPTIONS = {'charset': 'utf8'}
DEFAULT_CHARSET = 'utf-8'
LOCALE_PATHS = [get_path([BASEDIR, 'tribus', 'data', 'i18n'])]

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

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'tribus.web.urls'
WSGI_APPLICATION = 'tribus.web.wsgi.application'

#
# LDAP CONFIGURATION ----------------------------------------------------------
#

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
)

# This should be secret, but as we are in development, doesn't matter
# Production settings should be set in tribus/config/web_production.py
# Other local configuration should be set in tribus/config/web_local.py
SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

#
# DATABASE CONFIGURATION ------------------------------------------------------
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tribus',
        'USER': 'tribus',
        'PASSWORD': 'tribus',
        'HOST': 'localhost',
        'PORT': '',
    },
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': AUTH_LDAP_SERVER_URI,
        'USER': AUTH_LDAP_BIND_DN,
        'PASSWORD': AUTH_LDAP_BIND_PASSWORD,
    }
}

DATABASE_ROUTERS = ['ldapdb.router.Router']

PASSWORD_HASHERS = (
    'tribus.web.registration.ldap.hashers.SSHAPasswordLDAPHasher',
)

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'database'
CELERY_CACHE_BACKEND = 'memory'
CELERY_RESULT_DBURI = "postgresql://tribus:tribus@localhost/tribus"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERYBEAT_SCHEDULE = {
    "update_cache": {
        "task": "tribus.web.cloud.tasks.update_cache",
        "schedule": crontab(minute=0, hour=0),  # A las 12 am
        "args": (),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


APPEND_SLASH = True
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_FULL_DEBUG = False
API_LIMIT_PER_PAGE = 20
TASTYPIE_DEFAULT_FORMATS = ['json']
ACCOUNT_ACTIVATION_DAYS = 7


# CONFIGURACION HAYSTACK CON XAPIAN
XAPIAN_INDEX = get_path([BASEDIR, 'xapian_index'])
HAYSTACK_LOGGING = True
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': XAPIAN_INDEX,
        'HAYSTACK_XAPIAN_LANGUAGE': 'spanish'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

INSTALLED_APPS = (
    'ldapdb',
    'django_auth_ldap',
    'south',
    'django_static',
    'djcelery',
    'tastypie',
    'haystack',
    'celery_haystack',
    'registration',
    'waffle',
    'kombu.transport.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.web',
    'tribus.web.registration',
    'tribus.web.cloud',
    'tribus.web.profile',
    'tribus.web.admin',
)

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'waffle.middleware.WaffleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.tz',
    'tribus.web.processors.default_context',
)

try:
    from tribus.config.logger import *
except:
    pass

try:
    from tribus.config.web_local import *
except:
    pass

try:
    from tribus.config.web_production import *
except:
    pass
