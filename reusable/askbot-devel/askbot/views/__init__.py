"""
:synopsis: django view functions for the askbot project
"""
from askbot.views import readers
from askbot.views import writers
from askbot.views import commands
from askbot.views import users
from askbot.views import meta
from askbot.views import sharing
from askbot.views import widgets
from django.conf import settings
if 'avatar' in settings.INSTALLED_APPS:
    from askbot.views import avatar_views
