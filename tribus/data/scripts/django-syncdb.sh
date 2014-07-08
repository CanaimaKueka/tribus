#!/usr/bin/env bash

python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py config_development_su

for i in ${WAFFLE_SWITCHES}; do
    python manage.py switch ${i} on --create
done

exit 0
