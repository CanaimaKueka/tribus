#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import CASCADE
from mongoengine import Document, EmbeddedDocument
from mongoengine import (IntField, EmailField, StringField, DateTimeField,
    ListField, ReferenceField, EmbeddedDocumentField, ObjectIdField)


class Trib(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)
    author_email= EmailField(max_length=200, required=True)
    trib_content = StringField(max_length=200, required=True)
    trib_pub_date = StringField(required=True)


class Comment(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)
    author_email= EmailField(max_length=200, required=True)
    comment_content = StringField(max_length=200, required=True)
    comment_pub_date = StringField(required=True)
    trib_id = ObjectIdField()