# Makefile
# El Makefile es una hoja de instruciones para ejecutar el programa GNU MAKE.
# A través de MAKE, es posible compilar, instalar, desinstalar, comprobar y limpiar
# el software que estamos distribuyendo. También es usado por debian/rules para
# construir el paquete (si se le especifica).
# Hay que tener claro dos cosas. Existen dos visiones en el desarrollo de software
# para Canaima GNU/Linux: la del desarrollador del software y la del mantenedor del
# paquete. La visión del desarrollador tiene un ámbito íntimamente relacionado con
# el Makefile: es a través de él que el desarrollador proporciona una herramienta
# al usuario para interactuar con su software (compilarlo, instalarlo, etc.). El
# desarrollador diseña su programa de forma genérica, para funcionar en un sistema
# GNU/Linux que soporte lenguajes conocidos (bash, C, C++, Python, Perl, entre otros);
# no se preocupa por las reglas ni particularidades de determinada Distribución
# GNU/Linux (Debian, Fedora, Gentoo, etc.). La visión del Mantenedor del paquete está
# enfocada a determinar cómo hacer funcionar el software del desarrollador en una
# determinada Distribución GNU/Linux, con sus reglas y particularidades. Para ello se
# vale de "los scripts del mantenedor" (preinst, postinst, prerm, postrm, rules), de
# los scripts de "control" (control, docs, conffiles, compat, etc.) y ocasionalmente
# (si la licencia y el autor lo permiten) puede modificar el código fuente del
# desarrollador para adaptarlo a sus necesidades.

SHELL := sh -e

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: build

test:

	# Aquí se realizan diversas pruebas para segurar que
	# todo lo que se realice con el Makefile salga bien
	# (compilación, instalación, desinstalación, entre otros)
	# Una práctica común es la de correr los scripts en modo
	# "de prueba" para comprobar que están bien escritos.

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "\n=================================================================================\nHECHO!\n\n"

build:

	# Aquí se realizan todos los procedimientos relativos a
	# generación de archivos que necesitan compilarse.
	# Por ejemplo, una conversión de imágenes PNG > JPG,
	# Debe ir aquí. La compilación de binarios C++, debe ir
	# aquí. Entre otros ejemplos. Todos los programas que
	# utilices acá, debes incluirlas como dependencias de
	# compilación en el campo "Build-Depends" del archivo
	# debian/control.
	# Si no hay nada que compilar (por ejemplo, si tu
	# programa está hecho en bash o PHP) puedes dejar éste
	# espacio en blanco.
	#
	# EJEMPLO:
	# convert ejemplo.png ejemplo.jpg

	@echo "Nada para compilar!"

install:

	# Aquí se instala el software. Para ello se mueven los
	# archivos necesarios a los lugares destinados para su
	# correcto funcionamiento. Es necesario crear todos los
	# directorios utilizados. Recuerda que el Makefile se
	# utiliza en la creación de la estructura de archivos 
	# del paquete.
	# Debes anteponer la variable $(DESTDIR) en todos los
	# destinos:
	# Si haces "make install", la variable $(DESTDIR) es
	# removida por no tener valor y el programa se instala
	# en el sistema tal cual.
	# Si utilizas el Makefile en el empaquetamiento, puedes
	# asignarle el valor DESTDIR=$(CURDIR)/debian/nombre-p/
	# para que sea el contenido del paquete.
	#
	# EJEMPLOS
	# mkdir -p $(DESTDIR)/usr/bin/
	# mkdir -p $(DESTDIR)/etc/skel/Escritorio/
	# cp -r desktop/nombre-p.desktop $(DESTDIR)/usr/share/applications/
	# cp -r scripts/nombre-p.py $(DESTDIR)/usr/share/nombre-p/
	# cp -r scripts/interfaz.glade $(DESTDIR)/usr/share/nombre-p/
	# cp -r scripts/canaima-bienvenido.sh $(DESTDIR)/usr/bin/nombre-p

uninstall:

# Aquí se deshace lo que se hizo en el install, borrando exactamente lo que
# se creó en el install

clean:

# Borrar todo lo hecho en build para que quede todo como estaba antes de la
# compilación

reinstall: uninstall install
