#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    description = models.CharField(max_length = 160)
    location = models.CharField(max_length = 50)
    followers = models.ManyToManyField(User)
    follows = models.ManyToManyField(User)

    def __unicode__(self):
        return str(self.user)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Trib(models.Model):

    user = models.ForeignKey(User)
    date = models.DateTimeField()
    content = models.CharField(max_length = 140)
    comments = models.ForeignKey(Trib)
    likes = models.ManyToManyField(User)
    dislikes = models.ManyToManyField(User)

    def __unicode__(self):
        return self.content

    def filter(self):
        """Filtra XSS enlaza hashtags, menciones y enlaces """
        t = self.contenido

        t = t.replace('&','&amp;')
        t = t.replace('<','&lt;')
        t = t.replace('>','&gt;')
        t = t.replace('\'','&#39;')
        t = t.replace('"','&quot;')

        hashtags = re.findall('#[a-zA-Z][a-zA-Z0-9_]*', t)
        for hashtag in hashtags:
            t = t.replace(hashtag, '<a href="/twitter/buscar/?%s">%s</a>' % (urlencode({'busqueda':hashtag}), hashtag))

        links = re.findall('http\\:\\/\\/[^ ]+', t)
        for link in links:
            t = t.replace(link, '<a href="%s">%s</a>' % (link, link))

        menciones = re.findall('\\@[a-zA-Z0-9_]+', t)
        for mencion in menciones:
            t = t.replace(mencion, '<a href="/twitter/profile/%s/">%s</a>' % (mencion[1:], mencion))

        return t

class Follow(models.Model):
    fecha = models.DateTimeField()
    activo = models.BooleanField()
    follower = models.ForeignKey(Profile)
    followed = models.ForeignKey(User)

class Chat(models.Model):
    usuario = models.ForeignKey(User)
    mensaje = models.CharField(max_length = 200)

class Conectado(models.Model):
    usuario = models.ForeignKey(User)
    tiempo = models.DecimalField(max_digits = 20, decimal_places = 5)

