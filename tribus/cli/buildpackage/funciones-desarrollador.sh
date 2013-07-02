#!/bin/bash -e
#
# ==============================================================================
# PAQUETE: canaima-desarrollador
# ARCHIVO: funciones-desarrollador.sh
# DESCRIPCIÓN: Funciones utilizadas por canaima-desarrollador.sh
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

#------ AYUDANTES CREADORES --------------------------------------------------------------------------------------#
#=================================================================================================================#

function CREAR-PROYECTO() {
#-------------------------------------------------------------#
# Nombre de la Función: CREAR-PROYECTO
# Propósito: Crear o debianizar un proyecto de empaquetamiento.
# Dependencias:
#       - Requiere la carga del archivo ${CONF}
#-------------------------------------------------------------#

# Comprobaciones varias
# El nombre del proyecto está vacío
[ -z "${nombre}" ] && ERROR "Olvidaste ponerle un nombre al paquete." && exit 1
# El nombre del proyecto contiene un carácter inválido 
[ $( echo "${nombre}" | grep -c "[\?\*\+\.\\\/\%\$\#\@\!\~\=\^\<\>\ ]" ) != 0 ] && ERROR "Caracteres no permitidos en el nombre del paquete. Trata algo con letras, \"-\" y \"_\" solamente." && exit 1
# Si estamos debianizando, ¿El directorio coincide con el nombre y versión del paquete?
[ "${opcion}" == "debianizar" ] && [ ! -e "${DEV_DIR}${nombre}-${version}" ] && ERROR "¡Hey! No encuentro ningún directorio llamado \"${nombre}-${version}\" en ${DEV_DIR}" && exit 1
# Paramos si es un nuevo proyecto y la carpeta ya existe
[ -e "${DEV_DIR}${nombre}-${version}" ] && [ "${opcion}" == "crear-proyecto" ] && ERROR "Estamos creando un proyecto nuevo, pero la carpeta ${DEV_DIR}${nombre}-${version} ya existe." && exit 1
# ¿Me dijiste un destino válido?
[ "${destino}" != "canaima" ] && [ "${destino}" != "personal" ] && ERROR "Sólo conozco los destinos \"personal\" y \"canaima\". ¿Para quien carrizo es \"${destino}\"?" && exit 1
# La versión está vacía
[ -z "${version}" ] && version="1.0+0" && ADVERTENCIA "No me dijiste la versión. Asumiendo 1.0+0"
# El destino está vacío
[ -z "${destino}" ] && destino="personal" && ADVERTENCIA "No me dijiste si era un proyecto personal o para Canaima GNU/Linux. Asumo que es personal."
# La licencia está vacía
[ -z "${licencia}" ] && licencia="gpl3" && ADVERTENCIA "No especificaste la licencia del paquete. Asumiré que es GPL3."
# Creamos la carpeta si no está creado (nuevo proyecto)
[ ! -e "${DEV_DIR}${nombre}-${version}" ] && mkdir -p "${DEV_DIR}${nombre}-${version}"

# Asignando strings dependiendo de la licencia escogida
case ${licencia} in
gpl3) LICENSE="GPL-3" ;;
apache) LICENSE="Apache-2.0" ;;
artistic) LICENSE="Artistic" ;;
bsd) LICENSE="BSD" ;;
gpl) LICENSE="GPL-3" ;;
gpl2) LICENSE="GPL-2" ;;
gpl3) LICENSE="GPL-3" ;;
lgpl) LICENSE="LGPL-3" ;;
lgpl2) LICENSE="LGPL-2" ;;
lgpl3) LICENSE="LGPL-3" ;;
*) ERROR "Licencia '${licencia}' no soportada." && exit 1 ;;
esac

# Accedemos al directorio
cd "${DEV_DIR}${nombre}-${version}"
# Creamos el proyecto mediante dh_make. Lo pasamos a través de un pipe que le pasa una string
# a stdin para saltarnos la confirmación que trae por defecto dh_make. También enviamos todas
# las salidas a /dev/null para no ver las cosas en pantalla.
echo "enter" | dh_make --createorig --cdbs --copyright ${licencia} --email ${DEV_MAIL} > /dev/null 2>&1

[ ! -d "${DEV_DIR}${nombre}-${version}/debian/" ] && ERROR "Algo salió mal con la creación de la carpeta debian." && exit 1
# Presentamos alguna información en pantalla a modo de informe.
echo "Nombre del Paquete: ${nombre}"
echo "Versión: ${version}"
echo "Mantenedor: ${DEV_NAME}"
echo "Correo del Mantenedor: ${DEV_MAIL}"
echo "Licencia: ${licencia}"
# Removemos el directorio .orig creado
rm -rf "${DEV_DIR}${nombre}-${version}.orig"

