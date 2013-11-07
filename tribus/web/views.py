#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from tribus.web.user.forms import SignupForm

from tribus.web.forms import TribForm

from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.views import SearchView
from django.core.paginator import Paginator, InvalidPage
from django.http.response import Http404
from django.conf import settings
from haystack.forms import ModelSearchForm
from django.template.context import RequestContext
RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


def tour(request):
    return render('tour.html', {})


def index(request):
    if request.user.is_authenticated():
        render_js = ['jquery', 'jquery.autogrow', 'jquery.timeago', 'jquery.bootstrap-growl', 'bootstrap', 'angular',
                        'angular.resource', 'angular.infinite-scroll', 'dashboard.app',
                        'dashboard.jquery', 'navbar.app', 'navbar.jquery', 'md5', 'angular-gravatar']

        return render(request, 'dashboard.html', {
            'render_js': render_js,
            })
    else:
        signupform = SignupForm()
        signupform.fields['username'].widget.attrs['class'] = 'input-large'
        signupform.fields['first_name'].widget.attrs['class'] = 'input-small'
        signupform.fields['last_name'].widget.attrs['class'] = 'input-small'
        signupform.fields['email'].widget.attrs['class'] = 'input-large'
        signupform.fields['password'].widget.attrs['class'] = 'input-large'

        return render(request, 'index.html', {
            'signupform': signupform
            })
        
def tribus_search(request):
    context={}
    render_js = ['jquery', 'jquery.autogrow', 'bootstrap', 'angular', 'angular.resource', 
                 'angular.infinite-scroll', 'dashboard.app', 'dashboard.jquery',
                 'navbar.app', 'navbar.jquery', 'md5', 'angular-gravatar']
    context ["render_js"]= render_js
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = query
        sqs = SearchQuerySet().load_all().filter(autoname = query)
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        context["page"]= page
        
    return render(request, 'search/search.html', context)
