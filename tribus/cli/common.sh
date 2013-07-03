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


USAGE() {

	# ======================================================================
	# FUNCIÓN: USAGE
	# DESCRIPCIÓN: Función que explica el uso de un determinado módulo.
	# ENTRADAS:
	#       [COMMAND]: Nombre del módulo invocado.
	#       [DESCIPTION]: Descripción del módulo invocado.
	#       [PARAMETERS]: Parámetros del módulo invocado.
	# ======================================================================

	COMMAND="${1}"
	[ -n "${COMMAND}" ] && shift 1 || true
	DESCRIPTION="${1}"
	[ -n "${DESCRIPTION}" ] && shift 1 || true
	PARAMETERS="${1}"
	[ -n "${PARAMETERS}" ] && shift 1 || true

	. "${BASEDIR}/VERSION"

	if [ "${COMMAND}" = "${CS_CMD}" ]; then
		USAGE_CMD="${COMMAND}"
		MAN_CMD="${COMMAND}"
	else
		USAGE_CMD="${CS_CMD} ${COMMAND}"
		MAN_CMD="${CS_CMD}_${COMMAND}"
	fi

	NORMALMSG "%s, version %s - %s" "${CS_NAME}" "${VERSION}" "${RELDATE}"
	${PRINTF} "%s - %s\n" "${CS_AUTHOR}" "${CS_URL}"
	${ECHO}
	${PRINTF} "%s - %s\n" "${USAGE_CMD}" "${DESCRIPTION}"
	${ECHO}
	NORMALMSG "Uso:"
	${ECHO}
	${PRINTF} "  %s [-h|--ayuda|--help]\n" "${USAGE_CMD}"
	${PRINTF} "  %s [-u|--uso|--usage]\n" "${USAGE_CMD}"
	${PRINTF} "  %s [-A|--acerca|--about]\n" "${USAGE_CMD}"
	${ECHO}
	${PRINTF} "  %s ${PARAMETERS}\n" "${USAGE_CMD}"
	${ECHO}
	NORMALMSG "Puede ejecutar 'man %s' para mayor información." "${MAN_CMD}"
	${ECHO}

	exit 0
}

ABOUT() {

	# ======================================================================
	# FUNCIÓN: ABOUT
	# DESCRIPCIÓN: Función para mostrar la versión, autores y licencia.
	# ======================================================================

	. "${BASEDIR}/VERSION"

	${PRINTF} "%s, version %s\n" "${CS_NAME}" "${VERSION}"
	${PRINTF} "Code state (Git Commit): %s\n" "${COMMIT}"
	${ECHO}
	${PRINTF} "This program is a part of %s\n" "${CS_PKG}"
	${ECHO}
	${ECHO} "(C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>"
	${ECHO} "(C) 2012 Niv Sardi <xaiki@debian.org>"
	${ECHO}
	${ECHO} "This program is free software: you can redistribute it and/or modify"
	${ECHO} "it under the terms of the GNU General Public License as published by"
	${ECHO} "the Free Software Foundation, either version 3 of the License, or"
	${ECHO} "(at your option) any later version."
	${ECHO}
	${ECHO} "This program is distributed in the hope that it will be useful,"
	${ECHO} "but WITHOUT ANY WARRANTY; without even the implied warranty of"
	${ECHO} "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the"
	${ECHO} "GNU General Public License for more details."
	${ECHO}
	${ECHO} "You should have received a copy of the GNU General Public License"
	${ECHO} "along with this program. If not, see <http://www.gnu.org/licenses/>."
	${ECHO}
	${ECHO} "On Debian systems, the complete text of the GNU General Public License"
	${ECHO} "can be found in /usr/share/common-licenses/GPL-3 file."
	${ECHO}
	${ECHO} "Homepage: <http://code.google.com/p/canaima-semilla/>"
	${ECHO}

	exit 0
}

