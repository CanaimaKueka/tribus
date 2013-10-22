#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, hashlib
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
            u = User.objects.get(username__exact = request.user.username)
            u.description = request.POST['descripcion']
            u.location = request.POST['location']
            u.save()

            return HttpResponseRedirect('/profile')
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


def SearchProfile(request, nick):
    try:
        usuario = User.objects.get(username = nick)
    except:
        return HttpResponseRedirect('/')

    if request.user.is_authenticated():
        if request.user.username == nick:
            return HttpResponseRedirect('/profile')  
        btn_add  = False
        btn_eliminar = False
        # if request.user.user_profile.follows:
        #     if [x for x in request.user.user_profile.follows if x ==usuario]:
        #         btn_eliminar=True

        if not request.user.username == usuario.username and not btn_eliminar:
            btn_add = True

        render_js = ['jquery', 'jquery.autogrow', 'bootstrap', 'angular',
                    'angular.resource', 'angular.infinite-scroll', 'profiles.app',
                    'profiles.jquery', 'md5', 'angular-gravatar']

        render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus' ,'tribus-responsive']

        data = {"render_css": render_css ,
                "render_js":render_js,
                "user_view":usuario,
                "add":btn_add ,
                "eliminar":btn_eliminar
                }
        context = RequestContext(request)
        #modificar el template redireccion
        return render_to_response('profile/profiles_view.html', data, context)
    else:
        return HttpResponseRedirect('/')        


   
def DeleteFollow(request,nick):
    try:
        follow= User.objects.get(username = nick)
    except:
        return HttpResponseRedirect('/')
    if request.user.is_authenticated():

        usuario = User.objects.get (username = request.user.username)
        usuario.user_profile.follows.remove(follow)
        print ("borrando seguidor:")
    return HttpResponseRedirect('/profile/'+nick)


   
def AddFollow(request,nick):
    try:
        follow= User.objects.get(username = nick)
    except:
        return HttpResponseRedirect('/')
    if request.user.is_authenticated():
        usuario = User.objects.get (username = request.user.username)
        usuario.follows.add(follow)
    return HttpResponseRedirect('/profile/'+nick)




def UserProfile(request):

    render_js = ['jquery', 'jquery.autogrow', 'bootstrap', 'angular',
                    'angular.resource', 'angular.infinite-scroll', 'profiles.app',
                    'profiles.jquery', 'md5', 'angular-gravatar']

    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-ie' ,'tribus-responsive']


    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(request.user.email.lower()).hexdigest() #+ "?"
    # cambio de tamaño instanceable luego
    # gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

    data = {"render_css": render_css , "render_js":render_js , 'url': gravatar_url, 'user_view':request.user}
    context = RequestContext(request)
    


    print gravatar_url

    
    if request.user.is_authenticated():
        
        return render_to_response('profile/profiles.html', data, context)

    return HttpResponseRedirect('/')