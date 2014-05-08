#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus.config.brand import TRIBUS_SPONSORS
from django.shortcuts import render
from tribus.web.registration.forms import SignupForm
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.contrib.contenttypes.models import ContentType
from tribus.web.admin.forms import ActiveModulesForm
from django.http.response import HttpResponseRedirect

switch_names = {
    'cloud':'Package cloud',
    'profile': 'User profiles',
    'admin_first_time': "Admin's first time configuration" 
}

def tribus_config(request):
    context = {}
    
    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.sanitize', 'angular.resource',
                    'angular.bootstrap']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'search.angular',
                  'navbar.angular']

    context["render_js"] = render_js
    
    return render(request, 'admin/admin_content.html', context)
    
    
def active_modules(request):
    from waffle import Switch
    context = {}
    
    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.sanitize', 'angular.resource',
                    'angular.bootstrap']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'search.angular',
                  'navbar.angular', 'admin.angular']

    context["render_js"] = render_js
    
    sw = Switch.objects.order_by('name')
    
    if request.method == 'GET':
        form = ActiveModulesForm(request, [(switch_names[switch.name], switch) for switch in sw])
        context['form'] = form
        
    if request.method == 'POST':
        form_2 = ActiveModulesForm(request, [])
        if form_2.is_valid():
            return HttpResponseRedirect('/admin/tribus-config/')
            
    return render(request, 'admin/active_modules.html', context)


def logger_levels(request):
    context = {}
     
    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.sanitize', 'angular.resource',
                    'angular.bootstrap']
 
    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'search.angular',
                  'navbar.angular']

    context["render_js"] = render_js
     
    return render(request, 'admin/admin_content.html', context)
