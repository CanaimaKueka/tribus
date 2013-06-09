#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.conf import settings
from tribus.core.models import *
from tribus.core.forms import LoginForm

def Init(request):
    loginform = LoginForm()

    loginform.fields['username'].widget.attrs = {
    		'placeholder': 'Enter your username',
    		'class': 'input-large',
    		'autofocus': 'autofocus'
    		}
    loginform.fields['username'].max_length = 100
    loginform.fields['username'].label = ''

    loginform.fields['password'].widget.attrs = {
    		'placeholder': 'Enter your password',
    		'class': 'input-large'
    		}
    loginform.fields['password'].max_length = 100
    loginform.fields['password'].label = ''

    data = { 'loginform': loginform }
    context = RequestContext(request)
    return render_to_response('init.html', data, context)

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
                    return HttpResponseRedirect('/i/')
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

def Tour(request):
    data = {}
    context = RequestContext(request)
    return render_to_response('tour.html', data, context)
