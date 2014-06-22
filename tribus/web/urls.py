#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from django.views.generic.simple import direct_to_template
from django.views.generic.base import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tribus.web.api import api_01

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(regex=r'^$', view='tribus.web.views.index'),
    url(regex=r'^about/$',
        view=TemplateView.as_view(template_name='about.html')),
    url(regex=r'^about/privacy/$',
        view=TemplateView.as_view(template_name='privacy.html')),
    url(regex=r'^about/terms/$',
        view=TemplateView.as_view(template_name='terms.html')),
    url(regex=r'^search/$', view='tribus.web.views.search'),
    url(regex=r'', view=include('tribus.web.registration.urls')),
    url(regex=r'', view=include('tribus.web.cloud.urls')),
    url(regex=r'', view=include('tribus.web.profile.urls')),
    url(regex=r'', view=include('social_auth.urls')),
    url(regex=r'^api/', view=include(api_01.urls)),
    
    # urls adicionales para el admin aqui
    url(regex=r'^admin/tribus-config/$', view='tribus.web.admin.views.tribus_config'),
    url(regex=r'^admin/tribus-config/active-modules/$', view='tribus.web.admin.views.active_modules'),
    url(regex=r'^admin/tribus-config/logger-levels/$', view='tribus.web.admin.views.logger_levels'),
    
    url(regex=r'^admin/', view=include(admin.site.urls)),
    # url(regex=r'^opensearch.xml/$', direct_to_template, {
    #     'template': 'opensearch.xml',
    #     'mimetype': 'application/opensearchdescription+xml'
    #     }, name="opensearch"),
)
