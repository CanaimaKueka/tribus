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


from tastypie.validation import Validation as BaseValidation

from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm

from mongodbforms.documents import document_to_dict


class DocumentFormValidation(BaseValidation):

    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **DOES NOT** alter the data sent, only verifies it. If you
    want to alter the data, please use the ``CleanedDataFormValidation`` class
    instead.

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """

    def __init__(self, **kwargs):
        if not 'form_class' in kwargs:
            raise ImproperlyConfigured(
                "You must provide a 'form_class' to 'FormValidation' classes.")

        self.form_class = kwargs.pop('form_class')
        super(DocumentFormValidation, self).__init__(**kwargs)

    def form_args(self, bundle):
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}

        kwargs = {'data': {}}

        if hasattr(bundle.obj, 'pk'):
            if issubclass(self.form_class, ModelForm):
                kwargs['instance'] = bundle.obj
            kwargs['data'] = document_to_dict(bundle.obj)

        kwargs['data'].update(data)

        return kwargs

    def is_valid(self, bundle, request=None):
        """
        Performs a check on ``bundle.data``to ensure it is valid.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """

        form = self.form_class(**self.form_args(bundle))

        if form.is_valid():
            return {}

        # The data is invalid. Let's collect all the error messages & return
        # them.
        return form.errors
