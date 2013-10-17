#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import re
from django.db import models
from django.contrib.auth.models import User


def __unicode__(self):
    return self.username

def md5(self):
	m = hashlib.md5()
	self.md5 = m.update(self.email)
	print self.md5



User.add_to_class('description', models.CharField(max_length = 160, null = True, blank = True))
User.add_to_class('location',    models.CharField(max_length = 50, null = True, blank = True))
User.add_to_class('telefono',    models.IntegerField(null = True, blank = True))
User.add_to_class('md5',			 models.CharField(max_length = 50, null = True, blank = True))


User.add_to_class('follows',   models.ManyToManyField('self', symmetrical = False ,related_name='profile_follows'))
User.add_to_class('followers',   models.ManyToManyField('self',symmetrical = False, related_name='profile_followers'))
User.add_to_class('__unicode__',__unicode__)
User.add_to_class('md5',md5)