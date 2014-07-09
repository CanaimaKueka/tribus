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

from lxml.html import document_fromstring
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags, escape
from django.utils.translation import ugettext_lazy as _

from tribus.web.models import Trib, Comment


class TribForm(ModelForm):

    class Meta:
        model = Trib
        fields = ['trib_content']

    def clean(self):
        cleaned_data = super(TribForm, self).clean()

        for key in cleaned_data.keys():
            stripped_data = strip_tags(cleaned_data[key])
            if unicode(stripped_data).strip():
                parsed_data = document_fromstring(stripped_data).text_content()
                if unicode(parsed_data).strip():
                    cleaned_data[key] = escape(parsed_data)
                else:
                    raise ValidationError(_('Enter a valid value.'))
            else:
                raise ValidationError(_('Enter a valid value.'))
        return cleaned_data


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_content']

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        for key in cleaned_data.keys():
            stripped_data = strip_tags(cleaned_data[key])
            if unicode(stripped_data).strip():
                parsed_data = document_fromstring(stripped_data).text_content()
                if unicode(parsed_data).strip():
                    cleaned_data[key] = escape(parsed_data)
                else:
                    raise ValidationError(_('Enter a valid value.'))
            else:
                raise ValidationError(_('Enter a valid value.'))
        return cleaned_data