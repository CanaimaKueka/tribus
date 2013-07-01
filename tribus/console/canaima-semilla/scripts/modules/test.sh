#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/test.sh
# DESCRIPCIÓN: Módulo para la simulación del arranque de una imagen construida
#	      con Canaima Semilla.
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

if [ "${ACTION}" = "probar" ]; then
	LONGOPTS="imagen:,memoria:,procesadores:,iniciar-cd,iniciar-dd,nuevo-disco,dimensiones-disco:,ayuda,uso,acerca"
        COMMAND="probar"
        PARAMETERS="[-i|--imagen ARCHIVO]\n\
\t[-m|--memoria 256|512|...]\n\
\t[-p|--procesadores 1|2|4|...]\n\
\t[-c|--iniciar-cd]\n\
\t[-d|--iniciar-dd]\n\
\t[-n|--nuevo-disco]\n\
\t[-s|--dimensiones-disco 10|50|...]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "test" ]; then
	LONGOPTS="image:,memory:,processors:,start-cd,start-hd,new-disk,new-disk-size:,help,usage,about"
        COMMAND="test"
        PARAMETERS="[-i|--image FILE]\n\
\t[-m|--memory 256|512|...]\n\
\t[-p|--processors 1|2|4|...]\n\
\t[-c|--start-cd]\n\
\t[-d|--start-hd]\n\
\t[-n|--new-disk]\n\
\t[-s|--new-disk-size 10|50|...]\n\
\t[-h|--help]\n\
\t[-u|--usage]\n\
\t[-A|--about]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="i:m:p:cdns:huA"
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
			KVM_CD_FILE="${2}"
			shift 2 || true
		;;

		-m|--memoria|--memory)
			KVM_MEM="${2}"
			shift 2 || true
		;;

		-p|--procesadores|--processors)
			KVM_PROC="${2}"
			shift 2 || true
		;;

		-c|--iniciar-cd|--start-cd)
			KVM_DISK_MODE="d"
			shift 1 || true
		;;

		-d|--iniciar-dd|--start-hd)
			KVM_DISK_MODE="c"
			shift 1 || true
		;;

		-n|--nuevo-disco|--new-disk)
			KVM_NEW_DISK="true"
			shift 1 || true
		;;

		-s|--dimensiones-disco|--new-disk-size)
			KVM_NEW_DISK_SIZE="${2}"
			shift 2 || true
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

if [ -z "${KVM_CD_FILE}" ]; then
	ERRORMSG "No especificaste una imagen. Abortando."
	exit 1
fi

if [ ${KVM_NEW_DISK_SIZE} -ge ${SYS_FREE_DISK} ]; then
	ERRORMSG "El espacio libre en disco es insuficiente para crear el disco virtual para la prueba. Abortando."
	exit 1
fi

if [ ${KVM_MEM} -ge ${SYS_FREE_MEM} ]; then
	ERRORMSG "El espacio libre en memoria es menor al asignado para la prueba. Abortando."
	exit 1
fi

if [ ${KVM_PROC} -ge ${SYS_PROC_NUM} ]; then
	ERRORMSG "Se ha asignado un número de procesadores mayor al presente en el sistema. Abortando."
	exit 1
fi

if [ "${KVM_NEW_DISK}" = "true" ]; then
	if ${RM} -rf "${KVM_DISK_FILE}"; then
		INFOMSG "Removiendo disco virtual obsoleto en %s." "${KVM_DISK_FILE}"
	else
		ERRORMSG "Ha ocurrido un error inesperado durante la remoción del disco virtual obsoleto ubicado en %s." "${KVM_DISK_FILE}"
		exit 1
	fi

	${MKDIR} -p "$( ${DIRNAME} "${KVM_DISK_FILE}" )"

	if ${KVM_IMG} create -f qcow2 "${KVM_DISK_FILE}" "${KVM_NEW_DISK_SIZE}G"; then
		SUCCESSMSG "Se ha creado un nuevo disco virtual de %sG en %s." "${KVM_NEW_DISK_SIZE}" "${KVM_DISK_FILE}"
	else
		ERRORMSG "Ha ocurrido un error inesperado durante la creación un nuevo disco virtual en %s." "${KVM_DISK_FILE}"
		exit 1
	fi
fi

if ${KVM} -m "${KVM_MEM}" -smp "${KVM_PROC}" -boot "${KVM_DISK_MODE}" -hda "${KVM_DISK_FILE}" -cdrom "${KVM_CD_FILE}"; then
	SUCCESSMSG "Emulación iniciada a las ${TIMESTAMP}."
	exit 0
else
	ERRORMSG "Ha ocurrido un error inesperado durante el inicio de la emulación de la imagen ubicada en %s." "${KVM_CD_FILE}"
	exit 1
fi
