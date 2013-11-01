#!/usr/bin/env python
# -*- coding: utf-8 -*-

def default_context(request):
	return {
		'render_css': ['normalize', 'bootstrap', 'bootstrap-responsive',
			'fonts', 'font-awesome', 'tribus', 'tribus-responsive'],
		'render_js': ['jquery', 'bootstrap'],
		'tribus_distro': 'tribus_distro',
		'tribus_role_1': 'tribus_role_1',
		'tribus_role_2': 'tribus_role_2',
		'tribus_role_3': 'tribus_role_3',
	}

