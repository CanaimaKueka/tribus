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

from django.utils.html import strip_tags
from mongodbforms import DocumentForm
from tribus.web.documents import Trib, Comment

class TribForm(DocumentForm):
    class Meta:
        document = Trib

    def clean(self):
        cleaned_data = super(TribForm, self).clean()
        
        for key in cleaned_data.keys():
            cleaned_data[key] = strip_tags(cleaned_data[key])
        return cleaned_data

class CommentForm(DocumentForm):
    class Meta:
        document = Comment

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        
        for key in cleaned_data.keys():
            cleaned_data[key] = strip_tags(cleaned_data[key])

        return cleaned_data