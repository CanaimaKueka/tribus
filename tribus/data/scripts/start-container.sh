#!/usr/bin/env bash
service mongodb start
service postgresql start
service redis-server start
service slapd start
service ssh start
tail -f /dev/null

