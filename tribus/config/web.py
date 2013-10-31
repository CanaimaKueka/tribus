#!/usr/bin/env python
# -*- coding: utf-8 -*-

import djcelery, mongoengine, os

from tribus import BASEDIR
from tribus.common.utils import get_path
from celery.schedules import crontab

try:
    from tribus.config.ldap import *
except:
    pass

SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'America/Caracas'
LANGUAGE_CODE = 'es-ve'
DATABASE_OPTIONS = { 'charset': 'utf8' }
DEFAULT_CHARSET = 'utf-8'

SITE_ROOT = get_path([BASEDIR, 'tribus', 'web'])
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'static'])]
TEMPLATE_DIRS = [get_path([BASEDIR, 'tribus', 'data', 'html'])]

DJANGO_STATIC = not DEBUG
DJANGO_STATIC_MEDIA_ROOTS = [get_path([BASEDIR, 'tribus', 'data'])]

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'tribus.web.urls'

WSGI_APPLICATION = 'tribus.web.wsgi.application'

#
# LDAP CONFIGURATION -----------------------------------------------------------
#

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.github.GithubBackend',
    'django_auth_ldap.backend.LDAPBackend',


    #acomoda aplicacion de ldap
    #'django.contrib.auth.backends.ModelBackend',
)

# This should be secret, but as we are in development, doesn't matter
# Production settings should be set in tribus/config/web_production.py
# Other local configuration should be set in tribus/config/web_local.py
SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'facebook', 'google', 'github')
SOCIAL_AUTH_DEFAULT_USERNAME = 'tribus'
SOCIAL_AUTH_UID_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32

TWITTER_CONSUMER_KEY = '1uxQKRiKzHYUl3QbQSQ'
TWITTER_CONSUMER_SECRET = 'gLLJf5DIuJ4wvrVJI6cL553AIGdLjxnsUlwJbOKhw'
GOOGLE_OAUTH2_CLIENT_ID = '241742098100.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'AeJo0x0mS4SAtQF_TuAHsfGC'
FACEBOOK_APP_ID='172639862908723'
FACEBOOK_API_SECRET='ef4e623c629e9e5ca5632bdd703c80a4'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
GITHUB_APP_ID = 'c3d70354858107387ef8'
GITHUB_API_SECRET = 'b9defd6193c11c8fb27c9f65ddaba0747524afcc'

#
# DATABASE CONFIGURATION -------------------------------------------------------
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
    'tribus.web.user.hashers.SSHAPasswordLDAPHasher',
    #'tribus.web.user.hashers.DummyPasswordHasher',
)

APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_FULL_DEBUG = False
API_LIMIT_PER_PAGE = 20
TASTYPIE_DEFAULT_FORMATS = ['json']
ACCOUNT_ACTIVATION_DAYS = 7

BROKER_URL = 'redis://localhost:6379/0'
# Programacion de task para djcelery
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    "update_cache": {
        "task": "tribus.web.packages.tasks.update_cache",
        "schedule": crontab(),
        "args": (),
    },               
}

# Configuracion de haystack y whoosh
WHOOSH_INDEX = os.path.join(BASEDIR, 'whoosh_index/')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}


# GRAVATAR_URL # Gravatar base url. Defaults to 'http://www.gravatar.com/'
# GRAVATAR_SECURE_URL # Gravatar base secure https url. Defaults to 'https://secure.gravatar.com/'
# GRAVATAR_DEFAULT_SIZE # Gravatar size in pixels. Defaults to '80'
# GRAVATAR_DEFAULT_IMAGE # An image url or one of the following: 'mm', 'identicon', 'monsterid', 'wavatar', 'retro'. Defaults to 'mm'
# GRAVATAR_DEFAULT_RATING # One of the following: 'g', 'pg', 'r', 'x'. Defaults to 'g'
# GRAVATAR_DEFAULT_SECURE # True to use https by default, False for plain http. Defaults to True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.web',
    'tribus.web.user',
    'tribus.web.packages',
    'tribus.web.profile',
    'ldapdb',
    'django_auth_ldap',
    'social_auth',
    'djcelery',
    'south',
    'django_static',
    'tastypie',
    'tastypie_mongoengine',
    'django_gravatar',
    'haystack',
    'whoosh'
)

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'martinez.faneyth@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_SUBJECT_PREFIX = '[Tribus] '

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


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
    'tribus.web.processors.default_context',
    'social_auth.context_processors.social_auth_by_type_backends',
)


SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'tribus.web.user.pipeline.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
)

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


try:
    djcelery.setup_loader()
except:
    pass

try:
    mongoengine.connect(db='tribus')
except:
    pass

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
