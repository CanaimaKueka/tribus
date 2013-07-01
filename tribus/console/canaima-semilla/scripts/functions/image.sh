#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/image.sh
# DESCRIPCIÓN: Funciones para la construcción y procesamiento de imágenes.
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

CS_BUILD_IMAGE() {

	# ======================================================================
	# FUNCIÓN: CS_BUILD_IMAGE
	# DESCRIPCIÓN: Crea una imagen instalable a partir de la configuración
	#	      generada por CS_POPULATE_TREE.
	# ENTRADAS:
	#	[ISOS]: Directorio donde se encuentra el árbol de configuración.
	#	[BUILD_OP_MODE]: Modo de operación. 
	#	[BUILD_PRINT_MODE]: Modo de verbosidad.
	# SALIDAS:
	#	[0]: La imagen se construyó satisfactoriamente.
	#	[1]: La construcción de la imagen falló
	# ======================================================================

	ISOS="${1}"
	[ -n "${ISOS}" ] && shift 1 || true
	BUILD_OP_MODE="${1}"
	[ -n "${BUILD_OP_MODE}" ] && shift 1 || true
	BUILD_PRINT_MODE="${1}"
	[ -n "${BUILD_PRINT_MODE}" ] && shift 1 || true

	TCSCONFFILE="${ISOS}/config/c-s/tree.conf"

	if [ -f "${TCSCONFFILE}" ]; then
		. "${TCSCONFFILE}"
	else
		WARNINGMSG "El contenedor de construcción parece haber sido configurado manualmente."
		WARNINGMSG "Puede que algunas características de %s no estén disponibles." "${CS_NAME}"

		if [ -f "${ISOS}/config/common" ] && [ -f "${ISOS}/config/binary" ] && \
		[ -f "${ISOS}/config/chroot" ] && [ -f "${ISOS}/config/bootstrap" ]; then

			. "${ISOS}/config/bootstrap"
			. "${ISOS}/config/chroot"
			. "${ISOS}/config/binary"
			. "${ISOS}/config/common"

			ARCH="${LB_ARCHITECTURES}"
			MEDIO="${LB_BINARY_IMAGES}"
			META_DISTRO="${LB_MODE}"

			case ${MEDIO} in
				usb-hdd|hdd)
					MEDIO_LBNAME="binary.img"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.img"
				;;

				iso)
					MEDIO_LBNAME="binary.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;

				iso-hybrid)
					MEDIO_LBNAME="binary-hybrid.iso"
					MEDIO_CSNAME="${META_DISTRO}-flavour_${ARCH}.iso"
				;;
			esac
		else
			ERRORMSG "%s no pudo encontrar una configuración apropiada en %s." "${CS_NAME}" "${ISOS}/config"
			exit 1
		fi
	fi

	WARNINGMSG "[--- INICIANDO CONSTRUCCIÓN ---]"
	cd "${ISOS}" && ${LB} build ${LB_QUIET} ${LB_VERBOSE} 2>&1 | ${TEE} -a "${ISOS}/${LOGFILE}"

	if [ -e "${ISOS}/${MEDIO_LBNAME}" ] && [ -n "${MEDIO_CSNAME}" ] && [ -n "${MEDIO_LBNAME}" ]; then

		PESO="$( ${ECHO} "scale=2;$( ${STAT} --format=%s "${ISOS}/${MEDIO_LBNAME}" )/1048576" | ${BC} )MB"
		${MV} "${ISOS}/${MEDIO_LBNAME}" "${ISOS}/${MEDIO_CSNAME}"

		SUCCESSMSG "Se ha creado una imagen %s con un peso de %s." "${MEDIO}" "${PESO}"
		SUCCESSMSG "Puedes encontrar la imagen '%s' en el directorio %s" "${MEDIO_CSNAME}" "${ISOS}"
		exit 0
	else
		ERRORMSG "Ocurrió un error durante la generación de la imagen."
		ERRORMSG "Si deseas asistencia, puedes enviar un correo a %s con el contenido del archivo '%s'" "${CS_LOG_MAIL}" "${ISOS}/${LOGFILE}"
		exit 1
	fi
}
