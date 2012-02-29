#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import datetime

class Repository(models.Model):
    name = models.CharField(max_length=60)
    address = models.URLField(max_length=60)

    def __unicode__(self):
        return self.name

class Distribution(models.Model):
    name = models.CharField(max_length=60)
    address = models.URLField(max_length=60)
    repos = models.ForeignKey(Repository)

    def __unicode__(self):
        return self.name

# A person is a user of chamanes, that is a package maintainer
class User(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    role = models.CharField(max_length=60)
    appadmin = models.BooleanField()
    loggedin = models.BooleanField()
    mail = models.EmailField(max_length=60)
    uid = models.CharField(max_length=60)

    def __unicode__(self):
#       return u'%s %s' % (self.firstname, self.lastname)
        return self.uid

class Package(models.Model):
    maintainer = models.ForeignKey(User)
    name = models.SlugField(max_length=255)
    debianversion = models.CharField(max_length=60)
    upstreamversion = models.CharField(max_length=60)
    origin = models.ForeignKey(Repository)
    branch = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

