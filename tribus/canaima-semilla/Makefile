# Makefile

SHELL = sh -e

# Datos del Proyecto
AUTHOR = Luis Alejandro Martínez Faneyth
EMAIL = luis@huntingbears.com.ve
MAILIST = desarrolladores@canaima.softwarelibre.gob.ve
PACKAGE = Canaima Semilla
CHARSET = UTF-8
VERSION = $(shell cat VERSION | grep "VERSION" | sed 's/VERSION="//g;s/+.*//g')
YEAR = $(shell date +%Y)

# Datos de traducción
LANGTEAM = Equipo de Traducción de Canaima Semilla <desarrolladores@canaima.softwarelibre.gob.ve>
POTITLE = Plantilla de Traducción para Canaima Semilla
POTEAM = Equipo de Traducción de Canaima Semilla
PODATE = $(shell date +%F\ %R%z)
PYLOCALE = canaimasemilla/translator.py
POTDIR = locale/pot/canaima-semilla/
GUIPOTNAME = c-s-gui.pot
COREPOTNAME = c-s-core.pot
GUIPOTLISTNAME = POTFILES.gui.in
COREPOTLISTNAME = POTFILES.core.in
GUIPOT = $(POTDIR)$(GUIPOTNAME)
COREPOT = $(POTDIR)$(COREPOTNAME)
GUIPOTLIST = $(POTDIR)$(GUIPOTLISTNAME)
COREPOTLIST = $(POTDIR)$(COREPOTLISTNAME)
LOCALETYPES = core gui

# Listas de Archivos
SCRIPTS = $(shell find ./scripts -type f -iname "*.sh")
DOCIMAGES = $(shell ls -1 documentation/rest/images/ | grep "\.svg" | sed 's/\.svg//g')
GUIIMAGES = $(shell ls -1 canaimasemilla/images/ | grep "\.svg" | sed 's/\.svg//g')
ICOIMAGES = $(shell ls -1 icons/hicolor/scalable/apps/ | grep "\.svg" | sed 's/\.svg//g')
LOCALES = $(shell find locale -mindepth 1 -maxdepth 1 -type d | sed 's|locale/pot||g;s|locale/||g')
PYCS = $(shell find . -type f -iname "*.pyc")

ICOSIZES = 16x16 22x22 24x24 32x32 48x48 64x64 128x128 256x256

# Dependencias de Construcción
# Tareas de Construcción
# gen-img: genera imágenes png a partir de svg. Usa CONVERT, LIBSVG e ICOTOOL.
# gen-mo: genera archivos mo a partir de archivos po. Usa MSGFMT.
# gen-doc: construye toda la documentación
#       - gen-man: genera una página de manual (man). Usa RST2MAN.
#       - gen-wiki: genera código wiki para github y googlecode a partir de fuentes rest. Usa PYTHON.
#       - gen-html: genera el manual HTML a partir de las fuentes rest. Usa SPHINX.
PYTHON = $(shell which python)
SHELLBIN = $(shell which sh)
RST2MAN = $(shell which rst2man)
SPHINX = $(shell which sphinx-build)
MSGFMT = $(shell which msgfmt)
CONVERT = $(shell which convert)
ICOTOOL = $(shell which icotool)
LIBSVG = $(shell find /usr/lib/ -maxdepth 1 -type d -iname "imagemagick-*")/modules-Q16/coders/svg.so
LIBRSVGBIN = $(shell which rsvg)

# Dependencias de Instalación
# Tareas de Instalación
# install: instala canaima-semilla. Necesita LIVEBUILD.
LIVEBUILD = $(shell which live-build)

