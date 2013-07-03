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

. ${ROOTDIR}/virtualenv/bin/activate
pip install -r ${ROOTDIR}/tools/packages-python.list
deactivate

exit 0