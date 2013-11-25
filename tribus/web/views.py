#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
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

from django.shortcuts import render
from tribus.web.registration.forms import SignupForm
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.contrib.contenttypes.models import ContentType

def tour(request):
    return render('tour.html', {})


def index(request):
    
    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.resource', 'angular.infinite-scroll',
                 'angular.bootstrap', 'angular.moment']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'dashboard.angular', 'navbar.angular']
    
    if request.user.is_authenticated():
        # Cargamos otras funciones adicionales
        render_js += ['moment', 'md5']

        return render(request, 'dashboard.html', {
            'render_js': render_js,
            })
    else:
        signupform = SignupForm()
        return render(request, 'index.html', {
            'signupform': signupform,
            'render_js': render_js,
            })


def tribus_search(request):
    context={}
        
    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.resource', 'angular.bootstrap']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
        'elements.angular', 'cloud.angular', 'navbar.angular']

    context ["render_js"]= render_js
    if request.GET:
        query = request.GET.get('q', '')
        objects = SearchQuerySet().filter(autoname = query)
        if objects:
            model_name = request.GET.get('filter', objects[0].model_name)
            sqs = objects.models(ContentType.objects.get(model=model_name).model_class())
            print sqs
            #paginator = Paginator(filter(None, sqs), 20) # Mas lento pero no hace falta print para que coloque bien los usuarios
            paginator = Paginator(sqs, 15) # Mas rapido pero necesita imprimir para mostrar correctamente los usuarios
            
            try:
                page = paginator.page(int(request.GET.get('page', 1)))
            except InvalidPage:
                return render(request, 'search/search.html', {})
            
            context["page"]= page
            context['query'] = query
            context['filter'] = model_name
        else:
            context["page"]= None
            context['query'] = query
            context['filter'] = None
            
    return render(request, 'search/search.html', context)