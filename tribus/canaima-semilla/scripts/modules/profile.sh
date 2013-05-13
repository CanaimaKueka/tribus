#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/modules/profile.sh
# DESCRIPCIÓN: Módulo asistente para la construcción de perfiles.
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

if [ "${ACTION}" = "perfil" ]; then
	LONGOPTS="crear,listar,ayuda,uso,acerca"
	COMMAND="perfil"
	PARAMETERS="[-c|--crear]\n\
\t[-l|--listar]\n\
\t[-h|--ayuda]\n\
\t[-u|--uso]\n\
\t[-A|--acerca]\n"

elif [ "${ACTION}" = "profile" ]; then
	LONGOPTS="create,list,help,usage,about"
	COMMAND="profile"
	PARAMETERS="[-c|--create]\n\
\t[-l|--list]\n\
\t[-h|--help]\n\
\t[-u|--usage]\n\
\t[-A|--about]\n"

else
	ERRORMSG "Error interno"
	exit 1
fi

SHORTOPTS="clhuA"
DESCRIPTION="$( NORMALMSG "Comando para la gestión de perfiles de distribuciones derivadas." )"

OPTIONS="$( ${GETOPT} --shell="sh" --name="${0}" --options="${SHORTOPTS}" --longoptions="${LONGOPTS}" -- "${@}" )"

if [ ${?} != 0 ]; then
	ERRORMSG "Ocurrió un problema interpretando los parámetros."
	exit 1
fi

eval set -- "${OPTIONS}"

while true; do
	case "${1}" in
		-c|--crear|--create)
			PROFILE_OP_MODE="create"
			shift 1 || true
		;;

		-l|--listar|--list)
			PROFILE_OP_MODE="list"
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

case ${PROFILE_OP_MODE} in
	create)
		PTEMPLATE="${FUNCTIONS}/newprofile.sh"
		PTMP="$( ${TEMPFILE} )"
		VARTMP="$( ${TEMPFILE} )"
		COMTMP="$( ${TEMPFILE} )"
		COPYTMP="$( ${TEMPFILE} )"

		${ECHO}
		NORMALMSG "Vamos a hacerte algunas preguntas con respecto a la distribución que deseas crear."
		NORMALMSG "Si no estás seguro de la información que se te pide, puedes presionar CTRL+C"
		NORMALMSG "en cualquier momento y volver a ejecutar el asistente cuando estés listo."
		${ECHO}
		NORMALMSG "Estás listo para crear el perfil? Presiona Y para continuar o N para cancelar."

		read -p "[Y/N]" CONTINUE

		if [ "${CONTINUE}" = "Y" ]; then
		        ${CP} ${PTEMPLATE} ${PTMP}
		        ${CAT} ${PTEMPLATE} | ${GREP} "#.*=.*@@.*" > ${VARTMP}
        		${CAT} ${PTEMPLATE} | ${GREP} "INFOMSG" > ${COMTMP}
        		${CAT} ${PTEMPLATE} | ${GREP} "# WHERE" > ${COPYTMP}
		        COUNT=$( ${CAT} ${VARTMP} | ${WC} -l )
			PROFILE_CREATED=0

		        ${ECHO}
		        NORMALMSG "Completa la siguiente información y luego presiona la tecla enter para confirmar:"
		        ${ECHO}

		        for LINE in $( ${SEQ} 1 ${COUNT} ); do
		                DESCRIPTION="$( ${SED} -n ${LINE}p ${COMTMP} | ${SED} 's|INFOMSG ||g;s|"||g' )"
				eval "COPY=\"$( ${SED} -n ${LINE}p ${COPYTMP} | ${AWK} '{print $4}' )\""
                		COPYTYPE="$( ${SED} -n ${LINE}p ${COPYTMP} | ${AWK} '{print $3}' )"
                		VARONLY="$( ${SED} -n ${LINE}p ${VARTMP} | ${SED} "s/=.*//g;s/# //g" )"

		                ${ECHO} ${DESCRIPTION}
		                read -p "${VARONLY}=" VALUE

				eval "${VARONLY}=\"${VALUE}\""
                		${ECHO}

				if [ -z "${PROFILE_NAME}" ]; then
					ERRORMSG "No puede dejar el campo 'PROFILE_NAME' vacío."
					exit 1
				fi

				if [ -e "${PROFILES}/${PROFILE_NAME}" ] && [ ${PROFILE_CREATED} -eq 0 ]; then
					ERRORMSG "Ya existe un perfil con nombre '%s'" "${PROFILE_NAME}"
					exit 1
				fi

				if [ -n "${COPY}" ] && [ -n "${VALUE}" ]; then
					if  [ -e "${VALUE}" ]; then

						if [ "${COPYTYPE}" = "FOLDER" ]; then
							${MKDIR} -p "${COPY}"
						elif [ "${COPYTYPE}" = "FILE" ]; then
							${MKDIR} -p "$( ${DIRNAME} "${COPY}" )"
						fi

						PROFILE_CREATED=1
						${CP} "${VALUE}" "${COPY}"
						${SED} -i "s|# ${VARONLY}=.*|${VARONLY}=\"profile\"|g" ${VARTMP}

					else
						ERRORMSG "La ruta '%s' no existe." "${VALUE}"
						exit 1
					fi
				else
					${SED} -i "s|# ${VARONLY}=.*|${VARONLY}=\"${VALUE}\"|g" ${VARTMP}
				fi

        		done

			${MKDIR} -p "${PROFILES}/${PROFILE_NAME}"
			${CP} "${VARTMP}" "${PROFILES}/${PROFILE_NAME}/profile.conf"
			${CHMOD} 644 "${PROFILES}/${PROFILE_NAME}/profile.conf"
			${RM} -rf "${PTMP}" "${VARTMP}" "${COMTMP}" "${COPYTMP}"

		elif [ "${CONTINUE}" = "N" ]; then
		        ERRORMSG "Cancelado."
		        exit 1
		else
		        ERRORMSG "Opción '%s' desconocida, cancelando." "${CONTINUE}"
		        exit 1
		fi
	;;

	list)
		${LS} -1 "${PROFILES}/"
		exit 0
	;;

esac
