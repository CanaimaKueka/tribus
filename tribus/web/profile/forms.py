#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import random
import string

from django import forms
from django.forms import Form
from django.utils.datastructures import SortedDict
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm as BasePasswordResetForm, SetPasswordForm as BaseSetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tribus.web.registration.ldap.models import LdapUser


class data_change(Form):
	required_css_class = 'required'
	descripcion = forms.RegexField(
	                                label = _('Descripcion'), required = False,
	                                regex = r'^[\w.@+-]+$',
	                                widget = forms.Textarea(
	                                    attrs = {
	                                        'class': 'input-largue'
	                                    }
	                                ),
	                                max_length = 254,
	                                error_messages = {
	                                'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
	                                }
	                            )

	email = forms.EmailField(label = _('email'), required = False)