# Dependencias de tareas de mantenimiento
# generatepot: generates POT template from php sources. Uses XGETTEXT.
# updatepos: updates PO files from POT files. Uses MSGMERGE.
# snapshot: makes a new development snapshot. Uses SHELLBIN and GIT.
# release: makes a new release. Uses SHELLBIN, GIT, PYTHON, MD5SUM, TAR and GBP.
PYTHON = $(shell which python)
SHELLBIN = $(shell which sh)
GIT = $(shell which git)
MSGMERGE = $(shell which msgmerge)
XGETTEXT = $(shell which xgettext)
DEVSCRIPTS = $(shell which debuild)
DPKGDEV = $(shell which dpkg-buildpackage)
DEBHELPER = $(shell which dh)
GBP = $(shell which git-buildpackage)
LINTIAN = $(shell which lintian)
GNUPG = $(shell which gpg)
MD5SUM = $(shell which md5sum)
TAR = $(shell which tar)
BASHISMS = $(shell which checkbashisms)

all: build

build: gen-img gen-mo gen-doc

gen-doc: gen-wiki gen-html gen-man

gen-predoc: clean-predoc

	@echo "Preprocesando documentación ..."
	@$(SHELLBIN) tools/predoc.sh build

gen-wiki: check-buildep gen-img gen-predoc clean-wiki

	@echo "Generando documentación desde las fuentes [RST > WIKI]"
	@cp documentation/githubwiki.index documentation/rest/Home.md
	@cp documentation/rest/*.md documentation/rest/*.rest documentation/githubwiki/
	@rm -rf documentation/rest/Home.md
	@cp documentation/googlewiki.index documentation/rest/index.rest
	@echo "" >> documentation/rest/index.rest
	@cat documentation/rest/contents.rest >> documentation/rest/index.rest
	@mv documentation/rest/contents.rest documentation/rest/contents.tmp
	@$(PYTHON) -B tools/googlecode-wiki.py
	@mv documentation/rest/contents.tmp documentation/rest/contents.rest
	@rm -rf documentation/rest/index.rest

gen-html: check-buildep gen-img gen-predoc clean-html

	@echo "Generando documentación desde las fuentes [RST > HTML]"
	@cp documentation/sphinx.index documentation/rest/index.rest
	@$(SPHINX) -E -Q -b html -d documentation/html/doctrees documentation/rest documentation/html
	@rm -rf documentation/rest/index.rest documentation/html/doctrees documentation/html/objects.inv

gen-man: check-buildep gen-predoc clean-man

	@echo "Generando documentación desde las fuentes [RST > MAN]"
	@$(RST2MAN) --language="es" --title="CANAIMA SEMILLA" documentation/man/canaima-semilla.rest documentation/man/canaima-semilla.1

gen-img: check-buildep clean-img

	@printf "Generando imágenes desde las fuentes [SVG > PNG,JPG,ICO] ["
	@for IMAGE in $(DOCIMAGES); do \
		$(CONVERT) -background None documentation/rest/images/$${IMAGE}.svg \
			documentation/rest/images/$${IMAGE}.png; \
		$(CONVERT) -background None documentation/rest/images/$${IMAGE}.png \
			documentation/rest/images/$${IMAGE}.jpg; \
		printf "."; \
	done;
	@for IMAGE in $(GUIIMAGES); do \
		$(CONVERT) -background None canaimasemilla/images/$${IMAGE}.svg \
			canaimasemilla/images/$${IMAGE}.png; \
		printf "."; \
	done;
	@for IMAGE in $(ICOIMAGES); do \
		for SIZE in $(ICOSIZES); do \
			mkdir -p icons/hicolor/$${SIZE}/apps/; \
			$(CONVERT) -background None icons/hicolor/scalable/apps/$${IMAGE}.svg \
				-resize $${SIZE} icons/hicolor/$${SIZE}/apps/$${IMAGE}.png; \
			printf "."; \
		done; \
	done;
	@$(ICOTOOL) -c -o documentation/rest/images/favicon.ico \
		documentation/rest/images/favicon.png
	@printf "]\n"

gen-mo: check-buildep clean-mo

	@printf "Generando mensajes de traducción desde las fuentes [PO > MO] ["
	@for LOCALE in $(LOCALES); do \
		for TYPE in $(LOCALETYPES); do \
			$(MSGFMT) locale/$${LOCALE}/LC_MESSAGES/c-s-$${TYPE}.po \
				-o locale/$${LOCALE}/LC_MESSAGES/c-s-$${TYPE}.mo; \
			printf "."; \
		done; \
	done
	@printf "]\n"

# INSTALL TASKS ------------------------------------------------------------------------------

install: install-core install-doc install-gui

install-core:

	@mkdir -p $(DESTDIR)/usr/bin
	@mkdir -p $(DESTDIR)/etc/canaima-semilla/core
	@mkdir -p $(DESTDIR)/usr/share/canaima-semilla
	@cp c-s-core.sh $(DESTDIR)/usr/bin/c-s
	@cp -r scripts templates profiles $(DESTDIR)/usr/share/canaima-semilla/
	@cp config/core/* $(DESTDIR)/etc/canaima-semilla/core/

install-common:

	@mkdir -p $(DESTDIR)/usr/share/locale
	@mkdir -p $(DESTDIR)/usr/share/icons/hicolor
	@cp -r locale/* $(DESTDIR)/usr/share/locale/
	@cp -r icons/hicolor/* $(DESTDIR)/usr/share/icons/hicolor/
	@rm -rf $(DESTDIR)/usr/share/locale/pot

install-doc:

	@mkdir -p $(DESTDIR)/usr/share/applications/
	@mkdir -p $(DESTDIR)/usr/share/doc/canaima-semilla/
	@cp c-s-manual.desktop $(DESTDIR)/usr/share/applications/
	@cp -r documentation/html $(DESTDIR)/usr/share/doc/canaima-semilla/

install-gui:

	@mkdir -p $(GUIDIR)/usr/share/applications/
	@mkdir -p $(GUIDIR)/usr/share/canaima-semilla/
	@mkdir -p $(DESTDIR)/etc/canaima-semilla/gui
	@cp c-s-gui.desktop $(GUIDIR)/usr/share/applications/
	@cp -r gui $(GUIDIR)/usr/share/canaima-semilla/
	@cp config/gui/* $(DESTDIR)/etc/canaima-semilla/gui/

uninstall:

	@rm -rf /usr/bin/c-s
	@rm -rf /usr/share/canaima-semilla
	@rm -rf /usr/share/doc/canaima-semilla
	@rm -f /usr/share/locale/*/LC_MESSAGES/canaima-semilla.mo
	@rm -f /usr/share/applications/c-s-manual.desktop
	@rm -f /usr/share/applications/c-s-gui.desktop

