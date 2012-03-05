#!/usr/bin/env python
# -*- coding: utf-8 -*-

from viewer.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.conf import settings

conftree = settings.CONFTREE

class Menu(conftree, action):

    def menulist(conftree, action):
        for x,y in conftree[action].iteritems():
            if x is 'url':
                return (action,y)

    def actionlist(self):
        submenus = conftree[action]['submenus']
        if submenus is not None:
            actions = [x for x in submenus]
            return actions
            
def welcome(request):
    latest_tickets = Ticket.objects.all().order_by('-date_reported')[:6]
    latest_packages = Package.objects.all().order_by('-date_uploaded')[:6]
    latest_promotions = User.objects.all().order_by('-date_promoted')[:6]
    statistics = 'TODO'
    statistics = 'TODO'
    action_list = 'TODO'
    pagevars = {
        'latest_tickets': latest_tickets,
        'latest_packages': latest_packages,
        'latest_promotions': latest_promotions,
        'statistics': statistics,
        'menu_list': statistics,
        'action_list': statistics,
    }
    context_instance = RequestContext(request)
    return render_to_response('welcome.html', pagevars, context_instance)

def doc(request, docname):
    pagevars = {
        'latest_tickets': latest_tickets,
        'latest_packages': latest_packages,
        'latest_promotions': latest_promotions,
        'statistics': statistics,
    }
    context_instance = RequestContext(request)
    return render_to_response('doc.html', pagevars, context_instance)

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/profile/')

        else:
            return HttpResponseRedirect('/error/auth/')

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
