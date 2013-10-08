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

from tribus.web.user.models import LdapUser


class data_change(Form):
	required_css_class = 'required'
	descripcion = forms.RegexField(
	                                label = _('Descriccion'), required = False,
	                                regex = r'^[\w.@+-]+$',
	                                widget = forms.Textarea(
	                                    attrs = {
	                                        'placeholder': _('coloca tu descripcion'),
	                                        'class': 'input-xlarge'
	                                    }
	                                ),
	                                max_length = 254,
	                                error_messages = {
	                                'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
	                                }
	                            )

	direction = forms.RegexField(
	                                label = _('Direccion'), required = False,
	                                regex = r'^[\w.@+-]+$',
	                                widget = forms.Textarea(
	                                    attrs = {
	                                        'placeholder': _('Coloca tu direccion'),
	                                        'class': 'input-xlarge'
	                                    }
	                                ),
	                                max_length = 254,
	                                error_messages = {
	                                'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
	                                }
	                            )

	location = forms.RegexField(
	                                label = _('localidad'), required = False,
	                                regex = r'^[\w.@+-]+$',
	                                widget = forms.Textarea(
	                                    attrs = {
	                                        'placeholder': _('Coloca tu Localidad'),

	                                        'class': 'input-xlarge'
	                                    }
	                                ),
	                                max_length = 254,
	                                error_messages = {
	                                'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
	                                }
	                            )

