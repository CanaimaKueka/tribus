#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s.sh [MÓDULO] [PARÁMETROS] [...]
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

# Determinando directorio de ejecución
BINDIR="$( dirname "$( readlink -f "${0}")" )"

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

# Determinando acción invocada
ACTION=${1}
[ -n "${ACTION}" ] && shift 1 || true

# Asignando información para --help, --usage
COMMAND="c-s"
DESCRIPTION="$( NORMALMSG "Generador de distribuciones derivadas" )"
PARAMETERS="\t[construir|build] [...] [--help]\n\
\t[perfil|profile] [...] [--help]\n\
\t[grabar|save] [...] [--help]\n\
\t[probar|test] [...] [--help]\n"

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
		MODULE "${ACTION}.sh" "${ACTION}" "${BINDIR}" "${@}"
	;;
esac
