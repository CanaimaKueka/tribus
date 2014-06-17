#!/usr/bin/env bash
service mongodb restart
service postgresql restart
service redis-server restart
service slapd restart
service ssh restart
tail -f /dev/null

