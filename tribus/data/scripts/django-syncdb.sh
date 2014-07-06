#!/usr/bin/env bash

python manage.py syncdb --noinput
python manage.py migrate --noinput

for i in ${WAFFLE_SWITCHES}; do
    python manage.py switch ${i} on --create
done

exit 0