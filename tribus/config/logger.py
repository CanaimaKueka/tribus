#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'tribus': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'scss': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'SocialAuth': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'haystack': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}
