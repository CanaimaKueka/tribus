#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongodbforms import DocumentForm
from tribus.web.documents import Trib

class TribForm(DocumentForm):
    class Meta:
        document = Trib