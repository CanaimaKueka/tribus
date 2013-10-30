#!/usr/bin/env python
# -*- coding: utf-8 -*-

def default_context(request):
	return {
		'render_css': ['normalize', 'bootstrap', 'bootstrap-responsive',
			'fonts', 'font-awesome', 'tribus', 'tribus-responsive'],
		'render_js': [],
	}

