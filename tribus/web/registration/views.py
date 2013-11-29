#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Views which allow users to create and activate accounts.

"""

from django.contrib.auth.views import login as django_login
from django.contrib.sites.models import Site, RequestSite

from registration import signals
from registration.backends.default.views import ActivationView as BaseActivationView
from registration.backends.default.views import RegistrationView as BaseRegistrationView

from tribus.web.registration.ldap.utils import create_ldap_user
from tribus.web.registration.forms import SignupForm
from tribus.web.registration.models import TribusRegistrationProfile

class RegistrationView(BaseRegistrationView):

    form_class = SignupForm

    def register(self, request, **cleaned_data):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = TribusRegistrationProfile.objects.create_inactive_user(
                    cleaned_data['username'], cleaned_data['first_name'],
                    cleaned_data['last_name'], cleaned_data['email'],
                    cleaned_data['password1'], site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, request, user):
        return ('registration_signup_complete', (), {})


class ActivationView(BaseActivationView):
    def activate(self, request, activation_key):
        activated_user = TribusRegistrationProfile.objects.activate_user(activation_key)

        if activated_user:
            ldap_user = create_ldap_user(activated_user)
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})


def login(request, *args, **kwargs):
    if request.method == 'POST':

        # If we have 'remember_me' checked, user session
        # will never expire
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    # Dispatch to Django's built-in login view
    return django_login(request, *args, **kwargs)