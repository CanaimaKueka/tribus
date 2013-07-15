#!/bin/bash -e
#
# ==============================================================================
# PAQUETE: canaima-desarrollador
# ARCHIVO: canaima-desarrollador.sh
# DESCRIPCIÓN: Script de bash principal del paquete canaima-desarrollador
# COPYRIGHT:
#  (C) 2010 Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>
#  (C) 2010 Diego Alberto Aguilera Zambrano <daguilera85@gmail.com>
#  (C) 2010 Carlos Alejandro Guerrero Mora <guerrerocarlos@gmail.com>
#  (C) 2010 Francisco Javier Vásquez Guerrero <franjvasquezg@gmail.com>
# LICENCIA: GPL3
# ==============================================================================
#
# Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los
# términos de la Licencia Pública General de GNU (versión 3).

VARIABLES="/usr/share/canaima-desarrollador/variables.conf"

# Inicializando variables
. ${VARIABLES}

# Cargando configuración
. ${CONF}

# Cargando funciones
. ${FUNCIONES}

# Función para chequear que ciertas condiciones se cumplan para el
# correcto funcionamiento de canaima-desarrollador
# Ver /usr/share/canaima-desarrollador/scripts/funciones-desarrollador.sh
CHECK

# Función para cargar los datos del desarrollador especificados en
# ${CONF} (nombre, correo, etc.)
# Ver /usr/share/canaima-desarrollador/scripts/funciones-desarrollador.sh
DEV-DATA

# Capturamos los parámetros 
PARAMETROS=${@}

# Si hay parámetros, y no existen parámetros de ayuda ...
if [ -n "${PARAMETROS}" ] && [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) == 0 ] && [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) == 0 ]; then

# Removemos el ayudante
PARAMETROS=${PARAMETROS#${1}}

# Damos formato a los parámetros para que sean seleccionados correctamente por el ciclo for
PARAMETROS=$( echo ${PARAMETROS} | sed 's/=/="/g' )
PARAMETROS=$( echo ${PARAMETROS} | sed 's/ --/"#####--/g' )
PARAMETROS=$( echo ${PARAMETROS} | sed 's/ /_____/g' )
PARAMETROS=$( echo ${PARAMETROS} | sed 's/#####/ /g' )
[ -n "${PARAMETROS}" ] && PARAMETROS="${PARAMETROS}\""

# Parseamos cada parámetro y lo convertimos en variable
for ARGUMENTO in ${PARAMETROS}; do
ARG_VARIABLE=${ARGUMENTO#--}
ARG_VARIABLE=${ARG_VARIABLE%=*}
ARG_VALOR=${ARGUMENTO#--${ARG_VARIABLE}=}
ARG_VALOR=$( echo ${ARG_VALOR} | sed 's/_____/ /g' )
ARG_VARIABLE=$( echo ${ARG_VARIABLE} | tr '[:lower:]' '[:upper:]' )
ARG_VARIABLE=$( echo ${ARG_VARIABLE} | tr '-' '_' )
eval "${ARG_VARIABLE}=${ARG_VALOR}"
done

fi

# Case encargado de interpretar los parámetros introducidos a
# canaima-desarrollador y ejecutar la función correspondiente
case ${1} in

#------ AYUDANTES CREADORES --------------------------------------------------------------------------------------#
#=================================================================================================================#

crear-proyecto|debianizar)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/crear-proyecto"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-nombre" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-version" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-destino" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-licencia" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardemos los parámetros en variables para usarlos después
opcion=${1}
nombre=${NOMBRE}
version=${VERSION}
destino=${DESTINO}
licencia=${LICENCIA}
CREAR-PROYECTO
fi
;;

crear-fuente)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/crear-fuente"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-directorio" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardando directorio en variable para utilizarlo después
directorio=${DIRECTORIO}
CREAR-FUENTE
fi
;;

empaquetar)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/empaquetar"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-directorio" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-mensaje" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-procesadores" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-no-enviar" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

[ $( echo ${PARAMETROS} | grep -c "\-\-no-enviar" ) == 1 ] && NO_ENVIAR=1
# Guardamos los parámetros en variables para usarlas después
directorio=${DIRECTORIO}
mensaje=${MENSAJE}
procesadores=${PROCESADORES}
EMPAQUETAR
fi
;;

