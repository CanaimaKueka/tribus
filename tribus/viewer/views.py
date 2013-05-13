#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.conf import settings
from tribus.viewer.models import *
from tribus.viewer.forms import LoginForm

conftree = settings.CONFTREE

#class Menu(conftree, action):

#    def menulist(conftree, action):
#        for x,y in conftree[action].iteritems():
#            if x is 'url':
#                return (action,y)

#    def actionlist(self):
#        submenus = conftree[action]['submenus']
#        if submenus is not None:
#            actions = [x for x in submenus]
#            return actions

def Welcome(request):
    latest_tickets = Ticket.objects.all().order_by('-date_reported')[:6]
    latest_packages = Package.objects.all().order_by('-date_uploaded')[:6]
    latest_promotions = User.objects.all().order_by('-date_promoted')[:6]
    statistics = 'TODO'
    statistics = 'TODO'
    action_list = 'TODO'
    data = {
        'latest_tickets': latest_tickets,
        'latest_packages': latest_packages,
        'latest_promotions': latest_promotions,
        'statistics': statistics,
        'menu_list': statistics,
        'action_list': statistics,
    }
    context = RequestContext(request)
    return render_to_response('welcome.html', data, context)

def doc(request, docname):
    data = {
        'latest_tickets': latest_tickets,
        'latest_packages': latest_packages,
        'latest_promotions': latest_promotions,
        'statistics': statistics,
    }
    context = RequestContext(request)
    return render_to_response('doc.html', data, context)

def Login(request):

    def errorHandle(error):
        form = LoginForm()
        data = {
            'error' : error,
            'form' : form,
            }
        context = RequestContext(request)
        return render_to_response('login.html', data, context)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                else:
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                error = u'invalid login'
                return errorHandle(error)
        else: 
            error = u'form is invalid'
            return errorHandle(error)
    else:
        form = LoginForm()
        data = {
            'form': form,
            }
        context = RequestContext(request)
        return render_to_response('login.html', data, context)

def Logout(request):
    auth.logout(request)
    data = {}
    context = RequestContext(request)
    return render_to_response('logout.html', data, context)

def Dashboard(request):
    data = {}
    context = RequestContext(request)
    return render_to_response('dashboard.html', data, context)
