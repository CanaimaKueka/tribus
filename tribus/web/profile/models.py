#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import OneToOneField, ManyToManyField, Model
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(Model):
    user = OneToOneField(User, related_name='user_profile')
    follows = ManyToManyField(User, related_name='follows_profile', blank=True)
    followers = ManyToManyField(User, related_name='followers_profile', blank=True)

    def __unicode__(self):
        return self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)