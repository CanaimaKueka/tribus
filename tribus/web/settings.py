#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import djcelery
import ldap
from tribus.web.auth.ldap.config import LDAPSearch, GroupOfNamesType
djcelery.setup_loader()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tribus',
        'USER': 'tribus',
        'PASSWORD': 'tribus',
        'HOST': 'localhost',
        'PORT': '',
    },
   # 'ldap': {
   #     'ENGINE': 'ldapdb.backends.ldap',
   #     'NAME': 'ldap://localhost/',
   #     'USER': 'cn=admin,dc=tribus,dc=org',
   #     'PASSWORD': 'tribus',
   #  }
 }
AUTHENTICATION_BACKENDS = (
    'tribus.web.auth.ldap.backend.LDAPBackend',
)

LOGIN_REDIRECT_URL="/i/"

ACCOUNT_ACTIVATION_DAYS = 7

# DATABASE_ROUTERS = ['ldapdb.router.Router']

BROKER_URL = 'redis://localhost:6379/0'

SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
STATIC_ROOT = ''
STATIC_URL = os.path.join(SITE_ROOT, 'static', '')
STATICFILES_DIRS = (
	os.path.join(SITE_ROOT, 'static', ''),
)
TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates', ''),
)
ROOT_URLCONF = 'tribus.web.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.web',
    'djcelery',
    'south',
    'ldapdb'
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Luis Alejandro Martínez Faneyth', 'luis@huntingbears.com.ve'),
)

MANAGERS = ADMINS

SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

TIME_ZONE = 'America/Caracas'

LANGUAGE_CODE = 'es-ve'

DATABASE_OPTIONS = {'charset': 'utf8'}

DEFAULT_CHARSET = 'utf-8'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'tribus.web.processors.tribusconf',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter':'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    },
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'localhost:6379:1',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
    },
}


AUTHENTICATION_BACKENDS = (
    'tribus.web.auth.ldap.backend.LDAPBackend',
)


# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://localhost"
AUTH_LDAP_BASE = "dc=tribus,dc=org"
AUTH_LDAP_BIND_DN = "cn=admin,dc=tribus,dc=org"
AUTH_LDAP_BIND_PASSWORD = "tribus"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_BASE, ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
    )

# Set up the basic group parameters.
#AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=django,ou=groups,dc=example,dc=com",
#    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
#)
#AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

# Simple group restrictions
#AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
#AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

#AUTH_LDAP_PROFILE_ATTR_MAP = {
#    "employee_number": "employeeNumber"
#}

#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}

#AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600


