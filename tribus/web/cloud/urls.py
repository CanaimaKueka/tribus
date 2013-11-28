#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^cloud/$',
        'tribus.web.cloud.views.frontpage',
        name='cloud_frontpage'),

    url(r'^cloud/p/(?P<name>(\w*\W*)*)',
        'tribus.web.cloud.views.profile',
        name='cloud_profile'),
                       
    url(r'^cloud/l/index$',
        'tribus.web.cloud.views.package_list',
        name='cloud_list'),

    url(r'^cloud/l/tag/(?P<tag>(\w*\W*)*)',
        'tribus.web.cloud.views.by_tag',
        name='cloud_by_tag'),

    url(r'^cloud/l/category/(?P<category>(\w*\W*)*)',
        'tribus.web.cloud.views.by_category',
        name='cloud_by_category'),
    )
