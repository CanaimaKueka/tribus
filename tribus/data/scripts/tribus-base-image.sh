set -x
set -e
export DEBIAN_FRONTEND=noninteractive
debconf-set-selections /media/desarrollo/tribus/tribus/config/data/preseed-debconf.conf
apt-get update
apt-get install postgresql slapd ldap-utils redis-server mongodb-server python-xapian reprepro sudo uwsgi nginx
apt-get install libxml2-dev libxslt1-dev python-dev libldap2-dev libsasl2-dev libpq-dev gcc make python-setuptools lsb-release git curl ca-certificates
easy_install pip
pip install django-tastypie==0.10.0 cssmin==0.1.4 slimit==0.8.1 docutils==0.11 sphinx==1.2b3 babel==1.3 django==1.5.2 South==0.8.2 celery==3.0.23 celery-with-redis==3.0 django-celery==3.0.23 django-redis==3.3 hiredis==0.1.1 oauth2==1.5.211 psycopg2==2.5.1 python-debian==0.1.21 python-ldap==2.4.13 python-openid==2.2.5 redis==2.8.0 chardet==2.1.1 webdriverwrapper==1.0.1 django-ldapdb==0.1.0 django-auth-ldap==1.1.4 django-social-auth==0.7.28 mimeparse==0.1.3 django-haystack==2.1.0 celery-haystack==0.7.2 mongoengine==0.8.4 mongodbforms==0.3 transifex-client==0.9.1 django-registration django-waffle==0.10 lxml flake8 coverage coveralls nodeenv sh pep257 fabric==1.8.2 pyyaml -e git+https://github.com/LuisAlejandro/django-tastypie-mongoengine.git#egg=django-tastypie-mongoengine -e git+https://github.com/joseguerrero/xapian-haystack.git#egg=xapian-haystack -e git+https://github.com/joseguerrero/django-static.git#egg=django-static
echo root:tribus | chpasswd
echo postgres:tribus | chpasswd
service mongodb restart
service postgresql restart
service redis-server restart
service slapd restart
sudo -iu postgres bash -c 'psql -f /media/desarrollo/tribus/tribus/config/data/preseed-db.sql'
ldapadd -x -w "tribus" -D "cn=admin,dc=tribus,dc=org" -H "ldap://localhost" -f /media/desarrollo/tribus/tribus/config/data/preseed-ldap.ldif
apt-get purge libxml2-dev libxslt1-dev python-dev libldap2-dev libsasl2-dev libpq-dev gcc make python-setuptools lsb-release git curl ca-certificates
apt-get autoremove
apt-get autoclean
apt-get clean
find /usr -name *.pyc -print0 | xargs -0r rm -rf
find /var/cache/apt -type f -print0 | xargs -0r rm -rf
find /var/lib/mongodb/journal -type f -print0 | xargs -0r rm -rf
find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf
find /usr/share/man -type f -print0 | xargs -0r rm -rf
find /usr/share/doc -type f -print0 | xargs -0r rm -rf
find /usr/share/locale -type f -print0 | xargs -0r rm -rf
find /var/log -type f -print0 | xargs -0r rm -rf
find /var/tmp -type f -print0 | xargs -0r rm -rf
find /tmp -type f -print0 | xargs -0r rm -rf
find /src -type f -print0 | xargs -0r rm -rf
exit 0
