#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

def chamanesconf(request):
    dictionary = {
        'app_skin': settings.APP_SKIN,
        'app_name': settings.APP_NAME,
        'app_desc': settings.APP_DESC,
        'app_locale': settings.LANGUAGE_CODE,
        'app_charset': settings.DEFAULT_CHARSET,
        'app_static_url': settings.STATIC_URL,
    }

    return dictionary

