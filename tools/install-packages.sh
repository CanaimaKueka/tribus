#!/bin/bash
#
# ====================================================================
# PACKAGE: aguilas
# FILE: tools/snapshot.sh
# DESCRIPTION:  Makes a new development snapshot of Aguilas.
# USAGE: ./tools/snapshot.sh
# COPYRIGHT:
# (C) 2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
# LICENCE: GPL3
# ====================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

ROOTDIR="$( pwd )"
PACKAGES="$( cat "${ROOTDIR}/tools/packages-debian.list" )"

echo "slapd slapd/purge_database boolean true" | debconf-set-selections

DEBIAN_FRONTEND="noninteractive" aptitude purge --assume-yes --allow-untrusted -o DPkg::Options::="--force-confmiss" -o DPkg::Options::="--force-confnew" -o DPkg::Options::="--force-overwrite" ${PACKAGES}

echo "slapd slapd/domain string tribus.org" | debconf-set-selections
echo "slapd shared/organization string tribus" | debconf-set-selections
echo "slapd slapd/password1 password tribus" | debconf-set-selections
echo "slapd slapd/password2 password tribus" | debconf-set-selections

DEBIAN_FRONTEND="noninteractive" aptitude install --assume-yes --allow-untrusted -o DPkg::Options::="--force-confmiss" -o DPkg::Options::="--force-confnew" -o DPkg::Options::="--force-overwrite" ${PACKAGES}

echo "postgres:tribus" | chpasswd

su postgres -c "psql -U postgres -c \"DROP DATABASE tribus;\""
su postgres -c "psql -U postgres -c \"DROP ROLE tribus;\""

su postgres -c "psql -U postgres -c \"CREATE ROLE tribus PASSWORD 'md51a2031d64cd6f9dd4944bac9e73f52dd' NOSUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;\""
su postgres -c "psql -U postgres -c \"CREATE DATABASE tribus OWNER tribus;\""
su postgres -c "psql -U postgres -c \"GRANT ALL PRIVILEGES ON DATABASE tribus to tribus;\""

sh ${ROOTDIR}/tools/maint/ldap-populate-users.sh  cn=admin,dc=tribus,dc=org tribus localhost dc=tribus,dc=org

exit 0