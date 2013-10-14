#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import (Document, IntField, EmailField, StringField, DateTimeField,
    ListField, ReferenceField, CASCADE)


class Trib(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)

    author_email= EmailField(max_length=200, required=True)
    trib_content = StringField(max_length=200, required=True)
    trib_pub_date = DateTimeField(required=True)
    retribs = ListField(IntField())


class ReTrib(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)

    trib = ReferenceField(Trib, reverse_delete_rule=CASCADE)
    trib_pub_date = DateTimeField()