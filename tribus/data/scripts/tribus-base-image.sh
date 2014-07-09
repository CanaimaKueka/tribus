#!/usr/bin/env bash

debconf-set-selections ${PRESEED_DEBCONF}

apt-get update
apt-get install ${DEBIAN_RUN_DEPENDENCIES}
apt-get install ${DEBIAN_BUILD_DEPENDENCIES}

for i in ${CHANGE_PASSWD}; do
	echo ${i} | chpasswd
done

for j in ${START_SERVICES}; do
	service ${j} restart
done

easy_install pip
pip install ${PYTHON_DEPENDENCIES}

sudo -i -u postgres bash -c "psql -f ${PRESEED_DB}"
ldapadd ${LDAP_ARGS} -f "${PRESEED_LDAP}"

apt-get purge ${DEBIAN_BUILD_DEPENDENCIES}
apt-get autoremove
apt-get autoclean
apt-get clean

find / -name "*.pyc" -print0 | xargs -0r rm -rf
find /var/cache/apt -type f -print0 | xargs -0r rm -rf
find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf
find /usr/share/man -type f -print0 | xargs -0r rm -rf
find /usr/share/doc -type f -print0 | xargs -0r rm -rf
find /usr/share/locale -type f -print0 | xargs -0r rm -rf
find /var/log -type f -print0 | xargs -0r rm -rf
find /var/tmp -type f -print0 | xargs -0r rm -rf
find /tmp -type f -print0 | xargs -0r rm -rf

exit 0