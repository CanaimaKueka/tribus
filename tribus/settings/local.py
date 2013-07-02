#!/usr/bin/env python
# -*- coding: utf-8 -*-

SECRET_KEY = 'oue0893ro5c^82!zke^ypu16v0u&%s($lnegf^7-vcgc^$e&$f'

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'facebook', 'google', 'github')

TWITTER_CONSUMER_KEY = '1uxQKRiKzHYUl3QbQSQ'
TWITTER_CONSUMER_SECRET = 'gLLJf5DIuJ4wvrVJI6cL553AIGdLjxnsUlwJbOKhw'
GOOGLE_OAUTH2_CLIENT_ID = '241742098100.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'AeJo0x0mS4SAtQF_TuAHsfGC'
FACEBOOK_APP_ID='172639862908723'
FACEBOOK_API_SECRET='ef4e623c629e9e5ca5632bdd703c80a4'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
GITHUB_APP_ID = 'c3d70354858107387ef8'
GITHUB_API_SECRET = 'b9defd6193c11c8fb27c9f65ddaba0747524afcc'

# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://localhost"
AUTH_LDAP_BASE = "dc=tribus,dc=org"
AUTH_LDAP_BIND_DN = "cn=admin,"+AUTH_LDAP_BASE
AUTH_LDAP_BIND_PASSWORD = "tribus"
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,'+AUTH_LDAP_BASE

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

BROKER_URL = 'redis://localhost:6379/0'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'martinez.faneyth@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_SUBJECT_PREFIX = '[Tribus] '



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

