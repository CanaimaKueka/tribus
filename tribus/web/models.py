#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


from django.db.models import (Model, OneToOneField, CharField, ManyToManyField)
from mongoengine import (Document, IntField, StringField, DateTimeField,
    ListField, ReferenceField, CASCADE)

class UserProfile(User):

    user = OneToOneField(User, related_name='profile_user', primary_key=True, parent_link=True)
    followers = ManyToManyField(User, related_name='profile_followers')
    follows = ManyToManyField(User, related_name='profile_follows')
    description = CharField(max_length=160)
    location = CharField(max_length=50)

    def __unicode__(self):
        return str(self.username)

def create_user_profile(sender, instance, created, **kwargs):

    try:
        UserProfile.objects.get(user=instance)
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

# def __unicode__(self):
#     return self.username

# User.add_to_class('description', models.CharField(max_length = 160, null = True, blank = True))
# User.add_to_class('location',    models.CharField(max_length = 50, null = True, blank = True))
# User.add_to_class('telefono',    models.IntegerField(null = True, blank = True))
# User.add_to_class('follows',   models.ManyToManyField('self', related_name='profile_follows'))
# User.add_to_class('followers',   models.ManyToManyField('self', related_name='profile_followers'))
# User.add_to_class('__unicode__',__unicode__)


#
# MongoDB Documents ----------------------------
#


class Trib(Document):
    author_id = IntField()
    author_username = StringField(max_length=200, required=True)
    author_first_name = StringField(max_length=200, required=True)
    author_last_name = StringField(max_length=200, required=True)
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

# class Trib(models.Model):

#     user = models.ForeignKey(User, related_name='trib_user')
#     date = models.DateTimeField()
#     content = models.CharField(max_length = 140)
#     comments = models.ForeignKey('self')
#     likes = models.ManyToManyField(User, related_name='trib_likes')
#     dislikes = models.ManyToManyField(User, related_name='trib_dislikes')

#     def __unicode__(self):
#         return self.content

#     def filter(self):
#         """Filtra XSS enlaza hashtags, menciones y enlaces """
#         t = self.contenido

#         t = t.replace('&','&amp;')
#         t = t.replace('<','&lt;')
#         t = t.replace('>','&gt;')
#         t = t.replace('\'','&#39;')
#         t = t.replace('"','&quot;')

#         hashtags = re.findall('#[a-zA-Z][a-zA-Z0-9_]*', t)
#         for hashtag in hashtags:
#             t = t.replace(hashtag, '<a href="/twitter/buscar/?%s">%s</a>' % (urlencode({'busqueda':hashtag}), hashtag))

#         links = re.findall('http\\:\\/\\/[^ ]+', t)
#         for link in links:
#             t = t.replace(link, '<a href="%s">%s</a>' % (link, link))

#         menciones = re.findall('\\@[a-zA-Z0-9_]+', t)
#         for mencion in menciones:
#             t = t.replace(mencion, '<a href="/twitter/profile/%s/">%s</a>' % (mencion[1:], mencion))

#         return t

# class Follow(models.Model):
#     fecha = models.DateTimeField()
#     activo = models.BooleanField()
#     follower = models.ForeignKey(Profile)
#     followed = models.ForeignKey(User)

# class Chat(models.Model):
#     usuario = models.ForeignKey(User)
#     mensaje = models.CharField(max_length = 200)

# class Conectado(models.Model):
#     usuario = models.ForeignKey(User)
#     tiempo = models.DecimalField(max_digits = 20, decimal_places = 5)

