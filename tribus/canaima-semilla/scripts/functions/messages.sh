#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/messages.sh
# DESCRIPCIÓN: Funciones encargadas de mostrar, traducir e introducir mensajes
#	      en los archivos de log.
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

NORMALMSG() {

	# ======================================================================
	# FUNCIÓN: NORMALMSG
	# DESCRIPCIÓN: Función simple para mostrar un texto traducido y
	#	      guardarlo en el log.
	# ENTRADAS:
	#       [NORMALMSG]: Texto.
	# ======================================================================

	NORMALMSG="${1}"

	if [ -n "${NORMALMSG}" ]; then
		shift 1 || true
		LOCALIZED="$( ${GETTEXT} -s "${NORMALMSG}" )"
		${PRINTF} "${LOCALIZED}\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "${LOCALIZED}\n" >> "${ISOS}/${LOGFILE}"
		fi

	fi
}

DEBUGMSG() {

	# ======================================================================
	# FUNCIÓN: DEBUGMSG
	# DESCRIPCIÓN: Función para mostrar y añadir al log una variable y su
	#	      valor.
	# ENTRADAS:
	#       [DEBUGVAR]: Variable a evaluar.
	# ======================================================================

	DEBUGVAR="${1}"
	eval "DEBUGVALUE=\"\${${DEBUGVAR}}\""

	if [ -n "${DEBUGVAR}" ]	&& [ -n "${DEBUGVALUE}" ] && [ "${BUILD_OP_MODE}" = "vardump" ]; then
		shift 1 || true
		${PRINTF} "${YELLOW}${DEBUGVAR}${END}='${DEBUGVALUE}'\n"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[DEBUG] ${DEBUGVAR}='${DEBUGVALUE}'\n" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

CONFIGMSG() {

	# ======================================================================
	# FUNCIÓN: CONFIGMSG
	# DESCRIPCIÓN: Función para mostrar, traducir y añadir al log un
	#	      mensaje de configuración en conjunto con la variable
	#	      que está siendo modificada.
	# ENTRADAS:
	#       [CONFIGMSG]: Texto de configuración.
	#       [CONFIGVAR]: Variable de configuración.
	# ======================================================================


	CONFIGMSG="${1}"
	[ -n "${CONFIGMSG}" ] && shift 1 || true

	CONFIGVAR="${1}"
	[ -n "${CONFIGVAR}" ] && shift 1 || true

	if [ -n "${CONFIGMSG}" ] && [ -n "${CONFIGVAR}" ] && [ "${BUILD_PRINT_MODE}" = "normal" ]; then
		LOCALIZED="$( ${GETTEXT} -s "${CONFIGMSG}" )"
		${PRINTF} "${UNDERSCORE}${CONFIGVAR}${END}: ${LOCALIZED} ...\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[CONFIG] ${CONFIGVAR}: ${LOCALIZED} ...\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

INFOMSG() {

	# ======================================================================
	# FUNCIÓN: INFOMSG
	# DESCRIPCIÓN: Función simple para mostrar, traducir y añadir al log un
	#	      mensaje de información.
	# ENTRADAS:
	#       [INFOMSG]: Texto.
	# ======================================================================

	INFOMSG="${1}"

	if [ -n "${INFOMSG}" ] && [ "${BUILD_PRINT_MODE}" = "verbose" ]; then
		shift 1 || true
		LOCALIZED="$( ${GETTEXT} -s "${INFOMSG}" )"
		${PRINTF} "${LOCALIZED}\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[INFO] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

WARNINGMSG() {

	# ======================================================================
	# FUNCIÓN: WARNINGMSG
	# DESCRIPCIÓN: Función simple para mostrar, traducir y añadir al log un
	#	      mensaje de advertencia.
	# ENTRADAS:
	#       [WARNINGMSG]: Texto.
	# ======================================================================

	WARNINGMSG="${1}"

	if [ -n "${WARNINGMSG}" ] && [ "${BUILD_PRINT_MODE}" = "verbose" ]; then
		shift 1 || true
		LOCALIZED="$( ${GETTEXT} -s "${WARNINGMSG}" )"
		${PRINTF} "${YELLOW}${LOCALIZED}${END}\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[WARNING] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

ERRORMSG() {

	# ======================================================================
	# FUNCIÓN: ERRORMSG
	# DESCRIPCIÓN: Función simple para mostrar, traducir y añadir al log un
	#	      mensaje de error.
	# ENTRADAS:
	#       [ERRORMSG]: Texto.
	# ======================================================================

	ERRORMSG="${1}"

	if [ -n "${ERRORMSG}" ]; then
		shift 1 || true
		LOCALIZED="$( ${GETTEXT} -s "${ERRORMSG}" )"
		${PRINTF} "${LRED}${LOCALIZED}${END}\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[ERROR] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

SUCCESSMSG() {

	# ======================================================================
	# FUNCIÓN: SUCCESSMSG
	# DESCRIPCIÓN: Función simple para mostrar, traducir y añadir al log un
	#	      mensaje de éxito.
	# ENTRADAS:
	#       [SUCCESSMSG]: Texto.
	# ======================================================================

	SUCCESSMSG="${1}"

	if [ -n "${SUCCESSMSG}" ]; then
		shift 1 || true
		LOCALIZED="$( ${GETTEXT} -s "${SUCCESSMSG}" )"
		${PRINTF} "${LGREEN}${LOCALIZED}${END}\n" "${@}"
		if [ "${SWITCHLOG}" = "on" ]; then
			${PRINTF} "[SUCCESS] ${LOCALIZED}\n" "${@}" >> "${ISOS}/${LOGFILE}"
		fi
	fi
}

