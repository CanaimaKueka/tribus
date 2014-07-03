#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
export DJANGO_SETTINGS_MODULE=tribus.config.web
export PYTHONPATH=/home/fran/Proyectos/tribus:
debconf-set-selections /home/fran/Proyectos/tribus/tribus/config/data/preseed-debconf.conf
apt-get update
apt-get install postgresql slapd ldap-utils redis-server reprepro sudo udev openssh-server python-xapian libxml2 libxslt1.1 make git curl lsb-release ca-certificates
apt-get install python-dev libxml2-dev libxslt1-dev libsasl2-dev libldap2-dev libpq-dev gcc
python /home/fran/Proyectos/tribus/tribus/data/scripts/get-pip.py
pip install Fabric==1.9.0 PyYAML==3.11 cssmin==0.2.0 slimit==0.8.1 Sphinx==1.2.2 Babel==1.3 Django==1.6.5 South==0.8.4 celery==3.0.23 django-celery==3.0.23 django-redis==3.6.2 hiredis==0.1.3 psycopg2==2.5.3 python-debian==0.1.21 chardet==2.2.1 django-ldapdb==0.3.2 django-auth-ldap==1.2.0 django-haystack==2.1.0 celery-haystack==0.7.2 django-waffle==0.10 django-registration==1.0 django-tastypie==0.10.0 python-mimeparse==0.1.4 transifex-client==0.11.beta lxml==3.3.5 flake8==2.1.0 pep257==0.3.2 coveralls==0.4.2 sh==1.09 -e git+https://github.com/joseguerrero/xapian-haystack.git#egg=xapian-haystack -e git+https://github.com/joseguerrero/django-static.git#egg=django-static
echo "root:tribus" | chpasswd
echo "postgres:tribus" | chpasswd
echo "openldap:tribus" | chpasswd
echo "redis:tribus" | chpasswd
service ssh start
service postgresql start
service redis-server start
service slapd start
sudo -i -u postgres bash -c "psql -f '/home/fran/Proyectos/tribus/tribus/config/data/preseed-db.sql'"
ldapadd -x -w "tribus" -D "cn=admin,dc=tribus,dc=org" -H "ldap://localhost" -f "/home/fran/Proyectos/tribus/tribus/config/data/preseed-ldap.ldif"
apt-get purge python-dev libxml2-dev libxslt1-dev libsasl2-dev libldap2-dev libpq-dev gcc
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
