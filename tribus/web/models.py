#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from django.db import models
from django.contrib.auth.models import User
from ldapdb.models import fields
import ldapdb.models
from django.conf import settings

class Profile(models.Model):
    user = models.ForeignKey(User)
    frase = models.CharField(max_length = 160)
    ubicacion = models.CharField(max_length = 50)
    avatar = models.CharField(max_length = 256)

    def __unicode__(self):
        return str(self.user)


# This class comes from django-ldapdb's examples
# https://github.com/jlaine/django-ldapdb
class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """

    class Meta:
        managed = False

    # related_name tip from
    # http://igorsobreira.com/2010/12/11/extending-user-model-in-django.html
    # user = models.OneToOneField(User)
    base_dn = settings.AUTH_LDAP_BASE
    object_classes = [
       'posixAccount', 'shadowAccount', 'inetOrgPerson',
       'top', 'person', 'organizationalPerson'
       ]

    first_name = fields.CharField(db_column='givenName')
    last_name = fields.CharField(db_column='sn')
    full_name = fields.CharField(db_column='cn')
    email = fields.CharField(db_column='mail')
    username = fields.CharField(db_column='uid', primary_key=True)
    password = fields.CharField(db_column='userPassword')
    uid = fields.IntegerField(db_column='uidNumber', unique=True)
    group = fields.IntegerField(db_column='gidNumber')
    home_directory = fields.CharField(db_column='homeDirectory')
    login_shell = fields.CharField(db_column='loginShell', default='/bin/bash')
    description = fields.CharField(db_column='description')

    def __str__(self):
       return self.uid

    def __unicode__(self):
       return self.full_name

    # post_save tip from
    # http://blog.tivix.com/2012/01/06/extending-user-model-in-django/
    # def create_ldap_user(sender, instance, created, **kwargs):
    #     if created:
    #         profile, created = self.objects.get_or_create(user=instance)

#
# Model Signaling --------------------------------------------------------------
#
# models.signals.post_save.connect(LdapUser.create_ldap_user, sender=User)

# Create your models here.
class Tweet(models.Model):
    def __unicode__(self):
        return self.contenido
    user = models.ForeignKey(User)
    fecha = models.DateTimeField()
    contenido = models.CharField(max_length = 140)
    retweet = models.BooleanField(default = False, blank = True)
    activo = models.BooleanField(default  =True)
    respuesta = models.IntegerField(null = True, blank = True)
    def filtrar(self):
        """Filtra XSS enlaza hashtags, menciones y enlaces """
        t = self.contenido

        #Anti XSS
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


# class Repository(models.Model):
#     name = models.CharField(max_length=60)
#     branches = models.CharField(max_length=60)
#     sections = models.CharField(max_length=60)
#     address = models.URLField(max_length=60)
#     source = models.BooleanField()

#     def __unicode__(self):
#         return self.name

# class Distribution(models.Model):
#     name = models.CharField(max_length=60)
#     address = models.URLField(max_length=60)
#     repos = models.ForeignKey(Repository)
#     bugtracker = models.URLField(max_length=60)
#     wiki = models.URLField(max_length=60)
#     devlist = models.EmailField(max_length=60)
#     disclist = models.EmailField(max_length=60)
#     suplist = models.EmailField(max_length=60)
    
#     def __unicode__(self):
#         return self.name

# class UserProfile(models.Model):
#     user = models.ForeignKey(User, unique=True)
#     role = models.CharField(max_length=60)
#     gnupg = models.CharField(max_length=60)
#     appadmin = models.BooleanField()
#     date_promoted = models.DateField()

#     def __unicode__(self):
#         return self.username

# class Package(models.Model):
#     maintainer = models.ForeignKey(UserProfile)
#     name = models.SlugField(max_length=255)
#     debianversion = models.CharField(max_length=60)
#     upstreamversion = models.CharField(max_length=60)
#     origin = models.ForeignKey(Repository)
#     branch = models.CharField(max_length=60)
#     depends = models.CharField(max_length=60)
#     recommends = models.CharField(max_length=60)
#     suggests = models.CharField(max_length=60)
#     conflicts = models.CharField(max_length=60)
#     date_uploaded = models.DateField()

#     def __unicode__(self):
#         return self.name

# class Ticket(models.Model):
#     title = models.CharField(max_length=255)
#     number = models.IntegerField()
#     package = models.ForeignKey(Package)
#     assigned_to = models.ForeignKey(UserProfile)
#     distro = models.ForeignKey(Distribution)
#     date_reported = models.DateField()
#     status = models.CharField(max_length=255)

#     def __unicode__(self):
#         return self.number

# class Comment(models.Model):
#     title = models.CharField(max_length=255)
#     number = models.IntegerField()
#     package = models.ForeignKey(Package)
#     assigned_to = models.ForeignKey(UserProfile)
#     distro = models.ForeignKey(Distribution)
#     date_reported = models.DateField()
#     status = models.CharField(max_length=255)

#     def __unicode__(self):
#         return self.number

# class Upload(models.Model):
#     maintainer = models.ForeignKey(UserProfile)
#     name = models.SlugField(max_length=255)
#     debianversion = models.CharField(max_length=60)
#     upstreamversion = models.CharField(max_length=60)
#     origin = models.ForeignKey(Repository)
#     branch = models.CharField(max_length=60)
#     upload_date = models.DateField()

#     def __unicode__(self):
#         return self.name

# class Team(models.Model):
#     maintainer = models.ForeignKey(UserProfile)
#     name = models.SlugField(max_length=255)
#     debianversion = models.CharField(max_length=60)
#     upstreamversion = models.CharField(max_length=60)
#     origin = models.ForeignKey(Repository)
#     branch = models.CharField(max_length=60)
#     upload_date = models.DateField()

#     def __unicode__(self):
#         return self.name

# class Upload(models.Model):
#     maintainer = models.ForeignKey(UserProfile)
#     name = models.SlugField(max_length=255)
#     debianversion = models.CharField(max_length=60)
#     upstreamversion = models.CharField(max_length=60)
#     origin = models.ForeignKey(Repository)
#     branch = models.CharField(max_length=60)
#     upload_date = models.DateField()

#     def __unicode__(self):
#         return self.name



