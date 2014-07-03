#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""

import base64
import hashlib
import random
import string

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template import loader
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django import forms
from django.forms import Form
from django.utils.datastructures import SortedDict
from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordResetForm as BasePasswordResetForm,
                                       SetPasswordForm as BaseSetPasswordForm)
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tribus.web.registration.ldap.models import LdapUser


class LoginForm(AuthenticationForm):

    """
    Subclass of Django ``AuthenticationForm`` which adds a remember me
    checkbox.
    """

    username = forms.RegexField(
        label=_('Username'), required=True,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs={
                'placeholder':
                _('Enter your username'),
                'class': 'input-block padding-2p'
            }
        ),
        max_length=30,
        error_messages={
            'invalid':
            _(
                "This value may contain only letters, numbers and @/./+/-/_ characters.")
        }
    )

    password = forms.CharField(
        label=_('Password'), required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':
                _('Enter your password'),
                'class': 'input-block padding-2p'
            }
        )
    )

    remember_me = forms.BooleanField(
        label=_('Remember my session'),
        initial=False,
        required=False
    )


class SignupForm(Form):

    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    username = forms.RegexField(
        label=_('Username'), required=True,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs={
                'placeholder':
                _('Pick a username'),
                'class': 'input-block padding-2p'
            }
        ),
        max_length=30,
        error_messages={
            'invalid':
            _(
                "This value may contain only letters, numbers and @/./+/-/_ characters.")
        }
    )

    first_name = forms.RegexField(
        label=_('First name'), required=True,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First name'),
                'class': 'input-block padding-4p'
            }
        ),
        max_length=30,
        error_messages={
            'invalid':
            _(
                "This value may contain only letters, numbers and @/./+/-/_ characters.")
        }
    )

    last_name = forms.RegexField(
        label=_('Last name'), required=True,
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last name'),
                'class': 'input-block padding-4p'
            }
        ),
        max_length=30,
        error_messages={
            'invalid':
            _(
                "This value may contain only letters, numbers and @/./+/-/_ characters.")
        }
    )

    email = forms.EmailField(
        label=_('Email'), required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':
                _('Enter a valid email'),
                'class': 'input-block padding-2p'
            }
        ),
        max_length=254
    )

    password1 = forms.CharField(
        label=_('Password'), required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':
                _('Create a password'),
                'class': 'input-block padding-2p'
            }
        )
    )

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existingldap = LdapUser.objects.filter(
            username=self.cleaned_data['username'])
        if existingldap.exists():
            raise forms.ValidationError(
                _("A user with that username already exists."))
        else:
            existingdb = User.objects.filter(
                username__iexact=self.cleaned_data['username'])
            if existingdb.exists():
                existingdb.delete()
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existingldap = LdapUser.objects.filter(
            email=self.cleaned_data['email'])
        if existingldap.exists():
            raise forms.ValidationError(
                _("A user with that email already exists."))
        else:
            existingdb = User.objects.filter(
                email__iexact=self.cleaned_data['email'])
            if existingdb.exists():
                existingdb.delete()
            return self.cleaned_data['email']


class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label=_('Email'), required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':
                _('Enter a valid email'),
                'class': 'input-block padding-2p'
            }
        ),
        max_length=254
    )

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = LdapUser.objects.filter(email__exact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.password for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD_PREFIX)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.html',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            obj, created = User.objects.get_or_create(username=user.username,
                                                      email=user.email,
                                                      password=user.password)
            if created:
                obj.is_active = True
                obj.last_login = timezone.now()
                obj.save()

            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            c = {
                'email': obj.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(obj.pk),
                'username': obj.username.encode('utf-8'),
                'first_name': obj.first_name.encode('utf-8'),
                'token': token_generator.make_token(obj),
                'protocol': use_https and 'https' or 'http',
            }

            subject = loader.render_to_string(subject_template_name, c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [obj.email])


class SetPasswordForm(BaseSetPasswordForm):

    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    new_password1 = forms.CharField(
        label=_('Password'), required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':
                _('Create a new password'),
                'class': 'input-block padding-2p'
            }
        )
    )

    new_password2 = forms.CharField(
        label=_('Password (repeat)'), required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':
                _('Repeat your new password'),
                'class': 'input-block padding-2p'
            }
        )
    )

    def save(self, commit=True):

        try:
            u = LdapUser.objects.get(username=self.user.username)
        except LdapUser.DoesNotExist:
            raise forms.ValidationError(
                _("A user with that username already exists."))
        else:
            self.user.set_password(self.cleaned_data['new_password1'])

            if commit:
                self.user.save()

            u.password = self.user.password
            u.save()

            return self.user


class PasswordChangeForm(SetPasswordForm):

    """
    A form that lets a user change his/her password by entering
    their old password.
    """

    old_password = forms.CharField(
        label=_('Old password'), required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':
                _('Enter your old password'),
                'class': 'input-block padding-2p'
            }
        )
    )

PasswordChangeForm.base_fields = SortedDict([
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
])
