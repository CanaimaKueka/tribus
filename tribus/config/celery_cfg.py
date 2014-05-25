# THIS FILE WOULD BE USED TO INITIALIZE CELERY 3.1.X
# 'django-celery' is not required, install it ONLY if you need to manage the schedule
# from the admin, or if you want to store task results in the DB through django's ORM:
# http://stackoverflow.com/questions/20116573/in-celery-3-1-making-django-periodic-task

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tribus.config.web')
app = Celery()
cfg = app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)