# MAINTAINER TASKS ---------------------------------------------------------------------------------

prepare: check-maintdep

	@git submodule init
	@git submodule update
	@cd documentation/githubwiki/ && git checkout development && git pull origin development
	@cd documentation/googlewiki/ && git checkout development && git pull origin development

pull-po: check-maintdep

	@tx pull -a

push-po: check-maintdep

	@tx push --source --translations

gen-po: check-maintdep gen-pot

	@printf "Actualizando archivos de traducción desde plantilla [POT > PO] ["
	@for LOCALE in $(LOCALES); do \
		for TYPE in $(LOCALETYPES); do \
			$(MSGMERGE) --no-wrap -q -s -U locale/$${LOCALE}/LC_MESSAGES/c-s-$${TYPE}.po \
				locale/pot/canaima-semilla/c-s-$${TYPE}.pot; \
			sed -i -e ':a;N;$$!ba;s|#, fuzzy\n||g' locale/$${LOCALE}/LC_MESSAGES/c-s-$${TYPE}.po; \
			rm -rf locale/$${LOCALE}/LC_MESSAGES/c-s-$${TYPE}.po~; \
			printf "."; \
		done; \
	done
	@printf "]\n"

gen-pot: check-maintdep

	@echo "Actualizando plantilla de traducción [ POT ] ..."
	@rm -rf $(COREPOTLIST) $(GUIPOTLIST)
	@cp locale/pot/canaima-semilla/c-s-gui.pot.in locale/pot/canaima-semilla/c-s-gui.pot
	@cp locale/pot/canaima-semilla/c-s-core.pot.in locale/pot/canaima-semilla/c-s-core.pot
	@for FILE in $(SCRIPTS); do \
		echo "../../.$${FILE}" >> $(COREPOTLIST); \
	done
	@echo "../../../$(PYLOCALE)" > $(GUIPOTLIST)
	@cd locale/pot/canaima-semilla/ && $(XGETTEXT) --msgid-bugs-address="$(MAILIST)" \
		--package-version="$(VERSION)" --package-name="$(PACKAGE)" --copyright-holder="$(AUTHOR)" \
		--no-wrap --from-code=utf-8 --language=Shell -kERRORMSG -kCONFIGMSG -kMSG -kWARNINGMSG \
		-kINFOMSG -kSUCCESSMSG -s -j -o $(COREPOTNAME) -f $(COREPOTLISTNAME)
	@cd locale/pot/canaima-semilla/ && $(XGETTEXT) --msgid-bugs-address="$(MAILIST)" \
		--package-version="$(VERSION)" --package-name="$(PACKAGE)" --copyright-holder="$(AUTHOR)" \
		--no-wrap --from-code=utf-8 --language=Python -k_ -s -j -o $(GUIPOTNAME) -f $(GUIPOTLISTNAME)
	@for TYPE in $(LOCALETYPES); do \
		sed -i -e 's/# SOME DESCRIPTIVE TITLE./# $(POTITLE)./' \
		-e 's/# Copyright (C) YEAR Luis Alejandro Martínez Faneyth/# Copyright (C) $(YEAR) $(AUTHOR)/' \
		-e 's/same license as the PACKAGE package./same license as the $(PACKAGE) package./' \
		-e 's/# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR./#\n# Translators:\n# $(AUTHOR) <$(EMAIL)>, $(YEAR)/' \
		-e 's/"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"/"PO-Revision-Date: $(PODATE)\\n"/' \
		-e 's/"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"/"Last-Translator: $(AUTHOR) <$(EMAIL)>\\n"/' \
		-e 's/"Language-Team: LANGUAGE <LL@li.org>\\n"/"Language-Team: $(POTEAM) <$(MAILIST)>\\n"/' \
		-e 's/"Language: \\n"/"Language: English\\n"/g' locale/pot/canaima-semilla/c-s-$${TYPE}.pot; \
		sed -i -e ':a;N;$$!ba;s|#, fuzzy\n||g' locale/pot/canaima-semilla/c-s-$${TYPE}.pot; \
	done

