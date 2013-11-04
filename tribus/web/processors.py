#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus.config.brand import *

def default_context(request):
    return {
        'render_css': ['normalize', 'bootstrap', 'bootstrap-responsive',
            'fonts', 'font-awesome', 'tribus', 'tribus-responsive'],
        'render_js': ['jquery', 'bootstrap'],
        'tribus_distro': TRIBUS_DISTRO,
        'tribus_role_1': TRIBUS_ROLE_1,
        'tribus_role_2': TRIBUS_ROLE_2,
        'tribus_role_3': TRIBUS_ROLE_3,
    }