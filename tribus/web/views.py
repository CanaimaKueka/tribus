#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tribus.config.brand import TRIBUS_SPONSORS
from django.shortcuts import render
from tribus.web.registration.forms import SignupForm
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.contrib.contenttypes.models import ContentType


def index(request):
    if request.user.is_authenticated():

        # Cargamos la librería AngujarJS junto con sus plugins
        render_js = ['angular', 'angular.sanitize', 'angular.resource',
                        'angular.bootstrap', 'angular.infinite-scroll',
                        'angular.moment']

        # Cargamos las funciones de Tribus para AngularJS
        render_js += ['controllers.angular', 'services.angular',
                      'elements.angular', 'dashboard.angular',
                      'navbar.angular']

        # Cargamos otras funciones adicionales
        render_js += ['moment', 'md5']

        return render(request, 'dashboard.html', {
            'render_js': render_js,
            'sponsors': TRIBUS_SPONSORS,
        })
    else:
        signupform = SignupForm()
        return render(request, 'index.html', {
            'signupform': signupform,
            'sponsors': TRIBUS_SPONSORS,
        })


def search(request):
    context = {}
    query = {}

    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.sanitize', 'angular.resource',
                    'angular.bootstrap']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                    'elements.angular', 'search.angular',
                    'navbar.angular']

    context["render_js"] = render_js

    if request.POST:
        query = request.POST.get('q', '')
    elif request.GET:
        query = request.GET.get('q', '')

    if query:
        objects = SearchQuerySet().autocomplete(autoname=query)

        if objects:
            # conducta extraña: dependiendo del modelo del primer elemento el resultado mostrado
            # por defecto puede ser un usuario o un paquete
            model_name = request.GET.get('filter', objects[0].model_name)
            sqs = objects.models(
                ContentType.objects.get(
                    model=model_name).model_class(
                    ))
            paginator = Paginator(sqs, 15)

            try:
                page = paginator.page(int(request.GET.get('page', 1)))
            except InvalidPage:
                return render(request, 'search/search.html', {})

            context["page"] = page
            context['query'] = query
            context['filter'] = model_name
        else:
            context["page"] = None
            context['query'] = query
            context['filter'] = None

    return render(request, 'search/search.html', context)
