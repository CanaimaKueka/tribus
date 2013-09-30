#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from tribus.web.profile.forms import data_change





def EditUserProfile(request):
    render_js = ['jquery', 'bootstrap']
    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']

    data = {"render_css": render_css , "render_js":render_js}
    context = RequestContext(request)
    
        # aqui debe estar la logica del los formularios cn su valudacion


    if request.user.is_authenticated():
        if request.method == "POST":
            print (dir (request.POST))
            u = User.objects.get(username__exact = request.user.username)
            print ("esto es la descripcion:",u.description)
            u.description = request.POST['descripcion']
            u.location = request.POST['location']
            u.save()

            return HttpResponseRedirect('/profile')
            #return render_to_response('profile/profiles.html', data, context)

        else:
            form = data_change()
            data['editForm'] = form
            return render_to_response('profile/edit.html', data, context)


    return HttpResponseRedirect('/')


def ChangePassword(request):
    render_js = ['jquery', 'bootstrap']
    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']

    data = {"render_css": render_css , "render_js":render_js}
    context = RequestContext(request)
    
        # aqui debe estar la logica del los formularios cn su valudacion


    if request.user.is_authenticated():
        
        return render_to_response('profile/change_password.html', data, context)

    return HttpResponseRedirect('/')


def UserProfile(request):
    render_js = ['jquery', 'bootstrap']
    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']

    data = {"render_css": render_css , "render_js":render_js}
    context = RequestContext(request)

    if request.user.is_authenticated():
        
        return render_to_response('profile/profiles.html', data, context)

    return HttpResponseRedirect('/')