#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/save.sh
# DESCRIPCIÓN: Módulo para grabar imágenes en médios de almacenamiento digitales
#	      u ópticos.
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

ACTION="${1}"
[ -n "${ACTION}" ] && shift 1 || true
BINDIR="${1}"
[ -n "${BINDIR}" ] && shift 1 || true

# Asignando directorios de trabajo
if [ "${BINDIR}" = "/usr/bin" ]; then
	BASEDIR="/usr/share/canaima-semilla"
	CONFDIR="/etc/canaima-semilla"
else
	BASEDIR="${BINDIR}"
	CONFDIR="${BASEDIR}"
fi

# Cargando valores predeterminados
. "${BASEDIR}/scripts/functions/defaults.sh"

# Corriendo rutinas de inicio
. "${BASEDIR}/scripts/init.sh"

if [ "${ACTION}" = "grabar" ]; then
	LONGOPTS="imagen:,dispositivo:,expresivo,silencioso,listar-opticos,listar-usb,ayuda,uso,acerca"
	COMMAND="grabar"
	PARAMETERS="[-i|--imagen ARCHIVO]\n\
\t[-d|--dispositivo DISPOSITIVO]\n\
\t[-v|--expresivo]\n\
\t[-q|--silencioso]\n\
\t[-l|--listar-opticos]\n\
\t[-L|--listar-usb]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "save" ]; then
	LONGOPTS="image:,device:,verbose,quiet,list-optical,list-usb,help,usage,about"
	COMMAND="save"
	PARAMETERS="[-i|--image FILE]\n\
\t[-d|--device DEVICE]\n\
\t[-v|--verbose]\n\
\t[-q|--quiet]\n\
\t[-l|--list-optical]\n\
\t[-L|--list-usb]\n\
\t[-h|--help]\n\
\t[-u|--usage]\n\
\t[-A|--about]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="i:d:vqlLhuA"
DESCRIPTION="$( NORMALMSG "Comando para simulación de imágenes instalables." )"

OPTIONS="$( ${GETOPT} --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ ${?} != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-i|--imagen|--image)
			IMAGE="${2}"
			shift 2 || true
		;;

		-d|--dispositivo|--device)
			DEVICE="${2}"
			shift 2 || true
		;;

		-v|--expresivo|--verbose)
			SAVE_PRINT_MODE="verbose"
			shift 1 || true
		;;

		-q|--silencioso|--quiet)
			SAVE_PRINT_MODE="quiet"
			shift 1 || true
		;;

		-l|--listar-opticos|--list-optical)
			SAVE_OP_MODE="list-optical"
			shift 1 || true
		;;

		-L|--listar-usb|--list-usb)
			SAVE_OP_MODE="list-usb"
			shift 1 || true
		;;

		-h|--ayuda|--help)
			if ${MAN} -w "${CS_CMD}_${COMMAND}" 1>/dev/null 2>&1; then
				${MAN} "${CS_CMD}_${COMMAND}"
				exit 0
			else
				USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
			fi
		;;

		-u|--uso|--usage)
			USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
		;;

		-A|--acerca|--about)
			ABOUT
		;;

		--)
			shift
			break
		;;

		*)
			ERRORMSG "Ocurrió un problema interpretando los parámetros."
			exit 1
		;;
	esac
done

case ${SAVE_OP_MODE} in
	list-usb|list-optical)
		LIST_DEV "${SAVE_OP_MODE}"
	;;

	normal)
		USB_LIST="$( LIST_DEV "list-usb" )"
		OPT_LIST="$( LIST_DEV "list-optical" )"

		for ITEM in ${USB_LIST}; do
			if [ "${ITEM}" = "${DEVICE}" ]; then
				if ${DD} if="${IMAGE}" of="${DEVICE}" 1>/dev/null 2>&1; then
					SAVED=1
					SUCCESSMSG "¡Felicidades! Su imagen ha sido grabada satisfactoriamente en el dispositivo indicado."
					exit 0
				else
					ERRORMSG "Ha ocurrido un error mientras se grababa la imagen. Retire la unidad e inténtelo de nuevo."
					exit 1
				fi
			fi
		done

		for ITEM in ${OPT_LIST}; do
			if [ "${ITEM}" = "${DEVICE}" ]; then
				if ${WODIM} -eject -data dev="${DEVICE}" ${IMAGE} 1>/dev/null 2>&1; then
					SAVED=1
					SUCCESSMSG "¡Felicidades! Su imagen ha sido grabada satisfactoriamente en el dispositivo indicado."
					exit 0
				else
					ERRORMSG "Ha ocurrido un error mientras se grababa la imagen. Retire la unidad e inténtelo de nuevo."
					exit 1
				fi
			fi
		done

		if [ ${SAVED} != 1 ]; then
			ERRORMSG "El dispositivo indicado no es apto para grabar imágenes."
			exit 1
		fi
	;;
esac
