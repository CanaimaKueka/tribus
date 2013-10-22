#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import OneToOneField, ManyToManyField, Model, CharField, IntegerField, ForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def __unicode__(self):
    return self.username

User.add_to_class('description', CharField(max_length = 160, null = True, blank = True))
User.add_to_class('location',    CharField(max_length = 50, null = True, blank = True))
User.add_to_class('telefono',    IntegerField(null = True, blank = True))
User.add_to_class('__unicode__',__unicode__)

class UserProfile(Model):
    user = OneToOneField(User, related_name='user_profile')
    follows = ForeignKey(User, related_name='follows_profile',null = True, blank=True)
    followers = ForeignKey(User, related_name='followers_profile',null = True, blank=True)

    def __unicode__(self):
        return self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


# User.add_to_class('follows',    models.ForeignKey(User, related_name="follow", null=True))
# User.add_to_class('followers',    models.ForeignKey(User, related_name="follower", null=True))

# class Social(models.Model):
# 	user = models.OneToOneField(User, primary_key=True)
# 	seguido   = models.ForeignKey(User, related_name="seguidos", null=True)
# 	seguidor = models.ForeignKey(User, related_name="seguidores", null=True)


