#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from tribus.web.profile.forms import data_change
from tribus.web.user.pipeline import edit_ldap_user

def SearchProfile(request, nick):
    try:
        user = User.objects.get(username = request.user.username)
    except:
        user = None
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

    context = {"render_css": render_css ,
            "render_js":render_js,
            "user": user,
            "user_view":user_view,            
            }
            
    context = RequestContext(request)
    #modificar el template redireccion
    return render(request,'profile/profiles_view.html',context)



def UserProfile(request):

    render_js = ['jquery', 'jquery.autogrow',  'jquery.timeago','bootstrap', 'angular',
                    'angular.resource', 'angular.infinite-scroll', 'profiles.app', 
                    'profiles.jquery', 'navbar.app', 'navbar.jquery', 'md5','angular-gravatar']

    render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-ie' ,'tribus-responsive']

    context = {"render_css": render_css , "render_js":render_js , 'user_view':request.user}
    
    if request.user.is_authenticated():
        if request.method == "POST":
            u = User.objects.get(username__exact = request.user.username)
            u.description = request.POST['descripcion']
            u.email = request.POST['email']
            u.save()
            edit_ldap_user(u)

            return HttpResponseRedirect('/profile')
        else:
            form = data_change()
            context['editForm'] = form
            return render(request,'profile/profiles.html', context)

    return HttpResponseRedirect('/')