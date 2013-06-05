#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import gettext as _

APP_SKIN = 'canaima'
APP_NAME = 'Tribus'
APP_DESC = u'Sistema para la Gestión de Comunidades en el Proyecto Canaima'
APP_MAIL = ''
LOCALE = ''

SIGNUP_URL = 'http://registro.canaima.softwarelibre.gob.ve/NewUserForm.php'
FORGOTPWD_URL = 'http://registro.canaima.softwarelibre.gob.ve/ResetPasswordForm.php'
TRAC_JSONRPC = 'http://trac.canaima.softwarelibre.gob.ve/canaima/jsonrpc'

CONFTREE = {
    'packages': {
        'submenus': { 
            'upload': _('Upload package'),
            'search': _('Search package database'),
            'browse': _('Browse package database'),
        },
        'name': _('Packages'),
        'url': '/pkg/',
        'searchable': True,
        'index': True,
        'active': True,
    },
    'users': {
        'submenus': { 
            'new': _('New user request'),
            'search': _('Search user database'),
            'browse': _('Browse user database'),
        },
        'name': 'Users',
        'url': '/user/',
        'searchable': True,
        'index': True,
        'active': True,
    },
    'distributions': {
        'submenus': '',
        'name': _('Distributions'),
        'url': '/distro/',
        'searchable': False,
        'index': True,
        'active': True,
    },
    'teams': {
        'submenus': { 
            'new': _('New team request'),
        },
        'name': _('Work teams'),
        'url': '/teams/',
        'searchable': False,
        'index': True,
        'active': True,
    },
    'uploads': {
        'submenus': '',
        'name': 'Uploads',
        'url': '/uploads/',
        'searchable': True,
        'index': True,
        'active': True,
    },
    'tickets': {
        'submenus': '',
        'name': 'Tickets',
        'url': '/tickets/',
        'searchable': True,
        'index': True,
        'active': True,
    },
}
