#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from tribus.web.profile.forms import data_change


def EditUserProfile(request):
    render_js = ['jquery', 'jquery.autogrow',  'jquery.timeago','bootstrap', 'angular',
                'angular.resource', 'angular.infinite-scroll', 'profiles.app', 
                'profiles.jquery', 'navbar.app', 'navbar.jquery', 'md5','angular-gravatar']

                
    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                'bootstrap-responsive', 'tribus', 'tribus-responsive']


            # ['jquery', 'jquery.autogrow', 'bootstrap', 'angular',
            #         'angular.resource', 'angular.infinite-scroll',  
            #         'profiles.app','profiles.jquery', 'navbar.app',
            #         'navbar.jquery','md5', 'angular-gravatar']                        

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
    user = User.objects.filter(username =  'luis')
    try:
        user_view = User.objects.get(username = nick)
    except:
        return HttpResponseRedirect('/profile')

    if request.user.username == nick:
        return HttpResponseRedirect('/profile')  

        # if request.user.user_profile.follows:
        #     if [x for x in request.user.user_profile.follows if x ==usuario]:
        #         btn_eliminar=True



    render_js = ['jquery', 'jquery.autogrow',  'jquery.timeago','bootstrap', 'angular',
                'angular.resource', 'angular.infinite-scroll', 'profiles.app', 
                'profiles.jquery', 'navbar.app', 'navbar.jquery', 'md5','angular-gravatar']
    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                    'bootstrap-responsive', 'tribus' ,'tribus-responsive']

    data = {"render_css": render_css ,
            "render_js":render_js,
            "user": user,
            "user_view":user_view,            
            }
    context = RequestContext(request)
    #modificar el template redireccion
    return render_to_response('profile/profiles_view.html', data, context)



def UserProfile(request):

    render_js = ['jquery', 'jquery.autogrow',  'jquery.timeago','bootstrap', 'angular',
                    'angular.resource', 'angular.infinite-scroll', 'profiles.app', 
                    'profiles.jquery', 'navbar.app', 'navbar.jquery', 'md5','angular-gravatar']

    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-ie' ,'tribus-responsive']

    data = {"render_css": render_css , "render_js":render_js , 'user_view':request.user}
    context = RequestContext(request)
    
    if request.user.is_authenticated():
        
        return render_to_response('profile/profiles.html', data, context)

    return HttpResponseRedirect('/')