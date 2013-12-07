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
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.http import base36_to_int
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from registration import signals
from registration.backends.default.views import ActivationView as BaseActivationView
from registration.backends.default.views import RegistrationView as BaseRegistrationView

from tribus.web.registration.ldap.utils import create_ldap_user
from tribus.web.registration.forms import SignupForm, SetPasswordForm
from tribus.web.registration.models import TribusRegistrationProfile
from tribus.web.registration.ldap.models import LdapUser


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


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel._default_manager.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
        'uid': uidb36,
        'token': token
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
