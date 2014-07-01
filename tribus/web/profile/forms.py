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
"""


from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _


class data_change(Form):

    required_css_class = 'required'
    descripcion = forms.RegexField(
        label=_('Description'), required=False, regex=r'^[\w.@+-]+$',
        max_length=254, widget=forms.Textarea(attrs={'class': 'input-large',
                                                     'ng-maxlength': '20'}),
        error_messages={'invalid': _(('This value may contain '
                                      'only letters, numbers '
                                      'and @/./+/-/_ '
                                      'characters.'))}
        )
    emailVisible = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'checkForm'})
        )
