#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/devices.sh
# DESCRIPCIÓN: Lista los dispositivos ópticos y/o usb disponibles para grabar
#              imágenes instalables.
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
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

LIST_DEV() {

        # ======================================================================
        # FUNCIÓN: LIST_DEV
        # DESCRIPCIÓN: Lista los dispositivos ópticos y/o usb disponibles.
        # ENTRADAS:
        #       [TYPE]: Tipo de Dispositivo
        # ======================================================================

        TYPE="${1}"
        [ -n "${TYPE}" ] && shift 1 || true

	DEVICELIST="$( ls -d1 /sys/block/* )"

	if [ "${TYPE}" = "list-optical" ]; then
		wodim -devices | grep '/dev/' | awk '{print $2}' | awk -F= '{print $2}'
	elif [ "${TYPE}" = "list-usb" ]; then
		for DEVICE in ${DEVICELIST}; do
			DEVICEID="$( basename ${DEVICE})"
			DEVICEBUS="$( udevadm info --query="all" --name="${DEVICEID}" | grep "ID_BUS" | awk -F= '{print $2}' )"
			DEVICETYPE="$( udevadm info --query="all" --name="${DEVICEID}" | grep "ID_TYPE" | awk -F= '{print $2}' )"
			DEVICENAME="$( udevadm info --query="all" --name="${DEVICEID}" | grep "DEVNAME" | awk -F= '{print $2}' )"
			if [ "${DEVICETYPE}" = "disk" ] && [ "${DEVICEBUS}" = "usb" ]; then
				echo "${DEVICENAME}"
			fi
		done
	fi

}
