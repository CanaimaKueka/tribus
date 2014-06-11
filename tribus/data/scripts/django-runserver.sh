#!/usr/bin/env bash
cd /home/huntingbears/desarrollo/tribus
ln -fs /home/huntingbears/desarrollo/tribus/tribus/config/data/tribus.nginx.conf /etc/nginx/sites-enabled/
ln -fs /home/huntingbears/desarrollo/tribus/tribus/config/data/tribus.uwsgi.ini /etc/uwsgi/apps-enabled/
ln -fs /home/huntingbears/desarrollo/tribus/tribus/config/data/tribus.supervisor.conf /etc/supervisor/conf.d/
service mongodb restart
service postgresql restart
service redis-server restart
service slapd restart
service uwsgi restart
service supervisor restart
sleep 120
exit 0
