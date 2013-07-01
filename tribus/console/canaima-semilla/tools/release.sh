#!/bin/sh -e
#
# ====================================================================
# PACKAGE: canaima-semilla
# FILE: tools/release.sh
# DESCRIPTION:  Makes a new stable release of Canaima Semilla.
# USAGE: ./tools/release.sh
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
ROOTNAME="$( basename ${ROOTDIR} )"
PROJDIR="$( dirname ${ROOTDIR} )"
GITHUBWIKI="${ROOTDIR}/documentation/githubwiki"
GOOGLEWIKI="${ROOTDIR}/documentation/googlewiki"
VERSION="${ROOTDIR}/VERSION"
CHANGELOG="${ROOTDIR}/ChangeLog"
CHANGES="$( tempfile )"
DEVERSION="$( tempfile )"
NEWCHANGES="$( tempfile )"
DATE=$( date +%D )
VERDE="\033[1;32m"
ROJO="\033[1;31m"
AMARILLO="\033[1;33m"
FIN="\033[0m"

ERROR() {
	printf "${ROJO}${1}${FIN}\n"
}

WARNING() {
	printf "${AMARILLO}${1}${FIN}\n"
}

SUCCESS() {
	printf "${VERDE}${1}${FIN}\n"
}

git config --global user.name "Luis Alejandro Martínez Faneyth"
git config --global user.email "luis@huntingbears.com.ve"
export DEBFULLNAME="Luis Alejandro Martínez Faneyth"
export DEBEMAIL="luis@huntingbears.com.ve"

if [ "$( git branch 2> /dev/null | sed -e '/^[^*]/d;s/\* //' )" != "development" ]; then
	ERROR "[MAIN] You are not on \"development\" branch."
	git checkout development
fi
if [ -n "$( git diff --exit-code 2> /dev/null )" ]; then
	ERROR "[MAIN] You have uncommitted code on \"development\" branch."
	exit 1
fi
cd ${GITHUBWIKI}
if [ "$( git branch 2> /dev/null | sed -e '/^[^*]/d;s/\* //' )" != "development" ]; then
	ERROR "[GITHUBWIKI] You are not on \"development\" branch."
	git checkout development
fi
if [ -n "$( git diff --exit-code 2> /dev/null )" ]; then
	ERROR "[GITHUBWIKI] You have uncommitted code on \"development\" branch."
	exit 1
fi
cd ${ROOTDIR}
cd ${GOOGLEWIKI}
if [ "$( git branch 2> /dev/null | sed -e '/^[^*]/d;s/\* //' )" != "development" ]; then
	ERROR "[GOOGLEWIKI] You are not on \"development\" branch."
	git checkout development
fi
if [ -n "$( git diff --exit-code 2> /dev/null )" ]; then
	ERROR "[GOOGLEWIKI] You have uncommitted code on \"development\" branch."
	exit 1
fi
cd ${ROOTDIR}

git log > ${CHANGES}
cp ${VERSION} ${DEVERSION}
git checkout release
git clean -fd
git reset --hard

OLDCOMMIT="$( cat ${VERSION} | grep "COMMIT" | sed 's/COMMIT=//g;s/"//g' )"
OLDCOMMITLINE="$( cat ${CHANGES}  | grep -n "${OLDCOMMIT}" | awk -F: '{print $1}' )"
NEWVERSION="$( cat ${DEVERSION} | grep "VERSION" | sed 's/VERSION=//g;s/"//g;s/+.*//g' )"

echo "STABLE RELEASE v${NEWVERSION} (${DATE})" > ${NEWCHANGES}
cat ${CHANGES} | sed -n 1,${OLDCOMMITLINE}p | sed 's/commit.*//g;s/Author:.*//g;s/Date:.*//g;s/Merge.*//g;/^$/d;' >> ${NEWCHANGES}
sed -i 's/New stable release.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
sed -i 's/New development snapshot.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
sed -i 's/Signed-off-by:.*//g;s/    //g;/^$/d;' ${NEWCHANGES}
echo "" >> ${NEWCHANGES}
cat ${CHANGELOG} >> ${NEWCHANGES}

WARNING "Merging development into release ..."
git merge -q -s recursive -X theirs --squash development

mv ${NEWCHANGES} ${CHANGELOG}
rm ${CHANGES} ${DEVERSION}

LASTCOMMIT="$( git rev-parse HEAD )"

echo "VERSION=\"${NEWVERSION}\"" > ${VERSION}
echo "COMMIT=\"${LASTCOMMIT}\"" >> ${VERSION}
echo "RELDATE=\"${DATE}\"" >> ${VERSION}

WARNING "Updating submodules ..."
make prepare

WARNING "Updating Google Code wiki ..."
cd ${GOOGLEWIKI}
git checkout master
git merge -q -s recursive -X theirs --squash development
git add .
git commit -q -a -m "Updating documentation"
git push -q --tags https://code.google.com/p/canaima-semilla.wiki/ master
git checkout development
cd ${ROOTDIR}

WARNING "Updating GitHub wiki ..."
cd ${GITHUBWIKI}
git checkout master
git merge -q -s recursive -X theirs --squash development
git add .
git commit -q -a -m "Updating documentation"
git push -q --tags git@github.com:HuntingBears/canaima-semilla.wiki.git master
git checkout development
cd ${ROOTDIR}

WARNING "Committing changes ..."
git add .
git commit -q -a -m "New stable release ${NEWVERSION}"
git tag ${NEWVERSION} -m "New stable release ${NEWVERSION}"

WARNING "Creating tarball ..."
tar -czf ../canaima-semilla_${NEWVERSION}.orig.tar.gz *

WARNING "Pushing new version to remote repositories ..."
git push -q --tags git@github.com:HuntingBears/canaima-semilla.git release
git push -q --tags git@gitorious.org:huntingbears/canaima-semilla.git release
git push -q --tags https://code.google.com/p/canaima-semilla/ release

git checkout development

SUCCESS "Stable Release Published"
