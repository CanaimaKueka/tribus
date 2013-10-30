#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^packages/$',
        'tribus.web.packages.views.frontpage',
        name='packages_frontpage'),

    url(r'^packages/(?P<name>(\w*\W*)*)',
        'tribus.web.packages.views.profile',
        name='packages_profile'),

    url(r'^packages/t/(?P<tag>(\w*\W*)*)',
        'tribus.web.packages.views.by_tag',
        name='packages_by_tag'),

    url(r'^packages/c/(?P<category>(\w*\W*)*)',
        'tribus.web.packages.views.by_category',
        name='packages_by_category'),
    )
