#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: tribus
# ARCHIVO: tbs.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./tbs.sh [MÓDULO] [PARÁMETROS] [...]
# COPYRIGHT:
#       (C) 2013 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
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

# Determinando directorio de ejecución
BINDIR="$( dirname "$( readlink -f "${0}")" )"

# Asignando directorios de trabajo
if [ "${BINDIR}" = "/usr/bin" ]; then
	BASEDIR="/usr/share/tribus"
elif [ -e "${BINDIR}/tribus/cli/base.sh" ]; then
	BASEDIR="${BINDIR}/tribus"
else
	echo "Abortando, existe una inconsistencia en la estructura de archivos de Tribus."
	exit 1
fi

# Cargando variables de uso común
. "${BASEDIR}/cli/base.sh"

# Determinando acción invocada
ACTION=${1}
[ -n "${ACTION}" ] && shift 1 || true

# Delegando acciones a los módulos/comandos
case ${ACTION} in
	-h|--ayuda|--help)
		if ${MAN} -w "${COMMAND}" 1>/dev/null 2>&1; then
			${MAN} "${COMMAND}"
			exit 0
		else
			USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
			exit 0
		fi
	;;

	-u|--uso|--usage|'')
		USAGE "${COMMAND}" "${DESCRIPTION}" "${PARAMETERS}"
		exit 0
	;;

	-A|--acerca|--about)
		ABOUT
		exit 0
	;;

	*)
		# Cargando valores predeterminados del módulo
		. "${BASEDIR}/cli/${ACTION}/defaults.sh"

		# Corriendo rutinas de inicio del módulo
		. "${BASEDIR}/cli/${ACTION}/init.sh"

		# Ejecutando módulo
		MODULE "${ACTION}.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;
esac
