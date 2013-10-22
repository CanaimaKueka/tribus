#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import re
from django.db import models
from django.contrib.auth.models import User


def __unicode__(self):
    return self.username


User.add_to_class('follows',    models.ForeignKey(User, related_name="follow", null=True))
User.add_to_class('followers',    models.ForeignKey(User, related_name="follower", null=True))

User.add_to_class('description', models.CharField(max_length = 160, null = True, blank = True))
User.add_to_class('location',    models.CharField(max_length = 50, null = True, blank = True))
User.add_to_class('telefono',    models.IntegerField(null = True, blank = True))
User.add_to_class('__unicode__',__unicode__)

class Social(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	seguido   = models.ForeignKey(User, related_name="seguidos", null=True)
	seguidor = models.ForeignKey(User, related_name="seguidores", null=True)