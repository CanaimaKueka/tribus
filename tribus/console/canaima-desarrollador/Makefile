# Makefile

SHELL := sh -e

SCRIPTS =	"debian/preinst install" \
		"debian/postinst configure" \
		"debian/prerm remove" \
		"debian/postrm remove" \
		"scripts/canaima-desarrollador.sh" \
		"scripts/funciones-desarrollador.sh" \
		"scripts/manual-desarrollador.sh"

all: build

test:

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "¡TODO BIEN!\n=================================================================================\n\n"

build:
	$(MAKE) clean

	# Generar la documentación con python-sphinx
	rst2man --language="es" --title="CANAIMA DESARROLLADOR" documentos/man-canaima-desarrollador.rst documentos/canaima-desarrollador.1
	$(MAKE) -C documentos latex
	$(MAKE) -C documentos html
	$(MAKE) -C documentos/_build/latex all-pdf

	$(MAKE) test

install:

	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/canaima-desarrollador/scripts/
	mkdir -p $(DESTDIR)/etc/skel/.config/canaima-desarrollador/
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/etc/skel/Escritorio/
#	cp -r desktop/manual-desarrollador.desktop $(DESTDIR)/usr/share/applications/
#	cp -r desktop/manual-desarrollador.desktop $(DESTDIR)/etc/skel/Escritorio/
	cp -r scripts/canaima-desarrollador.sh $(DESTDIR)/usr/bin/canaima-desarrollador
	ln -s /usr/bin/canaima-desarrollador $(DESTDIR)/usr/bin/c-d
	cp -r scripts/manual-desarrollador.sh $(DESTDIR)/usr/bin/manual-desarrollador
	cp -r plantillas $(DESTDIR)/usr/share/canaima-desarrollador/
	cp -r scripts/funciones-desarrollador.sh $(DESTDIR)/usr/share/canaima-desarrollador/scripts/
	cp -r conf/variables.conf $(DESTDIR)/usr/share/canaima-desarrollador/
	cp -r conf/usuario.conf $(DESTDIR)/etc/skel/.config/canaima-desarrollador/

uninstall:

	rm -rf $(DESTDIR)/usr/share/canaima-desarrollador
	rm -rf $(DESTDIR)/usr/bin/canaima-desarrollador
	rm -rf $(DESTDIR)/usr/bin/c-d
	rm -rf $(DESTDIR)/usr/bin/manual-desarrollador
	rm -rf $(DESTDIR)/etc/skel/Escritorio/manual-desarrollador.desktop
	rm -rf $(DESTDIR)/etc/skel/.config/canaima-desarrollador/
	rm -rf $(DESTDIR)/usr/share/applications/manual-desarrollador.desktop
clean:

	rm -rf documentos/_build/*
	rm -rf documentos/canaima-desarrollador.1

distclean:

reinstall: uninstall install