# A partir de aquí personalizamos un poco lo que dh_make colocó por defecto
# Creamos la carpeta debian/ejemplos y pasamos todos los ejemplos de debian a esa
# carpeta
mkdir -p "${DEV_DIR}${nombre}-${version}/debian/ejemplos"
mv ${DEV_DIR}${nombre}-${version}/debian/*.* ${DEV_DIR}${nombre}-${version}/debian/ejemplos/

# Si el proyecto es para Canaima GNU/Linux, entonces éstos son los campos a sustituir
# en debian/control
if [ "${destino}" == "canaima" ]; then
CONTROL_MAINTAINER="Equipo de Desarrollo de Canaima GNU\/Linux <desarrolladores@canaima.softwarelibre.gob.ve>"
CONTROL_UPLOADERS="José Miguel Parrella Romero <jparrella@onuva.com>, Carlos David Marrero <cdmarrero2040@gmail.com>, Orlando Andrés Fiol Carballo <ofiol@indesoft.org.ve>, Carlos Alejandro Guerrero Mora <guerrerocarlos@gmail.com>, Diego Alberto Aguilera Zambrano <diegoaguilera85@gmail.com>, Luis Alejandro Martínez Faneyth <martinez.faneyth@gmail.com>, Francisco Javier Vásquez Guerrero <franjvasquezg@gmail.com>, Carlos Escobar <carlosescobar70@gmail.com>"
CONTROL_STANDARDS="3.9.1"
CONTROL_HOMEPAGE="http:\/\/canaima.softwarelibre.gob.ve\/"
CONTROL_VCSGIT="git:\/\/gitorious.org\/canaima-gnu-linux\/${nombre}.git"
CONTROL_VCSBROWSER="git:\/\/gitorious.org\/canaima-gnu-linux\/${nombre}.git"
# Si el proyecto es personal, entonces son éstos
elif [ "${destino}" == "personal" ]; then
CONTROL_MAINTAINER="${DEV_NAME} <${DEV_MAIL}>"
CONTROL_UPLOADERS="${CONTROL_MAINTAINER}"
CONTROL_HOMEPAGE="Desconocido"
CONTROL_VCSGIT="Desconocido"
CONTROL_VCSBROWSER="Desconocido"
fi
# Campos comunes a sustituir en debian/control
CONTROL_DESCRIPTION="Insertar una descripción de no más de 60 caracteres."
CONTROL_LONG_DESCRIPTION="Insertar descripción larga, iniciando con un espacio."
CONTROL_ARCH="all"

# Lista de archivos a copiar en la carpeta debian del proyecto
COPIAR_PLANTILLAS_DEBIAN="preinst postinst prerm postrm rules copyright"
# Lista de archivos a copiar en la carpeta base del proyecto
COPIAR_PLANTILLAS_PROYECTO="AUTHORS README TODO COPYING THANKS ${LICENSE} Makefile"
# Determinando el año en que estamos
FECHA=$( date +%Y )
# Ciclo que recorre las plantillas declaradas en ${COPIAR_PLANTILLAS_DEBIAN}
# para copiarlas en la carpeta debian del proyecto (si no existen)
for plantillas_debian in ${COPIAR_PLANTILLAS_DEBIAN}; do
cp -r "${PLANTILLAS}${plantillas_debian}" "${DEV_DIR}${nombre}-${version}/debian/"
# Aprovechamos de sustituir algunos @TOKENS@ en las plantillas
sed -i "s/@AUTHOR_NAME@/${DEV_NAME}/g" "${DEV_DIR}${nombre}-${version}/debian/${plantillas_debian}"
sed -i "s/@AUTHOR_MAIL@/${DEV_MAIL}/g" "${DEV_DIR}${nombre}-${version}/debian/${plantillas_debian}"
sed -i "s/@YEAR@/${FECHA}/g" "${DEV_DIR}${nombre}-${version}/debian/${plantillas_debian}"
sed -i "s/@PAQUETE@/${nombre}/g" "${DEV_DIR}${nombre}-${version}/debian/${plantillas_debian}"
done

# Ciclo que recorre las plantillas declaradas en ${COPIAR_PLANTILLAS_PROYECTO}
# para copiarlas en el proyecto (si no existen)
for plantillas_proyecto in ${COPIAR_PLANTILLAS_PROYECTO}; do
cp -r "${PLANTILLAS}${plantillas_proyecto}" "${DEV_DIR}${nombre}-${version}/"
# Aprovechamos de sustituir algunos @TOKENS@ en las plantillas
sed -i "s/@AUTHOR_NAME@/${DEV_NAME}/g" "${DEV_DIR}${nombre}-${version}/${plantillas_proyecto}"
sed -i "s/@AUTHOR_MAIL@/${DEV_MAIL}/g" "${DEV_DIR}${nombre}-${version}/${plantillas_proyecto}"
sed -i "s/@YEAR@/${FECHA}/g" "${DEV_DIR}${nombre}-${version}/${plantillas_proyecto}"
sed -i "s/@PAQUETE@/${nombre}/g" "${DEV_DIR}${nombre}-${version}/${plantillas_proyecto}"
done
# Cambiamos el nombre al archivo de licencia
mv "${DEV_DIR}${nombre}-${version}/${LICENSE}" "${DEV_DIR}${nombre}-${version}/LICENSE"
# Sustituimos algunos campos de debian/control, por los valores que establecimos antes
sed -i "s/#Vcs-Git:.*/#Vcs-Git: ${CONTROL_VCSGIT}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/Standards-Version:.*/Standards-Version: 3.9.1/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/#Vcs-Browser:.*/#Vcs-Browser: ${CONTROL_VCSBROWSER}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/Homepage:.*/#Homepage: ${CONTROL_HOMEPAGE}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/Maintainer:.*/Maintainer: ${CONTROL_MAINTAINER}\nUploaders: ${CONTROL_UPLOADERS}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/Description:.*/Description: ${CONTROL_DESCRIPTION}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/<insert long description, indented with spaces>/${CONTROL_LONG_DESCRIPTION}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
sed -i "s/Architecture:.*/Architecture: ${CONTROL_ARCH}/g" "${DEV_DIR}${nombre}-${version}/debian/control"
# Arreglamos algunas cosas en el debian/changelog
sed -i "s/Initial release (Closes: #nnnn)  <nnnn is the bug number of your ITP>/Versión inicial de ${nombre} para Canaima GNU\/Linux/g" "${DEV_DIR}${nombre}-${version}/debian/changelog"
sed -i "s/(.*)/(${version})/g" "${DEV_DIR}${nombre}-${version}/debian/changelog"
# Nos aseguramos de que el formato del paquete fuente y el nivel de compatibilidad sean apropiados
echo "3.0 (quilt)" > ${DEV_DIR}${nombre}-${version}/debian/source/format
echo "7" > ${DEV_DIR}${nombre}-${version}/debian/compat

# Si no existe la carpeta .git (proyecto nuevo)
if [ ! -e "${DEV_DIR}${nombre}-${version}/.git/" ]; then
# Inicializamos un proyecto git
git init > /dev/null 2>&1
ADVERTENCIA "Repositorio git inicializado"
directorio="${DEV_DIR}${nombre}-${version}"
directorio_nombre=$( basename "${directorio}" )
# Configuramos el repositorio remoto
SET-REPOS
git add .
git commit -a -m "Versión inicial de ${nombre}-${version} para Canaima GNU/Linux"
fi
# Enviamos la notificación apropiada, dependiendo del target
# "crear-proyecto" o "debianizar"
if [ "${opcion}" == "crear-proyecto" ]; then
EXITO "¡Proyecto ${nombre} creado!"
elif [ "${opcion}" == "debianizar" ]; then
EXITO "¡Proyecto ${nombre} debianizado correctamente!"
fi
ADVERTENCIA "Lee los comentarios en los archivos creados para mayor información"
}

