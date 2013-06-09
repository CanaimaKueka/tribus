#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

def tribusconf(request):
    dictionary = {
        'TBS_LOCALE': settings.LANGUAGE_CODE,
        'TBS_CHARSET': settings.DEFAULT_CHARSET,
        'TBS_STATIC': settings.STATIC_URL,
    }

    return dictionary

