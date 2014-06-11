#!/usr/bin/env bash
ln -fs /proc/self/fd /dev/fd
ln -fs /media/desarrollo/tribus/tribus/config/data/tribus.nginx.conf /etc/nginx/sites-enabled/
ln -fs /media/desarrollo/tribus/tribus/config/data/tribus.uwsgi.ini /etc/uwsgi/apps-enabled/
ln -fs /media/desarrollo/tribus/tribus/config/data/tribus.supervisor.conf /etc/supervisor/conf.d/
service mongodb start
service postgresql start
service redis-server start
service slapd start
service uwsgi start
service nginx start
service supervisor start
sleep 1200
exit 0
