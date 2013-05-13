#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s-core.sh [MÓDULO] [PARÁMETROS] [...]
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

from gettext import gettext as _

# canaimasemilla.main.Main() strings
MAIN_TITLE = _('Generador de Distribuciones Derivadas')
MAIN_CREATE_PROFILE_TITLE = _('Crear perfil')
MAIN_BUILD_IMAGE_TITLE = _('Construir imagen')
MAIN_TEST_IMAGE_TITLE = _('Probar imagen')
MAIN_SAVE_IMAGE_TITLE = _('Grabar imagen')
MAIN_CREATE_PROFILE_TEXT = _('Inicia un asistente que permite construir un perfil para una nueva distribución derivada.')
MAIN_BUILD_IMAGE_TEXT = _('Crea una imagen de un Sistema Operativo construido en base a un perfil.')
MAIN_TEST_IMAGE_TEXT = _('Inicia un emulador que permite ejecutar el Sistema Operativo contenido en una imagen.')
MAIN_SAVE_IMAGE_TEXT = _('Inicia un asistente que permite grabar una imagen en un dispositivo de almacenamiento.')
MAIN_ROOT_ERROR_MSG = _('Canaima Semilla debe ser ejecutado con permisos de superusuario.')
MAIN_ROOT_ERROR_TITLE = _('Error de permisología')

# canaimasemilla.main.Build() strings
BUILD_TITLE = _('Canaima Semilla: Módulo de Construcción de Imágenes')
BUILD_PROFILE_MEDIA_1 = _('Seleccione el formato de archivo de la imagen:')
BUILD_PROFILE_MEDIA_2 = _('El formato que elija determinará el tipo de dispositivo en donde podrá grabar la imagen una vez construída.')
BUILD_PROFILE_MEDIA_ISO = _('Imagen para dispositivos ópticos de almacenamiento (CD/DVD).')
BUILD_PROFILE_MEDIA_IMG = _('Imagen para dispositivos de almacenamiento extraíble (USB).')
BUILD_PROFILE_MEDIA_HYBRID = _('Imagen mixta para dispositivos variados (CD/DVD/USB) [Recomendado].')
BUILD_PROFILE_ARCH_1 = _('Seleccione el tipo de arquitectura de la imagen:')
BUILD_PROFILE_ARCH_2 = _('Tenga en cuenta que algunas arquitecturas funcionan en ciertos tipos de computadores y otras no funcionan.')
BUILD_PROFILE_ARCH_AMD64 = _('Arquitectura de procesadores con soporte para 64 bits.')
BUILD_PROFILE_ARCH_I386 = _('Arquitectura de procesadores con soporte para 32 bits [Recomendado].')
BUILD_PROFILE_NAME_1 = _('Seleccione el perfil del sistema operativo a incluir en la imagen:')
BUILD_PROFILE_NAME_2 = _('Puede seleccionar un perfil existente o crear uno nuevo a través del menú de entrada.')
BUILD_CONFIRM_CANCEL_TITLE = _('Creación de imagen')
BUILD_CONFIRM_CANCEL_MSG = _('¿Está seguro que desea cancelar la creación de la imagen?{0}Presione aceptar para interrumpir la creación de la imagen o cancelar para continuar con el proceso.')
BUILD_CONFIRM_OK_TITLE = _('Creación de imagen')
BUILD_CONFIRM_OK_MSG = _('Todo está preparado para comenzar a construir la imagen.{0}Presione aceptar para continuar o cancelar para volver a la pantalla anterior.')
BUILD_WINDOW_TITLE = _('Creación de imagen')
BUILD_VALIDATE_SOURCES_MSG = _('Validando sección "{0}" de la rama "{1}"{2}para el repositorio "{3}" ({4})')
BUILD_VALIDATE_SOURCES_ERROR_TITLE = _('Error validando repositorios')
BUILD_VALIDATE_SOURCES_ERROR_MSG = _('Ha ocurrido un error mientras se intentaba comprobar la existencia de los repositorios especificados.{0}Por favor verifica que estás conectado a internet o que la ruta es la correcta.')
BUILD_SUCCESSFUL_TITLE = _('Completado')
BUILD_SUCCESSFUL_MSG = _('¡Felicidades! La generación de la imagen se ha completado satisfactoriamente.')
BUILD_FAILED_TITLE = _('Se ha interrumpido la construcción')
BUILD_FAILED_MSG = _('Ha ocurrido un error mientras se realizaba la construcción de la imagen.')
BUILD_PROCESS_STATUS = _('Construyendo imagen ...')

