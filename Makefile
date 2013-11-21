#!/usr/bin/make -f
# -*- makefile -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


SHELL = sh -e
PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
FAB = fab
SU = su
APTITUDE = aptitude
FAB = $(shell which fab)
SU = $(shell which su)
APTITUDE = $(shell which aptitude)

# MAINTAINER TASKS ---------------------------------------------------------------------------------

checkpkg:

	@printf "Checking if we have $(PACKAGE) ... "
	@if [ -z $(shell which $(TESTBIN)) ]; then \
		echo "[ABSENT]"; \
		echo "Installing $(PACKAGE) ... "; \
		echo "Enter your root password:"; \
		$(SU) root -c 'DEBIAN_FRONTEND="noninteractive" $(APTITUDE) install --assume-yes --allow-untrusted -o DPkg::Options::="--force-confmiss" -o DPkg::Options::="--force-confnew" -o DPkg::Options::="--force-overwrite" $(PACKAGE)'; \
	else \
		echo "[OK]"; \
	fi
	@echo

fabric:

	@$(MAKE) checkpkg PACKAGE=fabric TESTBIN=fab
	@$(MAKE) checkpkg PACKAGE=openssh-server TESTBIN=sshd

runserver: fabric

	@$(FAB) development runserver_django

shell: fabric

	@$(FAB) development shell_django

prepare: fabric

	@$(FAB) development build_js
	@$(FAB) development build_css
	

syncdb: fabric

	@$(FAB) development syncdb_django

environment: fabric

	@$(FAB) development environment


# REPOSITORY TASKS ------------------------------------------------------

create_test_repository: fabric
	@$(FAB) development install_repository
	@$(FAB) development select_sample_packages
	@$(FAB) development get_sample_packages
	@$(FAB) development index_sample_packages

# 1
install_repository: fabric

	@$(FAB) development install_repository
# 2
select_samples: fabric

	@$(FAB) development select_sample_packages
# 3
get_samples: fabric

	@$(FAB) development get_sample_packages
# 4
index_samples: fabric

	@$(FAB) development index_sample_packages
	
# -----------------------------------------------------------------------------

filldb_from_local: fabric

	@$(FAB) development filldb_from_local 
	
filldb_from_remote: fabric

	@$(FAB) development filldb_from_remote
	

# INDEX TASKS -----------------------------------------------------------------

rebuild_index: fabric

	@$(FAB) development rebuild_index
	
# -----------------------------------------------------------------------------
	
resetdb:

	@$(FAB) development resetdb
	
update_virtualenv: fabric

	@$(FAB) development update_virtualenv

update_catalog: fabric 

	@$(FAB) development update_catalog

compile_catalog: fabric 

	@$(FAB) development compile_catalog

init_catalog: fabric 

	@$(FAB) development init_catalog

extract_messages: fabric 

	@$(FAB) development extract_messages

tx_push: fabric 

	@$(FAB) development tx_push

tx_pull: fabric 

	@$(FAB) development tx_pull


# BUILD TASKS ------------------------------------------------------------------------------

build: fabric

	@$(FAB) development build

build_sphinx: fabric

	@$(FAB) development build_sphinx

build_mo: fabric

	@$(FAB) development build_mo

build_css: fabric

	@$(FAB) development build_css

build_js: fabric

	@$(FAB) development build_js

build_man: fabric

	@$(FAB) development build_man


# CLEAN TASKS ------------------------------------------------------------------------------

clean: fabric

	@$(FAB) development clean

clean_css: fabric

	@$(FAB) development clean_css

clean_js: fabric

	@$(FAB) development clean_js

clean_mo: fabric

	@$(FAB) development clean_mo

clean_sphinx: fabric

	@$(FAB) development clean_sphinx

clean_man: fabric

	@$(FAB) development clean_man

clean_dist: fabric

	@$(FAB) development clean_dist

clean_pyc: fabric

	@$(FAB) development clean_pyc
