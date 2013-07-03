#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/init.sh
# DESCRIPCIÓN: Rutina auxiliar para la preparación y validación del ambiente
#	      de ejecución del script principal.
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



# Asignando información para --help, --usage
COMMAND="c-s"
DESCRIPTION="$( NORMALMSG "Generador de distribuciones derivadas" )"
PARAMETERS="\t[construir|build] [...] [--help]\n\
\t[perfil|profile] [...] [--help]\n\
\t[grabar|save] [...] [--help]\n\
\t[probar|test] [...] [--help]\n"

TIMESTAMP="$( date +%Y%m%d%H%M )"
NATIVE_ARCH="$( dpkg --print-architecture )"
LOGFILE="${LOGFILE:-build.${TIMESTAMP}.log}"

CONFIG="${CONFIG:-${BASEDIR}/cli/common/config.sh}"
LIBRARY="${LIBRARY:-${BASEDIR}/cli/common/library.sh}"
VARIABLES="${VARIABLES:-${CONFDIR}/config/core}"
# FUNCTIONS="${FUNCTIONS:-${BASEDIR}/scripts/functions}"
# MODULES="${MODULES:-${BASEDIR}/scripts/modules}"
# PROFILES="${PROFILES:-${BASEDIR}/profiles}"
# SCRIPTS="${SCRIPTS:-${BASEDIR}/scripts}"
# ISOS="${ISOS:-${BASEDIR}/isos}"
# TEMPLATES="${TEMPLATES:-${BASEDIR}/templates}"


# Inicializando variables
# Un archivo variables.conf en ${ISOS} sobreescribe la configuración por defecto
for _FILE in ${CONFIG}; do
	if [ -f "${_FILE}" ]; then
		. "${_FILE}"
	fi
done

# Inicializando funciones
# Un archivo lib.sh en ${ISOS} sobreescribe la configuración por defecto
for _FILE in ${LIBRARY}; do
	if [ -f "${_FILE}" ]; then
		. "${_FILE}"
	fi
done

# Añadiendo directorios de ejecución a ${PATH} para permitir
# ubicarlos rápidamente
export PATH="${BINDIR%/}:${SCRIPTS%/}:${MODULES%/}:${PATH}"

# Comprobando estado previo a la ejecución de módulos
if [ $( ${ID} -u ) != 0 ]; then
	echo "Canaima Semilla debe ser ejecutado como usuario root."
	exit 1
fi

if [ ! -f "${CONFIG}" ]; then
	echo "El archivo de configuración '%s' no existe o no es ejecutable." "${CONFIG}"
	exit 1
fi

if [ ! -f "${LIBRARY}" ]; then
	echo "La librería de funciones principales '%s' no existe o no es ejecutable." "${LIBRARY}"
	exit 1
fi

if [ ! -d "${FUNCTIONS}" ]; then
	echo "El directorio que contiene las funciones '%s' no existe." "${FUNCTIONS}"
	exit 1
fi

if [ ! -d "${MODULES}" ]; then
	echo "El directorio que contiene los módulos '%s' no existe." "${MODULES}"
	exit 1
fi

if [ ! -d "${PROFILES}" ]; then
	echo "El directorio que contiene los perfiles '%s' no existe." "${PROFILES}"
	exit 1
fi

if [ ! -d "${SCRIPTS}" ]; then
	echo "El directorio que contiene los scripts '%s' no existe." "${SCRIPTS}"
	exit 1
fi

if [ ! -d "${ISOS}" ]; then
	echo "El directorio de construcción de imágenes '%s' no existe." "${ISOS}"
	exit 1
fi

SYS_FREE_MEM="$( ${ECHO} "scale=0;$( ${CAT} "/proc/meminfo" | ${GREP} "MemFree:" | ${AWK} '{print $2}' )/(10^3)" | ${BC} )"
SYS_FREE_DISK="$( ${ECHO} "scale=0;$( ${DF} "${BASEDIR}" | ${GREP} "/" | ${AWK} '{print $4}' )/(10^6)" | ${BC} )"
SYS_PROC_NUM="$( ${CAT} "/proc/cpuinfo" | ${GREP} -c "processor" )"

FUNCTIONS="${FUNCTIONS%/}"
MODULES="${MODULES%/}"
PROFILES="${PROFILES%/}"
SCRIPTS="${SCRIPTS%/}"
ISOS="${ISOS%/}"
