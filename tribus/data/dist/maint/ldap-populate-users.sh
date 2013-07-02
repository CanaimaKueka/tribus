#!/bin/sh
#
# ====================================================================
# PACKAGE: tribus
# FILE: tools/maint/ldap-populate-users.sh
# DESCRIPTION: Deletes all users and populates with example database.
# USAGE: ./ldap-populate-users.sh [ADMINDN] [PASS] [SERVER] [BASE]
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

TMP="$( tempfile )"
ROOTDIR="$( pwd )"
LDIF="${ROOTDIR}/tools/maint/users.ldif"
LDAPWRITER="${1}"
LDAPPASS="${2}"
LDAPSERVER="${3}"
LDAPBASE="${4}"

ENTRIES=$( ldapsearch -x -w "${LDAPPASS}" -D "${LDAPWRITER}" -h "${LDAPSERVER}" -b "${LDAPBASE}" -LLL "(uid=*)" | perl -p00e 's/\r?\n //g' | grep "dn: "| sed 's/dn: //g' | sed 's/ /_@_/g' )

for ENTRY in ${ENTRIES}; do
	echo "Deleting ${ENTRY}" | tee ${TMP}
	ldapdelete -x -w "${LDAPPASS}" -D "${LDAPWRITER}" -h "${LDAPSERVER}" "${ENTRY}"
done

ldapadd -x -w "${LDAPPASS}" -D "${LDAPWRITER}" -h "${LDAPSERVER}" -f "${LDIF}"

exit 0