function CREAR-FUENTE() {
#-------------------------------------------------------------#
# Nombre de la Función: CREAR-FUENTE
# Propósito: Crear un paquete fuente a partir de un proyecto
#            de empaquetamiento debian
# Dependencias:
#       - Requiere la carga del archivo ${CONF}
#-------------------------------------------------------------#

# Garanticemos que el directorio siempre tiene escrita la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# Comprobaciones varias
# El directorio está vacío
[ -z "${directorio#${DEV_DIR}}" ] && ERROR "¡Se te olvidó decirme cual era el directorio del proyecto del cuál deseas generar el paquete fuente!" && exit 1
# El directorio no existe
[ ! -d "${directorio}" ] && ERROR "El directorio no existe o no es un directorio." && exit 1
# Determinemos algunos datos de proyecto
DATOS-PROYECTO
# Si es un proyecto de empaquetamiento válido, entonces ...
if [ "${PAQUETE}" == "1" ]; then
# Determinemos si el directorio ingresado tiene un slash (/) al final
slash=${directorio#${directorio%?}}
# Si es así, lo removemos
[ "${slash}" == "/" ] && directorio=${directorio%?}
# Ingresamos a la carpeta del desarrollador
cd ${DEV_DIR}
# Corrigiendo nombre del directorio en caso de ser incorrecto
[ "${DEV_DIR}${NOMBRE_PROYECTO}-${VERSION_PROYECTO}" != ${directorio} ] && mv ${directorio} ${DEV_DIR}${NOMBRE_PROYECTO}-${VERSION_PROYECTO}
directorio="${DEV_DIR}${NOMBRE_PROYECTO}-${VERSION_PROYECTO}"
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# Removemos cualquier carpeta .orig previamente creada
rm -rf "${directorio}.orig"
# Creamos un nuevo directorio .orig
ADVERTENCIA "Creando paquete fuente ${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz"
cp -r ${directorio} "${directorio}.orig"
# Creamos el paquete fuente
dpkg-source --format="1.0" -i.git/ -I.git -b ${directorio}
# Movamos las fuentes que estén en la carpeta del desarrollador a su
# lugar en el depósito
[ "${1}" != "no-mover" ] && MOVER fuentes ${NOMBRE_PROYECTO}
# Emitimos la notificación
if [ -e "${DEPOSITO_SOURCES}${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz" ] && [ "${1}" != "no-mover" ]; then
EXITO "¡Fuente del proyecto ${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz creada y movida a ${DEPOSITO_SOURCES}!"
elif [ -e "${DEV_DIR}${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz" ] && [ "${1}" == "no-mover" ]; then
EXITO "¡Fuente del proyecto ${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz creada!"
else
ERROR "¡Epa! algo pasó durante la creación de ${NOMBRE_PROYECTO}_${VERSION_PROYECTO}.orig.tar.gz"
fi
fi
}

function EMPAQUETAR() {
#-------------------------------------------------------------#
# Nombre de la Función: EMPAQUETAR
# Propósito: Crear un paquete binario a partir de un proyecto
#            de empaquetamiento debian
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- git-buildpackage
#-------------------------------------------------------------#
if [ -z ${DEV_GPG} ]; then
	FIRMAR="-us -uc"
else
	FIRMAR="-k${DEV_GPG}"
fi
# Cálculo de los threads (n+1)
threads=$[ ${procesadores}+1 ]

# Comprobaciones varias
# No especificaste el directorio
[ -z "${directorio#${DEV_DIR}}" ] && directorio=$( pwd ) && ADVERTENCIA "No especificaste un directorio a empaquetar, asumiendo que es $( pwd )."
# Garanticemos que el directorio siempre tiene escrita la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# Tal vez te comiste el parámetro directoriorio o especificaste un directorio con espacios
[ $( echo "${directorio#${DEV_DIR}}" | grep -c " " ) != 0 ] && ERROR "Sospecho dos cosas: o te saltaste el nombre del directorio, o especificaste un directorio con espacios." && exit 1
# No especificaste un mensaje para el commit
[ -z "${mensaje}" ] && mensaje="auto" && ADVERTENCIA "Mensaje de commit vacío. Autogenerando."
# Construímos el comando de multiprocessing
[ ! -z "${procesadores}" ] && procesadores_com="-j${threads}" && ADVERTENCIA "Usando ${threads} hilos de procesamiento para construir el proyecto."
# No especificaste número de procesadores
[ -z "${procesadores}" ] && ADVERTENCIA "No especificaste número de procesadores a utilizar, asumiendo que no se quiere utilizar multiprocessing."
# El directorio no existe
[ ! -e "${directorio}" ] && ERROR "¡EPA! La carpeta \"${directorio}\" no existe en el directorio del desarrollador (${DEV_DIR})." && exit 1
# El directorio no es un directorio
[ ! -d "${directorio}" ] && ERROR "¡\"${directorio}\" no es un directorio!" && exit 1

# Obtengamos datos básicos del proyecto
DATOS-PROYECTO
# Movemos todo a sus depósitos
MOVER debs ${NOMBRE_PROYECTO}
MOVER logs ${NOMBRE_PROYECTO}
MOVER fuentes ${NOMBRE_PROYECTO}
# Accedemos al directorio
cd ${directorio}
# Hacemos commit de los (posibles) cambios hechos
REGISTRAR
if [ "${GIT_NONE}" == "0" ]; then
# Lo reflejamos en debian/changelog
[ "${NO_COMMIT}" == "0" ] && GIT-DCH
# Volvemos a hacer commit
[ "${NO_COMMIT}" == "0" ] && REGISTRAR
# Creamos el paquete fuente (formato 1.0)
CREAR-FUENTE no-mover
cd ${directorio}
# Empaquetamos
git-buildpackage ${FIRMAR} -tc ${procesadores_com}
git clean -fd
git reset --hard
# Movemos todo a sus depósitos
MOVER debs ${NOMBRE_PROYECTO}
MOVER logs ${NOMBRE_PROYECTO}
MOVER fuentes ${NOMBRE_PROYECTO}
# Hacemos push
[ "${NO_ENVIAR}" != 1 ] && ENVIAR
fi
# Nos devolvemos a la carpeta del desarrollador
cd ${DEV_DIR}
}

#------ AYUDANTES GIT --------------------------------------------------------------------------------------------------#
#=======================================================================================================================#

function DESCARGAR() {
#-------------------------------------------------------------#
# Nombre de la Función: DESCARGAR
# Propósito: Clonar un proyecto almacenado en un repositorio
#            git remoto.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core, grep, wget
#-------------------------------------------------------------#

# No especificaste un proyecto
[ -z "${proyecto}" ] && ERROR "No especificaste un proyecto." && exit 1
# Acceder a la carpeta del desarrollador
cd ${DEV_DIR}
# Si la dirección está en formato SSH, hacer la descarga normalmente
if [ $( echo ${proyecto} | grep -c "[@:]") != 0 ]; then
nombre=${proyecto#"git@gitorious.org/canaima-gnu-linux/"}
nombre=${proyecto#"git://gitorious.org/canaima-gnu-linux/"}
nombre=${nombre%".git"}
git clone ${proyecto}
# Constatar el resultado de la clonación
[ -e "${DEV_DIR}${nombre}" ] && EXITO "¡${nombre} Descargado!"
[ ! -e "${DEV_DIR}${nombre}" ] && ERROR "Ooops...! Algo falló con ${nombre}"
# Si el parámetro de descarga no es una dirección, sino el nombre del paquete
# y el repositorio remoto es gitorious.org ...
elif [ $( echo ${proyecto} | grep -c "[@:]" ) == 0 ] && [ "${REPO}" == "gitorious.org" ]; then
ADVERTENCIA "Verificando existencia de ${proyecto} en ${REPO} ..."
# Obtenemos el index HTML de gitorious ...
wget "http://gitorious.org/canaima-gnu-linux" > /dev/null 2>&1
# Extraemos los datos interesantes ...
FUENTE=$( cat "canaima-gnu-linux" | grep "git clone git://gitorious.org/canaima-gnu-linux/" | awk '{print $3}' )
# Y comprobamos si el paquete está disponible para descarga
if [ $( echo ${FUENTE} | grep -wc "git://gitorious.org/canaima-gnu-linux/${proyecto}.git" ) != 0 ]; then
descarga="git://gitorious.org/canaima-gnu-linux/${proyecto}.git"
git clone ${descarga}
# Constatar el resultado de la clonación
[ -e "${DEV_DIR}${proyecto}" ] && EXITO "¡${proyecto} Descargado!"
[ ! -e "${DEV_DIR}${proyecto}" ] && ERROR "Ooops...! Algo falló con ${proyecto}"
else
ERROR "Tal proyecto \"${proyecto}\"no existe en ${REPO}."
fi
# Si el parámetro de descarga no es una dirección, sino el nombre del paquete
# y el repositorio remoto es diferente de gitorious.org, esa modalidad de descarga
# no está disponible.
elif [ $( echo ${proyecto} | grep -c "[@:]" ) == 0 ] && [ "${REPO}" != "gitorious.org" ]; then
ERROR "Esa modalidad de descarga no está disponible para ${REPO}"
fi
# Nos devolvemos a la carpeta del desarrollador
cd ${DEV_DIR}
}

function REGISTRAR() {
#-------------------------------------------------------------#
# Nombre de la Función: REGISTRAR
# Propósito: Hacer git commit en el directorio especificado
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core, grep, awk
#-------------------------------------------------------------#

# Comprobaciones varias
# No especificaste el directorio
[ -z "${directorio#${DEV_DIR}}" ] && ADVERTENCIA "No especificaste un directorio a empaquetar, asumiendo que es $( pwd )."
# Garanticemos que el directorio siempre tiene escrita la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# Tal vez te comiste el parámetro directoriorio o especificaste un directorio con espacios
[ $( echo "${directorio#${DEV_DIR}}" | grep -c " " ) != 0 ] && ERROR "Sospecho dos cosas: o te saltaste el nombre del directorio, o especificaste un directorio con espacios." && exit 1
# No especificaste un mensaje para el commit
[ -z "${mensaje}" ] && mensaje="auto" && ADVERTENCIA "Mensaje de commit vacío. Autogenerando."
# El directorio no existe
[ ! -e "${directorio}" ] && ERROR "¡EPA! La carpeta \"${directorio}\" no existe en el directorio del desarrollador (${DEV_DIR})." && exit 1
# El directorio no es un directorio
[ ! -d "${directorio}" ] && ERROR "¡\"${directorio}\" no es un directorio!" && exit 1
# El directorio contiene un proyecto git
[ -e "${directorio}/.git" ] && GIT_NONE=0
# El directorio no contiene un proyecto git
[ ! -e "${directorio}/.git" ] && ERROR "El directorio '${directorio}' no contiene un proyecto git." && GIT_NONE=1
if [ "${GIT_NONE}" == "0" ]; then
# Ingresar al directorio
cd ${directorio}
# Emitir la notificación
ADVERTENCIA "Verificando proyecto ${directorio_nombre} ..."
# Asegurando que existan las ramas necesarias
[ $( git branch -l | grep -wc "master" ) == 0 ] && ADVERTENCIA "No existe la rama upstream, creando ..." && git add . && git commit -a -m "Versión inicial para Canaima GNU/Linux"
[ $( git branch -l | grep -wc "upstream" ) == 0 ] && ADVERTENCIA "No existe la rama upstream, creando ..." && git branch upstream
[ $( git branch -l | grep -wc "* master" ) == 0 ] && ADVERTENCIA "No estás en la rama master. Te voy a pasar para allá." && git checkout master
# Agregando todos los cambios
git add .
# Verificando que haya algún cambio desde el último commit
NO_COMMIT=0
if [ $( git status | grep -c "nothing to commit (working directory clean)" ) == 1 ]; then
EXITO "No hay nada a que hacer commit"
NO_COMMIT=1
else
# Si el mensaje de commit está vacío, o está configurado en modo "auto"
if [ -z "${mensaje}" ] || [ "${mensaje}" == "auto" ]; then
commit_message=""
# Autogenerar el mensaje de commit
for archivos_modificados in $( git status -s | grep -w "[AM] " | awk '{print $2}' ); do
archivos_modificados=$( basename ${archivos_modificados} )
commit_message=${commit_message}"${archivos_modificados} "
done
# Ejecutar el commit
if [ $( git status --porcelain | grep -c "debian/changelog" ) == 1 ] && [ $( git status --porcelain | wc -l ) == 1 ]; then
git commit -a -q -m "Nueva versión" && EXITO "¡Nueva versión!"
else
git commit -a -q -m "[ canaima-desarrollador ] Los siguientes archivos han sido modificados/añadidos: ${commit_message}" && EXITO "¡Commit!"
fi
else
# Si un mensaje ha sido especificado, ejecutar el commit con ese mensaje
if [ $( git status --porcelain | grep -c "debian/changelog" ) == 1 ] && [ $( git status --porcelain | wc -l ) == 1 ]; then
git commit -a -q -m "Nueva versión" && EXITO "¡Nueva versión!"
else
git commit -a -q -m "${mensaje}" && EXITO "¡Commit!"
fi
fi
# Combinar los cambios de master a upstream
git checkout upstream
git merge master > /dev/null 2>&1
git checkout master
ADVERTENCIA "Haciendo merge master -> upstream"
fi
# Volver a la carpeta del desarrollador
cd ${DEV_DIR}
fi
}

function ENVIAR() {
#-------------------------------------------------------------#
# Nombre de la Función: ENVIAR
# Propósito: Hace git push de un proyecto en específico
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core, grep, wget
#-------------------------------------------------------------#

# Comprobaciones varias
# No especificaste el directorio
[ -z "${directorio#${DEV_DIR}}" ] && ADVERTENCIA "No especificaste un directorio a empaquetar, asumiendo que es $( pwd )."
# Garanticemos que el directorio siempre tiene escrita la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# El directorio no existe
[ ! -e "${directorio}" ] && ERROR "¡EPA! La carpeta \"${directorio}\" no existe en el directorio del desarrollador (${DEV_DIR})." && exit 1
# El directorio no es un directorio
[ ! -d "${directorio}" ] && ERROR "¡\"${directorio}\" no es un directorio!" && exit 1
# El directorio contiene un proyecto git
[ -e "${directorio}/.git" ] && GIT_NONE=0
# El directorio no contiene un proyecto git
[ ! -e "${directorio}/.git" ] && ERROR "El directorio '${directorio}' no contiene un proyecto git." && GIT_NONE=1
if [ "${GIT_NONE}" == "0" ]; then
# Accedemos al directorio
cd ${directorio}
# Emitimos la notificación
ADVERTENCIA "Haciendo push en el proyecto ${directorio_nombre} ..."
# Configuramos los repositorios
SET-REPOS
# Asegurando que existan las ramas necesarias
[ $( git branch -l | grep -wc "upstream" ) == 0 ] && ERROR "Al proyecto le falta la rama upstream, creando ..." && git branch upstream
[ $( git branch -l | grep -wc "master" ) == 0 ] && ERROR "Al proyecto le falta la rama master, creando ..." && git branch master
# Hacemos push
[ $( git branch -l | grep -wc "master" ) == 1 ] && git push origin master upstream --tags && EXITO "¡Proyecto enviado!"
# Volvemos a la carpeta del desarrollador
cd ${DEV_DIR}
fi
}

function ACTUALIZAR() {
#-------------------------------------------------------------#
# Nombre de la Función: ACTUALIZAR
# Propósito: Hace git pull en el proyecto especificado
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core, grep
#	- Funciones: SET-REPOS
#-------------------------------------------------------------#

# Comprobaciones varias
# No especificaste el directorio
[ -z "${directorio#${DEV_DIR}}" ] && ADVERTENCIA "No especificaste un directorio a empaquetar, asumiendo que es $( pwd )."
# Garanticemos que el directorio siempre tiene escrita la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
directorio_nombre=$( basename "${directorio}" )
# El directorio no existe
[ ! -e "${directorio}" ] && ERROR "¡EPA! La carpeta \"${directorio}\" no existe en el directorio del desarrollador (${DEV_DIR})." && exit 1
# El directorio no es un directorio
[ ! -d "${directorio}" ] && ERROR "¡\"${directorio}\" no es un directorio!" && exit 1
# El directorio contiene un proyecto git
[ -e "${directorio}/.git" ] && GIT_NONE=0
# El directorio no contiene un proyecto git
[ ! -e "${directorio}/.git" ] && ERROR "El directorio '${directorio}' no contiene un proyecto git." && GIT_NONE=1
if [ "${GIT_NONE}" == "0" ]; then
# Accedemos al directorio
cd ${directorio}
# Emitimos la notificación
ADVERTENCIA "Actualizando proyecto ${directorio_nombre} ..."
# Configuramos los repositorios
SET-REPOS
# Asegurando que existan las ramas necesarias
[ $( git branch -l | grep -wc "upstream" ) == 0 ] && ERROR "Al proyecto le falta la rama upstream, creando ..." && git branch upstream
[ $( git branch -l | grep -wc "master" ) == 0 ] && ERROR "Al proyecto le falta la rama master, creando ..." && git branch master
# Hacemos pull
[ $( git branch -l | grep -wc "master" ) == 1 ] && git pull origin master upstream
# Volvemos a la carpeta del desarrollador
cd ${DEV_DIR}
fi
}

#------ AYUDANTES MASIVOS ----------------------------------------------------------------------------------------#
#=======================================================================================================================#

function DESCARGAR-TODO() {
#-------------------------------------------------------------#
# Nombre de la Función: DESCARGAR-TODO
# Propósito: Clonar todos los proyectos existentes en el
#            repositorio oficial git.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core, grep, wget, awk
#-------------------------------------------------------------#

# Accedemos a la carpeta del desarrollador
cd ${DEV_DIR}
# Descargamos la página HTML del repositorio oficial de Canaima GNU/Linux
wget "http://gitorious.org/canaima-gnu-linux" > /dev/null 2>&1
# Extraemos una lista de los datos interesantes
FUENTE=$( cat "canaima-gnu-linux" | grep "git clone git://gitorious.org/canaima-gnu-linux/" | awk '{print $3}' )
# Para cada elemento en la lista ...
for proyecto in ${FUENTE}; do DESCARGAR; done
# Borramos la página HTML descargada inicialmente
rm canaima-gnu-linux
}

function REGISTRAR-TODO() {
#-------------------------------------------------------------#
# Nombre de la Función: REGISTRAR-TODO
# Propósito: Hacer git commit a todos los proyectos en la
#            carpeta del desarrollador.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Funciones: REGISTRAR
#-------------------------------------------------------------#

# Para cada directorio en la carpeta del desarrollador, ejecutar la función REGISTRAR
for directorio in $( ls -F ${DEV_DIR} | grep "/" );do REGISTRAR;done
}

function ENVIAR-TODO() {
#-------------------------------------------------------------#
# Nombre de la Función: ENVIAR-TODO
# Propósito: Hace git push en todos los proyectos contenidos
#            dentro de la carpeta del desarrollador.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Funciones: ENVIAR
#-------------------------------------------------------------#

# Para cada directorio en la carpeta del desarrollador... ejecutar la función ENVIAR
for directorio in $( ls -F ${DEV_DIR} | grep "/" );do ENVIAR;done
}

function ACTUALIZAR-TODO() {
#-------------------------------------------------------------#
# Nombre de la Función: ACTUALIZAR-TODO
# Propósito: Hace git pull a todos los proyectos en la carpeta
#            del desarrollador.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Funciones: ACTUALIZAR
#-------------------------------------------------------------#

# Para cada directorio en la carpeta del desarrollador... ejecutar la función ACTUALIZAR
for directorio in $( ls -F ${DEV_DIR} | grep "/" );do ACTUALIZAR;done
}

function EMPAQUETAR-VARIOS() {
#-------------------------------------------------------------#
# Nombre de la Función: EMPAQUETAR-VARIOS
# Propósito: Empaqueta varios proyectos
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Funciones: EMPAQUETAR
#-------------------------------------------------------------#

# Comprobaciones varias
# No especificaste el directorio
[ -z "${para_empaquetar}" ] && ERROR "No especificaste la lista de proyectos que querías empaquetar." && exit 1
# No especificaste número de procesadores
[ -z "${procesadores}" ] && procesadores=0 && ADVERTENCIA "No me dijiste si tenías más de un procesador. Asumiendo uno sólo."
# cálculo de los threads (n+1)
procesadores=$[ ${procesadores}+1 ]
# Para cada directorio especificado en ${PARA_EMPAQUETAR}... ejecutar la función EMPAQUETAR
for directorio in ${para_empaquetar};do EMPAQUETAR;done
}

function EMPAQUETAR-TODO() {
#-------------------------------------------------------------#
# Nombre de la Función: EMPAQUETAR-TODO
# Propósito: Empaquetar todos los proyectos en la carpeta del
#            desarrollador
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Funciones: EMPAQUETAR
#-------------------------------------------------------------#

# Para cada directorio en la carpeta del desarrollador... ejecutar la función EMPAQUETAR
for directorio in $( ls -F ${DEV_DIR} | grep "/" );do EMPAQUETAR;done
}

#------ AYUDANTES INFORMATIVOS -----------------------------------------------------------------------------------------#
#=======================================================================================================================#

function LISTAR-REMOTOS() {
#-------------------------------------------------------------#
# Nombre de la Función: LISTAR-REMOTOS
# Propósito: Lista los proyectos existentes en el repositorio
#            oficial git de Canaima GNU/Linux
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#	- Paquetes: grep, wget, awk
#-------------------------------------------------------------#

# Descargamos la página HTML del repositorio oficial de Canaima GNU/Linux
wget "http://gitorious.org/canaima-gnu-linux" > /dev/null 2>&1
# Extraemos una lista de los datos interesantes
FUENTE=$( cat "canaima-gnu-linux" | grep "git clone git://gitorious.org/canaima-gnu-linux/" | awk '{print $3}' )
# Vamos imprimiéndolos uno a uno
for descarga in ${FUENTE}; do
nombre=${descarga#"git://gitorious.org/canaima-gnu-linux/"}
nombre=${nombre%".git"}
echo -e "${VERDE}Nombre:${FIN} ${nombre} | ${VERDE}Fuente:${FIN} ${descarga}"
done
# Borramos la página HTML descargada inicialmente
rm canaima-gnu-linux
}

function LISTAR-LOCALES() {
#-------------------------------------------------------------#
# Nombre de la Función: LISTAR-LOCALES
# Propósito: Lista los proyectos existentes en la carpeta del
#            desarrollador, clasificándolos.
# Dependencias:
# 	- Requiere la carga del archivo ${CONF}
#-------------------------------------------------------------#

# Para cada directorio en la carpeta del desarrollador...
for directorio in $( ls -F ${DEV_DIR} | grep "/" ); do
# Asegurarse que contiene la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
# Obtener su nombre base
directorio_nombre=$( basename "${directorio}" )
# Imprimir si es un proyecto versionado (git), si contiene las reglas básicas de un paquete fuente (source),
# y si contiene las reglas básicas de un proyecto debian (debian)
if [ -e "${directorio}/.git" ] && [ -e "${directorio}/Makefile" ] && [ -e "${directorio}/debian/control" ]; then
echo -e "${VERDE}Nombre:${FIN} ${directorio_nombre} | ${VERDE}Tipo:${FIN} git, source, debian"
elif [ -e "${directorio}/.git" ] && [ -e "${directorio}/Makefile" ] && [ ! -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} git, source"
elif [ -e "${directorio}/.git" ] && [ ! -e "${directorio}/Makefile" ] && [ ! -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} git"
elif [ -e "${directorio}/.git" ] && [ ! -e "${directorio}/Makefile" ] && [ -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} git, debian"
elif [ ! -e "${directorio}/.git" ] && [ -e "${directorio}/Makefile" ] && [ -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} source, debian"
elif [ ! -e "${directorio}/.git" ] && [ ! -e "${directorio}/Makefile" ] && [ -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} debian"
elif [ ! -e "${directorio}/.git" ] && [ -e "${directorio}/Makefile" ] && [ ! -e "${directorio}/debian/control" ]; then
echo -e "${AMARILLO}Nombre:${FIN} ${directorio_nombre} | ${AMARILLO}Tipo:${FIN} source"
elif [ ! -e "${directorio}/.git" ] && [ ! -e "${directorio}/Makefile" ] && [ ! -e "${directorio}/debian/control" ]; then
echo -e "${ROJO}Nombre:${FIN} ${directorio_nombre} | ${ROJO}Tipo:${FIN} proyecto desconocido"
fi
done

}

#------ FUNCIONES COMPLEMENTARIAS --------------------------------------------------------------------------------#
#=======================================================================================================================#

function CHECK() {
#-------------------------------------------------------------#
# Nombre de la Función: CHECK
# Propósito: Comprobar que ciertos parámetros se cumplan al
#            inicio del script canaima-desarrollador.sh
# Dependencias:
#	- Requiere la carga del archivo ${VARIABLES} y ${CONF}
#	- Paquetes: findutils
#-------------------------------------------------------------#

# Faltan variables por definir en el archivo de configuración ${CONF}
if [ -z "${REPO}" ] || [ -z "${REPO_USER}" ] || [ -z "${REPO_DIR}" ] || [ -z "${DEV_DIR}" ] || [ -z "${DEV_NAME}" ] || [ -z "${DEV_MAIL}" ] || [ -z "${DEPOSITO_LOGS}" ] || [ -z "${DEPOSITO_SOURCES}" ] || [ -z "${DEPOSITO_DEBS}" ]; then
ERROR "Tu archivo de configuración ${CONF} presenta inconsistencias. Todas las variables deben estar llenas." && exit 1
fi
# La carpeta del desarrollador ${DEV_DIR} no existe
[ ! -d "${DEV_DIR}" ] && ERROR "¡La carpeta del desarrollador ${DEV_DIR} no existe!" && exit 1
# El archivo de configuración personal ${CONF} no existe
[ ! -e "${CONF}" ] && ERROR "¡Tu archivo de configuración ${CONF} no existe!" && exit 1
# Asegurando que existan las carpetas de depósito
[ ! -e ${DEPOSITO_LOGS} ] && mkdir -p ${DEPOSITO_LOGS}
[ ! -e ${DEPOSITO_SOURCES} ] && mkdir -p ${DEPOSITO_SOURCES}
[ ! -e ${DEPOSITO_DEBS} ] && mkdir -p ${DEPOSITO_DEBS}
# Asegurando que la carpeta del desarrollador y de las plantillas
# terminen con un slash (/) al final
ultimo_char_dev=${DEV_DIR#${DEV_DIR%?}}
ultimo_char_pla=${PLANTILLAS#${PLANTILLAS%?}}
ultimo_char_sou=${DEPOSITO_SOURCES#${DEPOSITO_SOURCES%?}}
ultimo_char_deb=${DEPOSITO_DEBS#${DEPOSITO_DEBS%?}}
ultimo_char_log=${DEPOSITO_LOGS#${DEPOSITO_LOGS%?}}
[ "${ultimo_char_dev}" != "/" ] && DEV_DIR="${DEV_DIR}/"
[ "${ultimo_char_pla}" != "/" ] && PLANTILLAS="${PLANTILLAS}/"
[ "${ultimo_char_sou}" != "/" ] && DEPOSITO_SOURCES="${DEPOSITO_SOURCES}/"
[ "${ultimo_char_deb}" != "/" ] && DEPOSITO_DEBS="${DEPOSITO_DEBS}/"
[ "${ultimo_char_log}" != "/" ] && DEPOSITO_LOGS="${DEPOSITO_LOGS}/"
# Verificando que no hayan carpetas con nombres que contengan espacios
if [ $( ls ${DEV_DIR} | grep -c " " ) != 0 ]; then
ERROR "${DEV_DIR} contiene directorios con espacios en su nombre. Abortando."
exit 1
else
echo "Iniciando Canaima Desarrollador ..."
fi
}

function DEV-DATA() {
#-------------------------------------------------------------#
# Nombre de la Función: DEV-DATA
# Propósito: Establecer el nombre y correo del desarrollador
#            tanto para versionamiento como empaquetamiento.
# Dependencias:
#	- Requiere la carga del archivo ${CONF}
#	- Paquetes: git-core
#-------------------------------------------------------------#

# Configurando git para que use los datos del desarrollador
git config --global user.name "${DEV_NAME}"
git config --global user.email "${DEV_MAIL}"
# Estableciendo las variables de entorno que utilizan los métodos de
# empaquetamiento.
export DEBFULLNAME="${DEV_NAME}"
export DEBEMAIL="${DEV_MAIL}"
}

function DATOS-PROYECTO() {
#-------------------------------------------------------------#
# Nombre de la Función: DATOS-PROYECTO
# Propósito: Determinar algunos datos del proyecto
# Dependencias:
#	- Requiere la carga del archivo ${VARIABLES}
# 	- Paquetes: grep, awk, dpkg-dev
#-------------------------------------------------------------#

# Ubicación del changelog dentro del proyecto
CHANGELOG_PROYECTO="${directorio}/debian/changelog"
# Si existe, entonces:
if [ -e "${CHANGELOG_PROYECTO}" ]; then
# Usemos dpkg-parsechangelog para que nos diga el nombre y versión del proyecto
VERSION_PROYECTO=$( dpkg-parsechangelog -l${CHANGELOG_PROYECTO} | grep "Version: " | awk '{print $2}' )
NOMBRE_PROYECTO=$( dpkg-parsechangelog -l${CHANGELOG_PROYECTO} | grep "Source: " | awk '{print $2}' )
PAQUETE=1
else
# De lo contrario, advertir que no es un proyecto de empaquetamiento debian
ERROR "${directorio_nombre} no contiene ningún proyecto de empaquetamiento." && PAQUETE=0
fi
}

function SET-REPOS() {
#-------------------------------------------------------------#
# Nombre de la Función: SET-REPOS
# Propósito: Establecer correctamente el repositorio remoto
# Dependencias:
#	- Requiere la carga del archivo ${VARIABLES} y ${CONF}
#	- Se debe ejecutar dentro del proyecto
#	- git-core
#-------------------------------------------------------------#

# Determinar los datos del proyecto
DATOS-PROYECTO
# Si es un proyecto de empaquetamiento válido, entonces ...
if [ "${PAQUETE}" == "1" ]; then
# Determinando la dirección SSH para cada servidor remoto posible
# Por ahora spolo diferenciamos entre gitorious.org y cualquier otro
case ${REPO} in
"gitorious.org") repo_completo="${REPO_USER}@${REPO}:${REPO_DIR}/${NOMBRE_PROYECTO}.git" ;;
*) repo_completo="${REPO_USER}@${REPO}:${REPO_DIR}/${NOMBRE_PROYECTO}/.git" ;;
esac
# Si existe una dirección remota llamada "origin", y su contenido no es el correcto ...
if [ $( git remote | grep -wc "origin" ) == 1 ] && [ $( git remote show origin | grep -c "${repo_completo}" ) == 0 ]; then
# Si ya existe un adirección "origin_viejo", bórrala
[ $( git remote | grep -wc "origin_viejo" ) == 1 ] && git remote rm origin_viejo
# Renombra el "origin" incorrecto a "origin_viejo"
git remote rename origin origin_viejo
fi
# Si "origin" no existe, entonces agrega el correcto
[ $( git remote | grep -wc "origin" ) == 0 ] && git remote add origin ${repo_completo} && ADVERTENCIA "Definiendo \"${repo_completo}\" como repositorio git \"origin\""
echo "Repositorios establecidos"
fi
}

function GIT-DCH() {
#-------------------------------------------------------------#
# Nombre de la Función: GIT-DCH
# Propósito: Registrar los cambios en debian/changelog, usando
#            los mensajes de commit
# Dependencias:
#	- Requiere la carga del archivo ${VARIABLES} y ${CONF}
#	- Paquetes: git-buildpackage, dpkg-dev
#-------------------------------------------------------------#

# Determinar los datos del proyecto
DATOS-PROYECTO
# Si es un proyecto de empaquetamiento válido, entonces ...
if [ "${PAQUETE}" == "1" ]; then
# Accedemos al directorio
cd ${directorio}
ADVERTENCIA "Registrando cambios en debian/changelog ..."
# Determinamos la versión del proyecto antes de hacer git-dch
ANTES_DCH=$( dpkg-parsechangelog | grep "Version: " | awk '{print $2}' )
# Establecemos el editor como "true" para que no nos lleve al editor
# cuando le digamos git-dch
export EDITOR=true
# Ejecutamos git-dch y mandamos su salida a /dev/null
git-dch --release --auto --id-length=7 --full > /dev/null 2>&1
# Reestablecemos el valor anterior de la variable ${EDITOR}
export EDITOR=""
# Determinamos la versión del proyecto después de hacer git-dch
DESPUES_DCH=$( dpkg-parsechangelog | grep "Version: " | awk '{print $2}' )

# Si la versión cambió después de hacer git-dch ...
if [ "${DESPUES_DCH}" != "${ANTES_DCH}" ]; then
directorio="${DEV_DIR}${NOMBRE_PROYECTO}-${DESPUES_DCH}"
# Asegurarse que contiene la ruta completa
directorio=${DEV_DIR}${directorio#${DEV_DIR}}
# Obtener su nombre base
directorio_nombre=$( basename "${directorio}" )
ADVERTENCIA "Nueva versión ${DESPUES_DCH}"
# Si git-dch no cambió el directorio de nombre, luego del cambio de versión, hagámoslo por él
[ $( ls ${DEV_DIR} | grep -wc "${NOMBRE_PROYECTO}-${DESPUES_DCH}" ) == 0  ] && mv $( pwd ) "${DEV_DIR}${NOMBRE_PROYECTO}-${DESPUES_DCH}" && echo "git-dch no puso el nombre correcto al directorio. Lo voy a hacer."
# Si ya tenemos el nombre correcto, entonces hay que cambiarse para allá
[ $( ls ${DEV_DIR} | grep -wc "${NOMBRE_PROYECTO}-${DESPUES_DCH}" ) == 1  ] && [ $( pwd ) != "${DEV_DIR}${NOMBRE_PROYECTO}-${DESPUES_DCH}" ] && cd "${DEV_DIR}${NOMBRE_PROYECTO}-${DESPUES_DCH}" && echo "Cambiando directorio a ${NOMBRE_PROYECTO}-${DESPUES_DCH}"
else
ADVERTENCIA "Misma versión ${DESPUES_DCH}"
fi
# Nos devolvemos a la carpeta del desarrollador
cd ${DEV_DIR}
fi
}

function MOVER() {
#-------------------------------------------------------------#
# Nombre de la Función: MOVER
# Propósito: Mover archivos a su depósito correspondiente
# Dependencias:
#       - Requiere la carga del archivo ${CONF}
#-------------------------------------------------------------#
MOVER_ARCHIVOS=${2}
case ${1} in
# Mover .debs
debs)
if [ $( ls ${DEV_DIR}*.deb 2>/dev/null | wc -l ) != 0 ]; then
mv ${DEV_DIR}*.deb ${DEPOSITO_DEBS}
EXITO "Paquetes Binarios .deb movidos a ${DEPOSITO_DEBS}"
else
ERROR "Ningún paquete .deb para mover"
fi
;;

# Mover .diff .changes .dsc .tar.gz
fuentes)
[ $( ls ${DEV_DIR}${MOVER_ARCHIVOS}_*.tar.gz 2>/dev/null | wc -l ) != 0 ] && mv ${DEV_DIR}${MOVER_ARCHIVOS}_*.tar.gz ${DEPOSITO_SOURCES}
[ $( ls ${DEV_DIR}${MOVER_ARCHIVOS}_*.diff.gz 2>/dev/null | wc -l ) != 0 ] && mv ${DEV_DIR}${MOVER_ARCHIVOS}_*.diff.gz ${DEPOSITO_SOURCES}
[ $( ls ${DEV_DIR}${MOVER_ARCHIVOS}_*.changes 2>/dev/null | wc -l ) != 0 ] && mv ${DEV_DIR}${MOVER_ARCHIVOS}_*.changes ${DEPOSITO_SOURCES}
[ $( ls ${DEV_DIR}${MOVER_ARCHIVOS}_*.dsc 2>/dev/null | wc -l ) != 0 ] && mv ${DEV_DIR}${MOVER_ARCHIVOS}_*.dsc ${DEPOSITO_SOURCES}
EXITO "Fuentes *.tar.gz *.diff.gz *.changes *.dsc movidas a ${DEPOSITO_SOURCES}"
;;

# Mover .build
logs)
if [ $( ls ${DEV_DIR}${MOVER_ARCHIVOS}_*.build 2>/dev/null | wc -l ) != 0 ]; then
mv ${DEV_DIR}${MOVER_ARCHIVOS}_*.build ${DEPOSITO_LOGS}
EXITO "Logs .build movidos a ${DEPOSITO_LOGS}"
else
ERROR "Ningún log .build para mover"
fi
;;
esac
}

function ERROR() {
echo -e ${ROJO}${1}${FIN}
}

function ADVERTENCIA() {
echo -e ${AMARILLO}${1}${FIN}
}

function EXITO() {
echo -e ${VERDE}${1}${FIN}
}