gen-test:

	@printf "Buscando errores de sintaxis en shell scripts ["
	@for SCRIPT in $(SCRIPTS); \
	do \
		printf "." \
		$(SHELLBIN) -n $${SCRIPT}; \
		$(BASHISMS) -f -x $${SCRIPT} || true; \
	done
	@printf "]\n"

snapshot: check-maintdep prepare gen-html gen-wiki gen-po clean-all

	@$(MAKE) clean-all
	@$(SHELLBIN) tools/snapshot.sh

release: check-maintdep

	@$(SHELLBIN) tools/release.sh

deb-test-snapshot: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh test-snapshot

deb-test-release: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh test-release

deb-final-release: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh final-release

# CLEAN TASKS ------------------------------------------------------------------------------

clean: clean-img clean-mo clean-man clean-predoc clean-pyc

clean-all: clean-img clean-mo clean-html clean-wiki clean-man clean-predoc clean-pyc

clean-pyc:

	@printf "Cleaning precompilated python files ["
	@for PYC in $(PYCS); do \
		rm -rf $${PYC}; \
		printf "."; \
	done
	@printf "]\n"

clean-predoc:

	@echo "Cleaning preprocessed documentation files ..."
	@$(SHELLBIN) tools/predoc.sh clean
	@rm -rf documentation/rest/index.rest

