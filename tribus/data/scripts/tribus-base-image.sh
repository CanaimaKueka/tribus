#!/usr/bin/env bash

debconf-set-selections ${PRESEED_DEBCONF}

echo "deb http://http.us.debian.org/debian wheezy-backports main" >> /etc/apt/sources.list

apt-get update
apt-get install ${DEBIAN_RUN_DEPENDENCIES}
apt-get install ${DEBIAN_BUILD_DEPENDENCIES}

curl https://bootstrap.pypa.io/get-pip.py | python
curl https://www.npmjs.org/install.sh | bash

for i in ${CHANGE_PASSWD}; do
    echo ${i} | chpasswd
done

for j in ${START_SERVICES}; do
    service ${j} restart
done

pip install ${PYTHON_DEPENDENCIES}
npm install ${NODE_DEPENDENCIES}

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
