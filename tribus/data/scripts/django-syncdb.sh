#!/usr/bin/env bash
cd /home/fran/Proyectos/tribus
export DEBIAN_FRONTEND=noninteractive
export DJANGO_SETTINGS_MODULE=tribus.config.web
export PYTHONPATH=/home/fran/Proyectos/tribus:
python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py switch profile on --create
python manage.py switch admin_first_time off --create
python manage.py switch cloud on --create

