#!/usr/bin/env bash
service ssh start
service mongodb start
service postgresql start
service redis-server start
service slapd start
tail -f /dev/null

