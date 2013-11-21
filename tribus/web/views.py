#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from tribus.web.registration.forms import SignupForm
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.contrib.contenttypes.models import ContentType

def tour(request):
    return render('tour.html', {})


def index(request):
    if request.user.is_authenticated():
        render_js = ['jquery', 'jquery.autogrow', 'jquery.timeago', 'jquery.bootstrap-growl', 'jquery.bootstrap',
                        'angular', 'angular.resource', 'angular.infinite-scroll',
                        'dashboard.angular' ,'services.angular', 'controllers.angular',  'dashboard.jquery',
                        'navbar.angular', 'navbar.jquery',
                        'md5']

        return render(request, 'dashboard.html', {
            'render_js': render_js,
            })
    else:
        signupform = SignupForm()
        return render(request, 'index.html', {
            'signupform': signupform
            })


def tribus_search(request):
    context={}
    render_js = ['jquery', 'jquery.autogrow', 'jquery.bootstrap', 'angular', 'angular.resource','services.angular' ,'controllers.angular', 
                 'navbar.angular',  'navbar.jquery', 'md5']
    context ["render_js"]= render_js
    if request.GET:
        query = request.GET.get('q', '')
        objects = SearchQuerySet().filter(autoname = query)
        if objects:
            model_name = request.GET.get('filter', objects[0].model_name)
            sqs = objects.models(ContentType.objects.get(model=model_name).model_class())
            print sqs
            #print len(sqs)
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