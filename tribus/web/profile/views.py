#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from tribus.web.profile.forms import data_change
from tribus.web.registration.ldap.utils import edit_ldap_user

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

    render_js = ['jquery', 'jquery.autogrow', 'jquery.timeago', 'jquery.bootstrap-growl', 'jquery.bootstrap',
                    'md5','angular', 'angular.resource', 'angular.infinite-scroll','services.angular' , 'controllers.angular', 
                    'navbar.angular', 'navbar.jquery',
                    'profiles.angular', 'dashboard.jquery'
                    
                    ]

    return render(request,'profile/profiles_view.html', {
            'render_js': render_js,
            'user': user,
            'user_view': user_view,            
            })



def UserProfile(request):

    render_js = ['jquery', 'jquery.autogrow', 'jquery.timeago', 'jquery.bootstrap-growl', 'jquery.bootstrap',
                    'md5','angular', 'angular.resource', 'angular.infinite-scroll','services.angular' ,'controllers.angular', 
                    'navbar.angular', 'navbar.jquery',
                    'profiles.angular', 'dashboard.jquery',
                    ]

    if request.user.is_authenticated():
        if request.method == "POST":
            u = User.objects.get(username__exact = request.user.username)
            u.description = request.POST['descripcion']
            # u.email = request.POST['email']
            u.save()
            edit_ldap_user(u)
            return HttpResponseRedirect('/profile')

        else:
            form = data_change()
            return render(request,'profile/profiles.html', {
                'render_js': render_js,
                'user_view': request.user,
                'editForm': form
                })

    return HttpResponseRedirect('/')