# canaimasemilla.main.Profile() strings
PROFILE_TITLE = _('Canaima Semilla: Módulo de Creación de Perfiles')
PROFILE_ID_TAB = _('Identificación')
PROFILE_DISTRO_TAB = _('Distribución')
PROFILE_PACKAGES_TAB = _('Paquetes')
PROFILE_INSTALLER_TAB = _('Instalador')
PROFILE_EXTRAREPOS_TAB = _('Repositorios')
PROFILE_INCLUDES_TAB = _('Inclusiones')
PROFILE_MISC_TAB = _('Varios')
PROFILE_PROFILE_NAME_1 = _('Introduzca el nombre del sabor a crear:')
PROFILE_PROFILE_NAME_2 = _('Debe introducir el nombre con el que desea identificar la distribución derivada que está creando, en minúsculas y sin espacios.')
PROFILE_PROFILE_ARCH_1 = _('Seleccione las arquitecturas habilitadas para el sabor:')
PROFILE_PROFILE_ARCH_2 = _('Estas serán las arquitecturas disponibles para la construcción de imágenes basadas en el perfil de este nuevo sabor. Las arquitecturas que seleccione serán utilizadas para validar paquetes y repositorios.')
PROFILE_AUTHOR_NAME_1 = _('Introduzca el nombre de la persona o grupo responsable:')
PROFILE_AUTHOR_NAME_2 = _('Debe introducir el nombre de la persona o grupo responsable de la creación y mantenimiento del sabor.')
PROFILE_AUTHOR_EMAIL_1 = _('Introduzca el correo electrónico de la persona o grupo responsable:')
PROFILE_AUTHOR_EMAIL_2 = _('Debe introducir un correo electrónico válido para contacto de la persona o grupo responsable de la creación y mantenimiento del sabor.')
PROFILE_AUTHOR_URL_1 = _('Introduzca una dirección web para la persona o grupo responsable:')
PROFILE_AUTHOR_URL_2 = _('Puede introducir una dirección web de referencia para mayor información acerca del sabor.')
PROFILE_META_DIST_1 = _('Seleccione la Metadistribución base de sabor:')
PROFILE_META_DIST_2 = _('Seleccione la Metadistribución que será la base del sabor en construcción.')
PROFILE_META_CODENAME_1 = _('Seleccione el nombre código de la Metadistribución:')
PROFILE_META_CODENAME_2 = _('Seleccione la Metadistribución que será la base del sabor en construcción.')
PROFILE_META_REPO_1 = _('Introduzca el espejo del repositorio a utilizar:')
PROFILE_META_REPO_2 = _('Puede utilizar el espejo del repositorio de la Metadistribución que más le convenga. Se recomienda la utilización de un espejo local para mayor rapidez. Si no está seguro, deje el valor por defecto.')
PROFILE_META_REPOSECTIONS_1 = _('Seleccione las secciones que estarán disponibles:')
PROFILE_META_REPOSECTIONS_2 = _('Cada Metadistribución tiene secciones del repositorio particulares. Seleccione segun su conveniencia.')
PROFILE_OS_LOCALE_1 = _('Seleccione el idioma predeterminado del Sistema Operativo:')
PROFILE_OS_LOCALE_2 = _('Debe seleccionar de la lista el idioma que vendrá configurado en la imagen resultante.')
PROFILE_OS_PACKAGES_1 = _('Introduzca los paquetes que conformarán el Sistema Operativo:')
PROFILE_OS_PACKAGES_2 = _('Los paquetes que se listen acá deben estar presentes en el espejo de la Metadistribución seleccionada o en los repositorios adicionales. Deben incluirse los componentes escenciales de un Sistema Operativo para poder generar una imagen funcional.')
PROFILE_OS_PACKAGES_ENTRY = _('Paquetes (separados por espacios)')
PROFILE_OS_PACKAGES_VALIDATE_TITLE = _('Validación de paquetes')
PROFILE_OS_PACKAGES_VALIDATE_MSG = _('Validando sección "{0}" de la rama "{1}"{2}para el repositorio "{3}" ({4})')
PROFILE_OS_PACKAGES_VALIDATE_PKG_TITLE = _('Validación de paquetes')
PROFILE_OS_PACKAGES_VALIDATE_PKG_MSG = _('Validando presencia del paquete "{0}" dentro{1}del repositorio principal y repositorios adicionales ...')
PROFILE_OS_PACKAGES_VALIDATE_PKG_ERROR_TITLE = _('Error en la validación de paquetes')
PROFILE_OS_PACKAGES_VALIDATE_PKG_ERROR_MSG = _('No se ha encontrado el paquete "{0}" dentro de los repositorios provistos.')
PROFILE_OS_PACKAGES_VALIDATE_ARCH_ERROR_MSG = _('El soporte para arquitectura i386 y/o amd64 se encuentra vacío.{0}Debes seleccionar las arquitecturas soportadas para poder realizar la validación de los repositorios y paquetes que se incluirán dentro de la imagen instalable.')
PROFILE_OS_PACKAGES_VALIDATE_ARCH_ERROR_TITLE = _('Arquitecturas soportadas no encontradas')
PROFILE_OS_PACKAGES_VALIDATE_REPO_ERROR_MSG = _('{0}{1}Ha ocurrido un error mientras se intentaba comprobar la existencia de los repositorios especificados.{2}Por favor verifica que estás conectado a internet o que los datos proporcionados son correctos.')
PROFILE_OS_PACKAGES_VALIDATE_REPO_ERROR_TITLE = _('Repositorio inexistente o inconsistente')
PROFILE_OS_EXTRAREPOS_2 = _('Los repositorios adicionales permiten agregar software no oficial o desarrollado localmente a la imagen en construcción. Introduzca la dirección web, la rama y las secciones (separadas por espacios) correspondientes al repositorio.')
PROFILE_OS_EXTRAREPOS_CHECK = _('Deseo incluir repositorios adicionales (opcional).')
PROFILE_OS_EXTRAREPOS_URL = _('Dirección URL')
PROFILE_OS_EXTRAREPOS_BRANCH = _('Rama')
PROFILE_OS_EXTRAREPOS_SECTIONS = _('Secciones')
PROFILE_OS_EXTRAREPOS_VALIDATE_TITLE = _('Validación de repositorios')
PROFILE_OS_EXTRAREPOS_VALIDATE_MSG = _('Validando sección "{0}" de la rama "{1}"{2}para el repositorio "{3}" ({4})')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_MSG = _('La dirección URL "{0}" es inválida.{1}Comprueba que has introducido correctamente los datos y vuelve a intentarlo.')
PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE = _('Direción no válida')
PROFILE_OS_EXTRAREPOS_VALIDATE_ARCH_ERROR_MSG = _('El soporte para arquitectura i386 y/o amd64 se encuentra vacío.{0}Debes seleccionar las arquitecturas soportadas para poder realizar la validación de los repositorios y paquetes que se incluirán dentro de la imagen instalable.')
PROFILE_OS_EXTRAREPOS_VALIDATE_ARCH_ERROR_TITLE = _('Arquitecturas soportadas no encontradas')
PROFILE_OS_EXTRAREPOS_VALIDATE_REPO_ERROR_MSG = _('{0}{1}Ha ocurrido un error mientras se intentaba comprobar la existencia de los repositorios especificados.{2}Por favor verifica que estás conectado a internet o que los datos proporcionados son correctos.')
PROFILE_OS_EXTRAREPOS_VALIDATE_REPO_ERROR_TITLE = _('Repositorio inexistente o inconsistente')
PROFILE_OS_INCLUDES_1 = _('Seleccione las inclusiones de Sistema Operativo (opcional):')
PROFILE_OS_INCLUDES_2 = _('Puede seleccionar una carpeta que contenga la estructura de directorios y archivos que desea incluir en el Sistema Operativo de la imagen. Debe incluir los directorios en el mismo orden jerárquico que quiere que aparezcan.')
PROFILE_OS_INCLUDES_ENTRY = ''
PROFILE_OS_INCLUDES_SELECT_TITLE = _('Seleccione una carpeta')
PROFILE_OS_HOOKS_1 = _('Seleccione los scripts o "ganchos" de Sistema Operativo (opcional):')
PROFILE_OS_HOOKS_2 = _('Puede seleccionar una carpeta que contenga scripts de shell (sh/bash) que necesite ejecutar durante la construcción del Sistema Operativo que va a ser incluído en la imagen.')
PROFILE_OS_HOOKS_ENTRY = ''
PROFILE_OS_HOOKS_SELECT_TITLE = _('Seleccione una carpeta')
PROFILE_IMG_SYSLINUX_SPLASH_1 = _('Seleccione la imagen de arranque o portada para la imagen (opcional):')
PROFILE_IMG_SYSLINUX_SPLASH_2 = _('Puede selecionar una imagen PNG de no más de 800 por 600 pixeles de tamaño para mostrar en el fondo del menú (syslinux) de presentación de la imagen.')
PROFILE_IMG_SYSLINUX_SPLASH_ENTRY = ''
PROFILE_IMG_SYSLINUX_SPLASH_SELECT_TITLE = _('Seleccione una imagen')
PROFILE_IMG_POOL_PACKAGES_1 = _('Introduzca los paquetes que se incluirán en el repositorio interno de la imagen (opcional):')
PROFILE_IMG_POOL_PACKAGES_2 = _('Los paquetes acá listados se incluirán en el repositorio interno de la imagen, con el propósito de que estén disponibles para otros procesos posteriores (como por ejemplo instaladores o configuradores).')
PROFILE_IMG_POOL_PACKAGES_ENTRY = _('Paquetes (separados por espacios)')
PROFILE_IMG_INCLUDES_1 = _('Seleccione las inclusiones de imagen (opcional):')
PROFILE_IMG_INCLUDES_2 = _('Puede seleccionar una carpeta que contenga la estructura de directorios y archivos que desea incluir directamente en la imagen. Debe incluir los directorios en el mismo orden jerárquico que quiere que aparezcan.')
PROFILE_IMG_INCLUDES_ENTRY = ''
PROFILE_IMG_INCLUDES_SELECT_TITLE = _('Seleccione una carpeta')
PROFILE_IMG_HOOKS_1 = _('Seleccione los scripts o "ganchos" de imagen (opcional):')
PROFILE_IMG_HOOKS_2 = _('Puede seleccionar una carpeta que contenga scripts de shell (sh/bash) que necesite ejecutar durante la generación de la imagen.')
PROFILE_IMG_HOOKS_ENTRY = ''
PROFILE_IMG_HOOKS_SELECT_TITLE = _('Seleccione una carpeta')
PROFILE_IMG_DEBIAN_INSTALLER_CHECK = _('Deseo incluir el instalador Debian (opcional).')
PROFILE_IMG_DEBIAN_INSTALLER_2 = _('Al incluir el instalador Debian en la imagen, se agregará una opción de instalación en el menú de presentación de la imagen que permitirá instalar a través del debian-installer.')
PROFILE_IMG_DEBIAN_INSTALLER_BANNER_1 = _('Seleccione el banner para el instalador Debian (800x75px, PNG):')
PROFILE_IMG_DEBIAN_INSTALLER_BANNER_ENTRY = ''
PROFILE_IMG_DEBIAN_INSTALLER_BANNER_SELECT_TITLE = _('Seleccione una imagen')
PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_1 = _('Seleccione el archivo de presembrado (preseed) para el instalador Debian:')
PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_ENTRY = ''
PROFILE_IMG_DEBIAN_INSTALLER_PRESEED_SELECT_TITLE = _('Seleccione un archivo')
PROFILE_IMG_DEBIAN_INSTALLER_GTK_1 = _('Seleccione el archivo de temas GTK (gtkrc) para el instalador Debian:')
PROFILE_IMG_DEBIAN_INSTALLER_GTK_ENTRY = ''
PROFILE_IMG_DEBIAN_INSTALLER_GTK_SELECT_TITLE = _('Seleccione un archivo')
PROFILE_CONFIRM_CANCEL_TITLE = _('Creación de perfil')
PROFILE_CONFIRM_CANCEL_MSG = _('¿Está seguro que desea cancelar la creación del perfil?{0}Presione aceptar para interrumpir la creación del perfil o cancelar para continuar con el proceso.')
PROFILE_CONFIRM_OK_TITLE = _('Creación de perfil')
PROFILE_CONFIRM_OK_MSG = _('Todo está preparado para crear el nuevo perfil.{0}Presione aceptar para continuar o cancelar para volver a la pantalla anterior.')
PROFILE_MIMETYPE_ALL_NAME = _('Todos los archivos')
PROFILE_MIMETYPE_FOLDER_NAME = _('Carpetas')
PROFILE_MIMETYPE_PNG_NAME = _('Archivo de imagen PNG')
PROFILE_CREATING_UNKNOWN_ERROR_TITLE = _('Error desconocido')
PROFILE_CREATING_UNKNOWN_ERROR_MSG = _('Ha ocurrido un error desconocido durante la copia de los archivos al nuevo perfil. Por favor revisa los datos introducidos y vuelve a intentarlo.')
PROFILE_CREATING_EXISTS_ERROR_TITLE = _('El perfil ya existe')
PROFILE_CREATING_EXISTS_ERROR_MSG = _('El nombre de perfil seleccionado ya se encuentra en uso. Por favor selecciona otro y vuelve a intentarlo.')
PROFILE_CREATING_SUCCESS_TITLE = _('Perfil creado')
PROFILE_CREATING_SUCCESS_MSG = _('¡Felicidades! Su perfil ha sido creado.')