#------ AYUDANTES GIT --------------------------------------------------------------------------------------------#
#=================================================================================================================#
descargar|clonar|clone)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/descargar"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-proyecto" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardemos el segundo argumento en la varible "proyecto"
proyecto=${PROYECTO}
# Ejecutemos la función correspondiente
DESCARGAR
fi
;;

registrar|commit)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/registrar"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-directorio" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-mensaje" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardemos los parámetros en variables para usarlos después
directorio=${DIRECTORIO}
mensaje=${MENSAJE}
REGISTRAR
fi
;;

enviar|push)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/enviar"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-directorio" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardando directorio en variable para utilizarlo después
directorio=${DIRECTORIO}
ENVIAR
fi
;;

actualizar|pull)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/actualizar"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-directorio" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

# Guardando directorio en variable para utilizarlo después
directorio=${DIRECTORIO}
ACTUALIZAR
fi
;;

#------ AYUDANTES MASIVOS ----------------------------------------------------------------------------------------#
#=================================================================================================================#

descargar-todo|clonar-todo)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/descargar-todo"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
DESCARGAR-TODO
fi
;;

registrar-todo|commit-todo)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/registrar-todo"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
mensaje="auto"
REGISTRAR-TODO
fi
;;

enviar-todo|push-todo)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/enviar-todo"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
ENVIAR-TODO
fi
;;

actualizar-todo|pull-todo)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/actualizar-todo"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
ACTUALIZAR-TODO
fi
;;

empaquetar-varios)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/empaquetar-varios"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-para-empaquetar" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-procesadores" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-no-enviar" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

[ $( echo ${PARAMETROS} | grep -c "\-\-no-enviar" ) == 1 ] && NO_ENVIAR=1
# Guardamos los parámetros en variables para usarlas después
para_empaquetar=${PARA_EMPAQUETAR}
mensaje="auto"
procesadores=${PROCESADORES}
EMPAQUETAR-VARIOS
fi
;;

empaquetar-todo)
if [ -z "${PARAMETROS}" ] || [ $( echo ${PARAMETROS} | grep -c "\-\-ayuda" ) != 0 ] || [ $( echo ${PARAMETROS} | grep -c "\-\-help" ) != 0 ]; then
cat "${DIR_AYUDA}/empaquetar-todo"
else

for VERIFICAR in ${PARAMETROS}; do
[ $( echo ${VERIFICAR} | grep -c "\-\-procesadores" ) == 0 ] && [ $( echo ${VERIFICAR} | grep -c "\-\-no-enviar" ) == 0 ] && ERROR "No conozco la opción '${VERIFICAR}', revisa la documentación." && exit 1
done

[ $( echo ${PARAMETROS} | grep -c "\-\-no-enviar" ) == 1 ] && NO_ENVIAR=1
mensaje="auto"
procesadores=${PROCESADORES}
EMPAQUETAR-TODO
fi
;;


#------ AYUDANTES INFORMATIVOS -----------------------------------------------------------------------------------------#
#=======================================================================================================================#

listar-remotos)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/listar-remotos"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
LISTAR-REMOTOS
fi
;;

listar-locales)
if [ "${2}" == "--ayuda" ] || [ $"{2}" == "--help" ]; then
cat "${DIR_AYUDA}/listar-locales"
else
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
LISTAR-LOCALES
fi
;;

--ayuda|--help|'')
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
# Imprimiendo la ayuda
cat "${DIR_AYUDA}/canaima-desarrollador"
;;

debug)
[ -n "${2}" ] && ERROR "No conozco la opción '${2}', revisa la documentación." && exit 1
LISTA_DATOS="DEV_NAME DEV_MAIL DEV_GPG DEV_DIR DEPOSITO_SOURCES DEPOSITO_LOGS DEPOSITO_DEBS REPO REPO_USER REPO_DIR CONF VARIABLES PLANTILLAS FUNCIONES NAVEGADOR"
for VARIABLES_CONF in ${LISTA_DATOS}; do
eval "VARIABLES_CONF_EVAL=\$${VARIABLES_CONF}"
echo "${VARIABLES_CONF}=\"${VARIABLES_CONF_EVAL}\""
done
;;

*)
ERROR "No conozco el ayudante '"${1}"', échale un ojo a la documentación (man canaima-desarrollador)"
;;
esac

exit 0
