#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.web.settings")

from django.contrib.auth.models import User

u=User.objects.get(username__exact='admin')
u.set_password('tribus')
u.save()