#!/usr/bin/env bash
cd /home/huntingbears/desarrollo/tribus
export DEBIAN_FRONTEND=noninteractive
export DJANGO_SETTINGS_MODULE=tribus.config.web
export PYTHONPATH=/home/huntingbears/desarrollo/tribus
python manage.py syncdb --noinput
python manage.py migrate --noinput
exit 0