# canaimasemilla.main.Test() strings
TEST_TITLE = _('Canaima Semilla: Módulo de Emulación de Imágenes')
TEST_IMAGE_1 = _('Seleccione la imagen que desea probar:')
TEST_IMAGE_2 = _('Puede seleccionar cualquier imagen que contenga un sistema operativo instalable.')
TEST_IMAGE_ENTRY = ''
TEST_IMAGE_SELECT_TITLE = _('Seleccion una imagen ISO')
TEST_MIMETYPE_ALL_NAME = _('Todos los archivos')
TEST_MIMETYPE_ISO_NAME = _('Imágenes ISO')
TEST_MEMORY_1 = _('Indique la cantidad de memoria RAM (MB) que desea asignar:')
TEST_MEMORY_2 = _('Puede indicar la memoria en un rango comprendido entre la mínima necesaria y el máximo disponible en su computador.')
TEST_PROCESSORS_1 = _('Indique la cantidad de procesadores que desea asignar:')
TEST_PROCESSORS_2 = _('Puede indicar la cantidad de procesadores asignados a este proceso, según la disponibilidad de su computador.')
TEST_START_1 = _('Indique desde donde desea iniciar la prueba:')
TEST_START_2 = _('Puede iniciar desde la imagen para instalar o probar el modo "live" o desde el disco duro virtual para comprobar si el sistema operativo ha instalado correctamente.')
TEST_START_CD_LABEL = _('Iniciar desde la imagen seleccionada.')
TEST_START_HD_LABEL = _('Iniciar desde el disco duro virtual.')
TEST_DISK_CHECK_LABEL = _('Deseo formatear el disco duro virtual con el siguiente tamaño de disco (GB).')
TEST_CONFIRM_CANCEL_TITLE = _('Emulación de Imagen')
TEST_CONFIRM_CANCEL_MSG = _('¿Está seguro que desea cancelar la emulación de la imagen?{0}Presione aceptar para interrumpir la emulación de la imagen o cancelar para continuar con el proceso.')
TEST_CONFIRM_OK_TITLE = _('Emulación de Imagen')
TEST_CONFIRM_OK_MSG = _('Todo está preparado para comenzar la emulación de la imagen.{0}Presione aceptar para continuar o cancelar para volver a la pantalla anterior.')

