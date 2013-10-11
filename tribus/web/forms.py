#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import RegexField, Textarea
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm

class TribForm(AuthenticationForm):

    trib = RegexField(label=_('New Trib'), required=True,
                      regex=r'^[\w.@+-]+$', widget=Textarea(
                        attrs={
                            'placeholder': _('Enter your username'),
                            'class': 'input-xlarge'
                        }),
                      max_length=30, error_messages = {
                        'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
                      })