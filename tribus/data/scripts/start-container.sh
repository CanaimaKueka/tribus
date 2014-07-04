#!/usr/bin/env bash
for j in ${START_SERVICES}; do service ${j} restart; done
tail -f /dev/null

