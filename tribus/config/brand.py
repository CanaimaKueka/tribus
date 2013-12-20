#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

TRIBUS_DISTRO = _('Canaima GNU/Linux')
TRIBUS_ROLE_1 = _('Shaman')
TRIBUS_ROLE_2 = _('Chieftain')
TRIBUS_ROLE_3 = _('Warrior')
TRIBUS_ROLE_4 = _('Harvester')

TRIBUS_SPONSORS = [
    {
        'name': 'Metadistribución Canaima GNU/Linux',
        'image': '/static/img/canaima-logo.svg',
        'url': 'http://canaima.softwarelibre.gob.ve/',
    },
    {
        'name': 'Centro Nacional de Tecnologías de la Información',
        'image': '/static/img/cnti-logo.svg',
        'url': 'http://cnti.gob.ve/',
    },
    {
        'name':
        'Fondo de Investigación y Desarrollo de las Telecomunicaciones',
        'image': '/static/img/fidetel-logo.svg',
        'url': 'http://fidetel.gob.ve/',
    },
]
