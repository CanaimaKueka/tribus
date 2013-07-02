#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/build.sh
# DESCRIPCIÓN: Módulo para la construcción de imágenes instalables basadas
#	      en perfiles predefinidos.
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

if [ "${ACTION}" = "construir" ]; then
	LONGOPTS="arquitectura:,medio:,sabor:,archivo-config:,dir-construir:,solo-construir,solo-configurar,mostrar-variables,expresivo,silencioso,ayuda,uso,acerca"
	COMMAND="construir"
	PARAMETERS="[-a|--arquitectura i386|amd64]\n\
\t[-m|--medio usb|iso|hybrid]\n\
\t[-s|--sabor popular|primera-base|...]\n\
\t[-f|--archivo-config ARCHIVO]\n\
\t[-d|--dir-construir DIR]\n\
\t[-b|--solo-construir]\n\
\t[-c|--solo-configurar]\n\
\t[-D|--mostrar-variables]\n\
\t[-v|--expresivo]\n\
\t[-q|--silencioso]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "build" ]; then
	LONGOPTS="architecture:,image:,profile:,config-file:,build-dir:,build-only,config-only,var-dump,verbose,quiet,help,usage,about"
	COMMAND="build"
	PARAMETERS="[-a|--architecture i386|amd64]\n\
\t[-m|--image usb|iso|hybrid]\n\
\t[-s|--profile popular|primera-base|...]\n\
\t[-f|--config-file FILE]\n\
\t[-d|--build-dir DIR]\n\
\t[-b|--build-only]\n\
\t[-c|--config-only]\n\
\t[-D|--var-dump]\n\
\t[-v|--verbose]\n\
\t[-q|--quiet]\n\
\t[-h|--help]\n\
\t[-u|--usage]\n\
\t[-A|--about]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="a:m:s:f:d:bcDvqhuA"
DESCRIPTION="$( NORMALMSG "Comando para la construcción de imágenes instalables." )"

OPTIONS="$( ${GETOPT} --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ ${?} != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-a|--arquitectura|--architecture)
			ARCH="${2}"
			shift 2 || true
		;;

		-m|--medio|--image)
			MEDIO="${2}"
			shift 2 || true
		;;

		-s|--sabor|--profile)
			SABOR="${2}"
			shift 2 || true
		;;

		-f|--archivo-config|--config-file)
			EXTRACONF="${2}"
			shift 2 || true
		;;

		-d|--dir-construir|--build-dir)
			BUILDDIR="${2}"
			shift 2 || true
		;;

		-b|--solo-construir|--build-only)
			BUILD_OP_MODE="buildonly"
			shift 1 || true
		;;

		-c|--solo-configurar|--config-only)
			BUILD_OP_MODE="configonly"
			shift 1 || true
		;;

		-D|--mostrar-variables|--var-dump)
			BUILD_OP_MODE="vardump"
			shift 1 || true
		;;

		-v|--expresivo|--verbose)
			BUILD_PRINT_MODE="verbose"
			shift 1 || true
		;;

		-q|--silencioso|--quiet)
			BUILD_PRINT_MODE="quiet"
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

SWITCHLOG="on"

if [ -n "${BUILDDIR}" ]; then
	if [ -d "${BUILDDIR}" ]; then
		ISOS="${BUILDDIR}"
		INFOMSG "Utilizando %s para construir la imagen." "${BUILDDIR}"
	else
		ERRORMSG "El directorio '%s' establecido a través de la opción --dir-construir no existe." "${BUILDDIR}"
		exit 1
	fi
fi

case ${BUILD_OP_MODE} in
	configonly|vardump|normal)

		if [ -z "${SABOR}" ]; then
			SABOR="popular"
			INFOMSG "No especificaste un sabor, utilizando sabor '%s' por defecto." "${SABOR}"
		fi

		if [ -z "${ARCH}" ]; then
			ARCH="${NATIVE_ARCH}"
			INFOMSG "No especificaste una arquitectura, utilizando '%s' presente en el sistema." "${ARCH}"
		fi

		if [ -z "${MEDIO}" ]; then
			MEDIO="iso-hybrid"
			INFOMSG "No especificaste un tipo de formato para la imagen, utilizando medio '%s' por defecto." "${MEDIO}"
		fi

		if [ ! -d "${ISOS}" ]; then
			ERRORMSG "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
			exit 1
		fi

		if [ ! -d "${PROFILES}" ]; then
			ERRORMSG "La carpeta de perfiles '%s' no existe o no es un directorio válido." "${PROFILES}"
			exit 1
		fi

		if [ ! -d "${PROFILES}/${SABOR}" ]; then
			ERRORMSG "El perfil '%s' no existe dentro de la carpeta de perfiles '%s'." "${SABOR}" "${PROFILES}"
			exit 1
		fi

       		CS_CLEAN_TREE "${ISOS}" "${BUILD_OP_MODE}" "${BUILD_PRINT_MODE}"
		CS_LOAD_PROFILE "${ISOS}" "${PROFILES}" "${SABOR}" "${ARCH}" "${MEDIO}" "${BUILD_OP_MODE}" "${BUILD_PRINT_MODE}" "${EXTRACONF}"
		CS_CREATE_TREE "${ISOS}" "${BUILD_OP_MODE}" "${BUILD_PRINT_MODE}"
	;;
esac

case ${BUILD_OP_MODE} in
	buildonly|normal)

		if [ ! -d "${ISOS}" ]; then
			ERRORMSG "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
			exit 1
		fi

		CS_BUILD_IMAGE "${ISOS}" "${BUILD_OP_MODE}" "${BUILD_PRINT_MODE}"
	;;
esac
