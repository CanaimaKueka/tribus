#!/usr/bin/env python
# -*- coding: utf-8 -*-

def default_context(request):
	return {
		'render_css': ['normalize', 'fonts', 'font-awesome', 'bootstrap', 
			'bootstrap-responsive', 'tribus', 'tribus-responsive'],
		'render_js': [],
	}

