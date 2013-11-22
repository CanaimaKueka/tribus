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

from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from tribus.web.cloud.models import Package
from django.contrib.auth.models import User

class PackageIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    name = indexes.CharField(model_attr='Package')
    autoname = indexes.EdgeNgramField(model_attr='Package')
    description = indexes.CharField(model_attr='Description', null = True)
    
    def get_model(self):
        return Package
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
class UserIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True)
    fullname = indexes.EdgeNgramField(model_attr='get_full_name')
    username = indexes.EdgeNgramField(model_attr='username')
    autoname = indexes.EdgeNgramField(model_attr='username', use_template = True)
    description = indexes.CharField(model_attr='description', null = True)
    
    def get_model(self):
        return User
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()