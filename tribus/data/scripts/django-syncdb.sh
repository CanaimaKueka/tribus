#!/usr/bin/env bash

python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py config_development_su --noinput

for i in ${WAFFLE_SWITCHES}; do
    python manage.py switch ${i} on --create --noinput
done

exit 0
