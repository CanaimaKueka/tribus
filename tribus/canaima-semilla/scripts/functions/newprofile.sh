#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/newprofile.sh
# DESCRIPCIÓN: Plantilla que contiene todas las preguntas realizadas por el
#              asistente para la creación de nuevos perfiles.
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

if [ "1" = "0" ]; then
INFOMSG "Nombre del perfil"
# WHERE
# PROFILE_NAME="@@PROFILE_NAME@@"

INFOMSG "Arquitecturas habilitadas para la construcción de la distribución [ej: i386 amd64]"
# WHERE
# PROFILE_ARCH="@@PROFILE_ARCH@@"

INFOMSG "Nombre de la persona o grupo responsable del mantenimiento de la distribución derivada"
# WHERE
# AUTHOR_NAME="@@AUTHOR_NAME@@"

INFOMSG "Correo de la persona o grupo responsable"
# WHERE
# AUTHOR_EMAIL="@@AUTHOR_EMAIL@@"

INFOMSG "Página web de la persona o grupo responsable"
# WHERE
# AUTHOR_URL="@@AUTHOR_URL@@"

INFOMSG "Metadistribución base para la distribución derivada [ej: debian]"
# WHERE
# META_DIST="@@META_DIST@@"

INFOMSG "Código nombre de la Metadistribución base [ej: squeeze]"
# WHERE
# META_CODENAME="@@META_CODENAME@@"

INFOMSG "Repositorio para la Metadistribución base [ej: http://http.us.debian.org/debian]"
# WHERE
# META_REPO="@@META_REPO@@"

INFOMSG "Secciones del repositorio para la Metadistribución base [ej: main contrib]"
# WHERE
# META_REPOSECTIONS="@@META_REPOSECTIONS@@"

INFOMSG "Código de lenguage para la distribución derivada [ej: es_VE.UTF-8]"
# WHERE
# OS_LOCALE="@@OS_LOCALE@@"

INFOMSG "Paquetes que conformarán la distribución derivada [ej: gnome-core libreoffice]"
# WHERE
# OS_PACKAGES="@@OS_PACKAGES@@"

INFOMSG "[OPCIONAL] Archivo que contiene todos los repositorios adicionales [ej: /home/usuario/repos.list]"
# WHERE FILE ${PROFILES}/${PROFILE_NAME}/extra-repos.list
# OS_EXTRAREPOS="@@OS_EXTRAREPOS@@"

INFOMSG "[OPCIONAL] Carpeta que contiene los archivos que se incluirán en el Sistema Operativo [ej: /home/usuario/inclusiones/]"
# WHERE FOLDER ${PROFILES}/${PROFILE_NAME}/OS_INCLUDES/
# OS_INCLUDES="@@OS_INCLUDES@@"

INFOMSG "[OPCIONAL] Carpeta que contiene los scripts que se ejecutarán durante la construcción del Sistema Operativo [ej: /home/usuario/inclusiones/]"
# WHERE FOLDER ${PROFILES}/${PROFILE_NAME}/OS_HOOKS/
# OS_HOOKS="@@OS_HOOKS@@"

INFOMSG "[OPCIONAL] Imagen que se utilizará para el arranque del modo live [ej: /home/usuario/syslinux.png]"
# WHERE FILE ${PROFILES}/${PROFILE_NAME}/syslinux.png
# IMG_SYSLINUX_SPLASH="@@IMG_SYSLINUX_SPLASH@@"

INFOMSG "[OPCIONAL] Paquetes que se incluirán en el repositorio interno de la imagen [ej: grub grub-pc]"
# WHERE
# IMG_POOL_PACKAGES="@@IMG_POOL_PACKAGES@@"

INFOMSG "[OPCIONAL] Carpeta que contiene los archivos que se incluirán en la imagen [ej: /home/usuario/inclusiones/]"
# WHERE FOLDER ${PROFILES}/${PROFILE_NAME}/IMG_INCLUDES/
# IMG_INCLUDES="@@IMG_INCLUDES@@"

INFOMSG "[OPCIONAL] Carpeta que contiene los scripts que se ejecutarán durante la construcción de la imagen [ej: /home/usuario/inclusiones/]"
# WHERE FOLDER ${PROFILES}/${PROFILE_NAME}/IMG_HOOKS/
# IMG_HOOKS="@@IMG_HOOKS@@"

INFOMSG "[OPCIONAL] ¿Desea incluir el Instalador Debian? true/false"
# WHERE
# IMG_DEBIAN_INSTALLER="@@IMG_DEBIAN_INSTALLER@@"

INFOMSG "[OPCIONAL] Imagen de banner para el Instalador Debian [ej: /home/usuario/banner.png]"
# WHERE FILE ${PROFILES}/${PROFILE_NAME}/DEBIAN_INSTALLER/banner.png
# IMG_DEBIAN_INSTALLER_BANNER="@@IMG_DEBIAN_INSTALLER_BANNER@@"

INFOMSG "[OPCIONAL] Archivo de preconfiguración para el Instalador Debian [ej: /home/usuario/preseed.cfg]"
# WHERE FILE ${PROFILES}/${PROFILE_NAME}/DEBIAN_INSTALLER/preseed.cfg
# IMG_DEBIAN_INSTALLER_PRESEED="@@IMG_DEBIAN_INSTALLER_PRESEED@@"

INFOMSG "[OPCIONAL] Archivo de temas GTK para el Instalador Debian [ej: /home/usuario/gtkrc]"
# WHERE FILE ${PROFILES}/${PROFILE_NAME}/DEBIAN_INSTALLER/gtkrc
# IMG_DEBIAN_INSTALLER_GTK="@@IMG_DEBIAN_INSTALLER_GTK@@"
fi
