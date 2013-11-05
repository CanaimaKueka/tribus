#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import RegexField, Textarea, HiddenInput
from django.utils.translation import ugettext_lazy as _

from mongodbforms import DocumentForm
from tribus.web.documents import Trib

class TribForm(DocumentForm):
    class Meta:
        document = Trib
        widgets = {
            'trib_content': Textarea(attrs={'placeholder': _('What are you doing?'),
                                            'class': 'action_textarea autosize expand',
                                            'ng-model': 'trib_content',
                                            }),
        }


    # author_id = IntField()
    # author_username = StringField(max_length=200, required=True)
    # author_first_name = StringField(max_length=200, required=True)
    # author_last_name = StringField(max_length=200, required=True)
    # author_email= EmailField(max_length=200, required=True)
    # trib_content = StringField(max_length=200, required=True)
    # trib_pub_date = DateTimeField(required=True)
    # trib_content = RegexField(label=_('New Trib'), required=True,
    #                               regex=r'^[.*]+$', widget=Textarea(
    #                                 attrs={
    #                                     'placeholder': _('What are you doing?'),
    #                                     'class': 'action_textarea autosize expand',
    #                                     'ng-model': 'trib_content',
    #                                 }),
    #                               max_length=200
    #                               )
