#!/usr/bin/env bash

for j in ${START_SERVICES}; do
	service ${j} restart
done

if ! id -u ${HOST_USER} >/dev/null 2>&1; then
	useradd -o -u ${HOST_USER_ID} ${HOST_USER}
	echo "${HOST_USER}:tribus" | chpasswd
fi

rm -rf /tmp/tribus/
mkdir -p /tmp/tribus/python/pip-packages
mkdir -p /tmp/tribus/python/deb-packages
mkdir -p /tmp/tribus/logs

cp -r /usr/local/lib/python2.7/dist-packages/* /tmp/tribus/python/pip-packages/
cp -r /usr/share/pyshared/* /tmp/tribus/python/deb-packages/

chown -R ${HOST_USER}:${HOST_USER} /tmp/tribus/

tail -f /dev/null