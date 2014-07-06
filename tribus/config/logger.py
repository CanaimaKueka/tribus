#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'standard'
        },
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'standard',
        #     'filename': '/tmp/tribus/logs/runtime.log'
        # },
    },
    'loggers': {
        'tribus': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'haystack': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}
