#!/usr/bin/env bash
service ssh start
service postgresql start
service slapd start
tail -f /dev/null