# canaimasemilla.main.Save() strings
SAVE_TITLE = _('Canaima Semilla: Módulo de Grabación de Imágenes')
SAVE_DEVICE_1 = _('Seleccione o introduzca el dispositivo donde desea grabar la imagen:')
SAVE_DEVICE_2 = _('En la lista se muestran los dispositivos ópticos y usb que se encuentran aptos y disponibles en su equipo para la grabación de imágenes instalables.')
SAVE_IMAGE_1 = _('Seleccione el archivo de imagen que desea grabar:')
SAVE_IMAGE_2 = _('Puede escoger imágenes ISO o IMG que estén aptas para la grabación en dispositivos de almacenamiento. Si usted hizo una imagen con Canaima Semilla, puede seleccionarla por acá.')
SAVE_IMAGE_ENTRY = ''
SAVE_IMAGE_SELECT_TITLE = _('Seleccione una imagen instalable')
SAVE_MIMETYPE_ALL_NAME = _('Todos los archivos')
SAVE_MIMETYPE_ISO_NAME = _('Imágenes ISO')
SAVE_CONFIRM_CANCEL_TITLE = _('Grabación de Imagen')
SAVE_CONFIRM_CANCEL_MSG = _('¿Está seguro que desea cancelar la grabación de la imagen?{0}Presione aceptar para interrumpir la grabación de la imagen o cancelar para continuar con el proceso.')
SAVE_CONFIRM_OK_TITLE = _('Grabación de Imagen')
SAVE_CONFIRM_OK_MSG = _('Todo está preparado para la grabación de la imagen.{0}Presione aceptar para continuar o cancelar para volver a la pantalla anterior.')
SAVE_WRITE_TITLE = _('Grabando')
SAVE_WRITE_MSG = _('Estamos grabando su imagen, espere un momento ...')
SAVE_FAILED_TITLE = _('Error de grabación')
SAVE_FAILED_MSG = _('Ha ocurrido un error desconocido durante la grabación de la imagen en el dispositivo seleccionado. Por favor revisa los datos introducidos y vuelve a intentarlo.')
SAVE_SUCCESSFUL_TITLE = _('Grabación exitosa')
SAVE_SUCCESSFUL_MSG = _('¡Felicidades! Su imagen ha sido grabada exitosamente.')
