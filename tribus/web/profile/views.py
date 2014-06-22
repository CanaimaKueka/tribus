#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from tribus.web.profile.forms import data_change
from tribus.web.registration.ldap.utils import edit_ldap_user
from waffle.decorators import waffle_switch

@waffle_switch('profile')
def SearchProfile(request, nick):
    """
    Vista que busca el perfil de un usuario si existe y lo redirecciona a su muro,
    sino redirecciona al perfil de usuario logeado. En caso de que no este logueado
    redirecciona a la pagina principal.
    
    @param request: request 
    @param nick: string que representa el username del usuario a quien buscas.  
    """
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=request.user.username)
        except:
            user = None
        try:
            user_view = User.objects.get(username=nick)
        except:
            return HttpResponseRedirect('/profile')

        if request.user.username == nick:
            return HttpResponseRedirect('/profile')

        # Cargamos la librería AngujarJS junto con sus plugins
        render_js = ['angular', 'angular.sanitize', 'angular.resource',
                     'angular.infinite-scroll', 'angular.bootstrap',
                     'angular.moment']

        # Cargamos las funciones de Tribus para AngularJS
        render_js += ['controllers.angular', 'services.angular',
                      'elements.angular', 'profiles.angular',
                      'navbar.angular']

        # Cargamos otras funciones adicionales
        render_js += ['moment', 'md5']

        return render(request, 'profile/profiles_view.html', {
            'render_js': render_js,
            'user': user,
            'user_view': user_view,
        })
    return HttpResponseRedirect("/")


@waffle_switch('profile')
def UserProfile(request):
    """
    vista que verifica que maneja la peticion del perfil del usuario logueado,
    incluyendo el manejo del formulario de cambio de datos.
    """

    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = ['angular', 'angular.sanitize', 'angular.resource',
                 'angular.infinite-scroll', 'angular.bootstrap',
                 'angular.moment']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'profiles.angular',
                  'navbar.angular']

    # Cargamos otras funciones adicionales
    render_js += ['moment', 'md5']

    if request.user.is_authenticated():
        if request.method == "POST":
            u = User.objects.get(username__exact = request.user.username)
            u.description  = request.POST['descripcion']
            if 'emailVisible' in request.POST:
                u.emailVisible = request.POST['emailVisible']
            else:
                u.emailVisible = False
            #u.emailVisible = request.POST['emailVisible']
            # u.email = request.POST['email']
            u.save()
            edit_ldap_user(u)
            return HttpResponseRedirect('/profile')

        else:
            form = data_change()
            return render(request, 'profile/profiles.html', {
                'render_js': render_js,
                'user_view': request.user,
                'editForm': form
            })

    return HttpResponseRedirect('/')
