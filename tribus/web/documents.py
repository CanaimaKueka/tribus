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

from mongoengine import Document
from mongoengine import (IntField, EmailField, StringField,
                         ObjectIdField, DateTimeField)


class Trib(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)
    author_email = EmailField(max_length=200, required=True)
    trib_content = StringField(max_length=200, required=True)
    trib_pub_date = StringField(required=True)


class Comment(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)
    author_email = EmailField(max_length=200, required=True)
    comment_content = StringField(max_length=200, required=True)
    comment_pub_date = StringField(required=True)
    trib_id = ObjectIdField()
