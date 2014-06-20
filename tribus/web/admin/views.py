#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from tribus.web.admin.forms import ActiveModulesForm
from django.http.response import HttpResponseRedirect
from tribus.config.switches import SWITCHES_CONFIGURATION

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
        form = ActiveModulesForm(request, [(SWITCHES_CONFIGURATION[switch.name][0], switch) for switch in sw])
        context['form'] = form
        
    if request.method == 'POST':
        form_2 = ActiveModulesForm(request)
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
