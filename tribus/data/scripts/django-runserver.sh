#!/usr/bin/env bash
cd /home/armikhael/Tribus/tribus
export DEBIAN_FRONTEND=noninteractive
export DJANGO_SETTINGS_MODULE=tribus.config.web
export PYTHONPATH=/home/armikhael/Tribus/tribus:
python manage.py celeryd -c 1 --beat -l INFO &
python manage.py celery beat -s celerybeat-schedule &
python manage.py runserver 0.0.0.0:8000

