#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/modules.sh
# DESCRIPCIÓN: Funciones encargadas de delegar acciones a los módulos.
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

MODULE() {

	# ======================================================================
	# FUNCIÓN: MODULE
	# DESCRIPCIÓN: Función que se encarga de validar e invocar al módulo
	#	      apropiado según los parámetros introducidos.
	# ENTRADAS:
	#       [MODULE]: Nombre de módulo.
	#       [ACTION]: Palabra con la cuál fue invocado el módulo.
	#       [BINDIR]: Directorio actual del script principal de c-s.
	# ======================================================================

	MODULE="${1}"
	[ -n "${MODULE}" ] && shift 1 || true
	ACTION="${1}"
	[ -n "${ACTION}" ] && shift 1 || true
	BINDIR="${1}"
	[ -n "${BINDIR}" ] && shift 1 || true

	if [ -z "${MODULE}" ]; then
		ERRORMSG "La función '%s' necesita el nombre de un módulo como primer argumento." "${FUNCNAME}"
		exit 1
	fi

	if [ -z "${BINDIR}" ]; then
		ERRORMSG "La función '%s' necesita el nombre de un directorio como segundo argumento." "${FUNCNAME}"
		exit 1
	fi

	if [ -x "${MODULES}/${MODULE}" ]; then
		exec "${MODULES}/${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "/usr/share/canaima-semilla/scripts/modules/${MODULE}" ]; then
		exec "/usr/share/canaima-semilla/scripts/modules/${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	elif [ -x "$( ${WHICH} "${MODULE}" 2>/dev/null )" ]; then
		exec "${MODULE}" "${ACTION}" "${BINDIR}" "${@}"
	else
		ERRORMSG "'%s' no parece ser un módulo válido de '%s'." "${MODULE}" "${CS_NAME}"
		ERRORMSG "Por favor reinstala canaima-semilla o verifica que has escrito bien el comando."
		exit 1
	fi
}
