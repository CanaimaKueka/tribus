#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus import BASEDIR
from tribus.common.utils import get_path

try:
    import djcelery
    djcelery.setup_loader()
except:
    pass

try:

    from celery.schedules import crontab

    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost/0'
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

    CELERYBEAT_SCHEDULE = {
        "update_cache": {
            "task": "tribus.web.cloud.tasks.update_cache",
            "schedule": crontab(minute=0, hour=0), # A las 12 am
            "args": (),
        }
    }

except:
    pass

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
# LDAP CONFIGURATION -----------------------------------------------------------
#

AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.twitter.TwitterBackend',
    #'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.contrib.github.GithubBackend',
    'django_auth_ldap.backend.LDAPBackend',


    # acomoda aplicacion de ldap
    #'django.contrib.auth.backends.ModelBackend',
)

# This should be secret, but as we are in development, doesn't matter
# Production settings should be set in tribus/config/web_production.py
# Other local configuration should be set in tribus/config/web_local.py
SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

# SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'facebook', 'google', 'github')
# SOCIAL_AUTH_DEFAULT_USERNAME = 'tribus'
# SOCIAL_AUTH_UID_LENGTH = 32
# SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32
# SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 32
# SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 32
# SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32

# TWITTER_CONSUMER_KEY = 'A2jx982HVh8KuFQ9q2iN8A'
# TWITTER_CONSUMER_SECRET = 'wU3T7KPgvNqj3mBH7Pyn81T10lSw2NN4LLuZCLYk5U'
# GOOGLE_OAUTH2_CLIENT_ID = '827167166748-7h5k1crt9fsr8jjqindi1c8hfl48eahj.apps.googleusercontent.com'
# GOOGLE_OAUTH2_CLIENT_SECRET = 'VvoYXzfheMInzrcTq8v3Tdhf'
# FACEBOOK_APP_ID='172639862908723'
# FACEBOOK_API_SECRET='60735113b51809707ed3771b248fb37e'
# FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# GITHUB_APP_ID = 'c3d70354858107387ef8'
# GITHUB_API_SECRET = '55adbc6ecf54d295b391c8a6a1037e71165728d6'

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
    'tribus.web.registration.ldap.hashers.SSHAPasswordLDAPHasher',
    #'tribus.web.registration.hashers.DummyPasswordHasher',
)

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tribus.tests',
    'tribus.web',
    'tribus.web.registration',
    'tribus.web.cloud',
    'tribus.web.profile',
    'tribus.web.admin',
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
    #'social_auth.context_processors.social_auth_by_type_backends',
)

# SOCIAL_AUTH_PIPELINE = (
#    'social_auth.backends.pipeline.social.social_auth_user',
#    'social_auth.backends.pipeline.user.get_username',
#    'tribus.web.registration.social.pipeline.create_user',
#    'social_auth.backends.pipeline.social.associate_user',
#    'social_auth.backends.pipeline.social.load_extra_data',
#    'social_auth.backends.pipeline.user.update_user_details'
#)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'localhost:6379:1',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        },
    },
}

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
