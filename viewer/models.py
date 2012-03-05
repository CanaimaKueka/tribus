#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Repository(models.Model):
    name = models.CharField(max_length=60)
    branches = models.CharField(max_length=60)
    sections = models.CharField(max_length=60)
    address = models.URLField(max_length=60)
    source = models.BooleanField()

    def __unicode__(self):
        return self.name

class Distribution(models.Model):
    name = models.CharField(max_length=60)
    address = models.URLField(max_length=60)
    repos = models.ForeignKey(Repository)
    bugtracker = models.URLField(max_length=60)
    wiki = models.URLField(max_length=60)
    devlist = models.EmailField(max_length=60)
    disclist = models.EmailField(max_length=60)
    suplist = models.EmailField(max_length=60)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    role = models.CharField(max_length=60)
    gnupg = models.CharField(max_length=60)
    appadmin = models.BooleanField()
    date_promoted = models.DateField()

    def __unicode__(self):
        return self.username

class Package(models.Model):
    maintainer = models.ForeignKey(UserProfile)
    name = models.SlugField(max_length=255)
    debianversion = models.CharField(max_length=60)
    upstreamversion = models.CharField(max_length=60)
    origin = models.ForeignKey(Repository)
    branch = models.CharField(max_length=60)
    depends = models.CharField(max_length=60)
    recommends = models.CharField(max_length=60)
    suggests = models.CharField(max_length=60)
    conflicts = models.CharField(max_length=60)
    date_uploaded = models.DateField()

    def __unicode__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    package = models.ForeignKey(Package)
    assigned_to = models.ForeignKey(UserProfile)
    distro = models.ForeignKey(Distribution)
    date_reported = models.DateField()
    status = models.CharField(max_length=255)

    def __unicode__(self):
        return self.number

class Comment(models.Model):
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    package = models.ForeignKey(Package)
    assigned_to = models.ForeignKey(UserProfile)
    distro = models.ForeignKey(Distribution)
    date_reported = models.DateField()
    status = models.CharField(max_length=255)

    def __unicode__(self):
        return self.number

class Upload(models.Model):
    maintainer = models.ForeignKey(UserProfile)
    name = models.SlugField(max_length=255)
    debianversion = models.CharField(max_length=60)
    upstreamversion = models.CharField(max_length=60)
    origin = models.ForeignKey(Repository)
    branch = models.CharField(max_length=60)
    upload_date = models.DateField()

    def __unicode__(self):
        return self.name

class Team(models.Model):
    maintainer = models.ForeignKey(UserProfile)
    name = models.SlugField(max_length=255)
    debianversion = models.CharField(max_length=60)
    upstreamversion = models.CharField(max_length=60)
    origin = models.ForeignKey(Repository)
    branch = models.CharField(max_length=60)
    upload_date = models.DateField()

    def __unicode__(self):
        return self.name

class Upload(models.Model):
    maintainer = models.ForeignKey(UserProfile)
    name = models.SlugField(max_length=255)
    debianversion = models.CharField(max_length=60)
    upstreamversion = models.CharField(max_length=60)
    origin = models.ForeignKey(Repository)
    branch = models.CharField(max_length=60)
    upload_date = models.DateField()

    def __unicode__(self):
        return self.name