clean-img:

	@printf "Cleaning generated images [JPG,ICO] ["
	@for IMAGE in $(DOCIMAGES); do \
		rm -rf documentation/rest/images/$${IMAGE}.jpg; \
		rm -rf documentation/rest/images/$${IMAGE}.png; \
		printf "."; \
	done
	@for IMAGE in $(GUIIMAGES); do \
		rm -rf canaimasemilla/images/$${IMAGE}.png; \
		printf "."; \
	done
	@for IMAGE in $(ICOIMAGES); do \
		for SIZE in $(ICOSIZES); do \
			rm -rf icons/hicolor/$${SIZE}; \
			printf "."; \
		done; \
	done
	@rm -rf documentation/rest/images/favicon.ico
	@printf "."
	@printf "]\n"

clean-mo:

	@printf "Cleaning generated localization ["
	@for LOCALE in $(LOCALES); do \
		rm -rf locale/$${LOCALE}/LC_MESSAGES/*.mo; \
		printf "."; \
	done
	@printf "]\n"

clean-html:

	@echo "Cleaning generated html ..."
	@rm -rf documentation/html/*
	@rm -rf documentation/html/.buildinfo

clean-wiki:

	@echo "Cleaning generated wiki pages ..."
	@rm -rf documentation/googlewiki/*
	@rm -rf documentation/githubwiki/*

clean-man:

	@echo "Cleaning generated man pages ..."
	@rm -rf documentation/man/canaima-semilla.1

# CHECK DEPENDENCIES ---------------------------------------------------------------------------------------------

check-instdep:

	@printf "Checking if we have Live Build ... "
	@if [ -z $(LIVEBUILD) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"live-build\" package."; \
		exit 1; \
	fi
	@echo

check-maintdep:

	@printf "Checking if we have python ... "
	@if [ -z $(PYTHON) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have a shell ... "
	@if [ -z $(SHELLBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"bash\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git... "
	@if [ -z $(GIT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-core\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have xgettext ... "
	@if [ -z $(XGETTEXT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have msgmerge ... "
	@if [ -z $(MSGMERGE) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have debhelper ... "
	@if [ -z $(DEBHELPER) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"debhelper\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have devscripts ... "
	@if [ -z $(DEVSCRIPTS) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"devscripts\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have dpkg-dev ... "
	@if [ -z $(DPKGDEV) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"dpkg-dev\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git-buildpackage ... "
	@if [ -z $(GBP) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-buildpackage\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have lintian ... "
	@if [ -z $(LINTIAN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"lintian\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have gnupg ... "
	@if [ -z $(GNUPG) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gnupg\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have md5sum ... "
	@if [ -z $(MD5SUM) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"coreutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have tar ... "
	@if [ -z $(TAR) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"tar\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have checkbashisms ... "
	@if [ -z $(BASHISMS) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"devscripts\" package."; \
		exit 1; \
	fi
	@echo

check-buildep:

	@printf "Checking if we have python ... "
	@if [ -z $(PYTHON) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have a shell... "
	@if [ -z $(SHELLBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"bash\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have sphinx-build ... "
	@if [ -z $(SPHINX) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python-sphinx\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have convert ... "
	@if [ -z $(CONVERT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"imagemagick\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have rst2man ... "
	@if [ -z $(RST2MAN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python-docutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have msgfmt ... "
	@if [ -z $(MSGFMT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have icotool ... "
	@if [ -z $(ICOTOOL) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"icoutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have imagemagick svg support ... "
	@if [ -z $(LIBSVG) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"libmagickcore-extra\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have imagemagick rsvg support ... "
	@if [ -z $(LIBRSVGBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"librsvg2-bin\" package."; \
		exit 1; \
	fi
	@echo
