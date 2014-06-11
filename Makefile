#!/usr/bin/make -f
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



# COMMON VARIABLES & CONFIG ----------------------------------------------------

SHELL = sh -e
PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
FAB = $(shell which fab)
BASH = $(shell which bash)
SU = $(shell which su)
SUDO = $(shell which sudo)
APTITUDE = $(shell which aptitude)
USER = $(shell id -u -n)
ROOT = root


# HELPER TASKS -----------------------------------------------------------------
# ------------------------------------------------------------------------------

dependencies:

	@# With this script we will satisfy dependencies on the supported
	@# distributions.
	@$(BASH) tribus/data/scripts/satisfy-depends.sh

generate_debian_base_image_i386:

	@$(FAB) development generate_debian_base_image_i386

generate_debian_base_image_amd64:

	@$(FAB) development generate_debian_base_image_amd64

generate_tribus_base_image_i386:

	@$(FAB) development generate_tribus_base_image_i386

generate_tribus_base_image_amd64:

	@$(FAB) development generate_tribus_base_image_amd64


# COMMON TASKS -----------------------------------------------------------------
# ------------------------------------------------------------------------------

environment: dependencies

	@$(FAB) development environment

runserver: dependencies

	@$(FAB) development runserver

stopserver: dependencies

	@$(FAB) development stopserver

restartserver: dependencies

	@$(FAB) development restartserver

syncdb: dependencies

	@$(FAB) development syncdb

shell: dependencies

	@$(FAB) development shell

prepare: dependencies

	@$(FAB) development build_js
	@$(FAB) development build_css


# REPOSITORY TASKS ------------------------------------------------------

create_test_repository: dependencies

	@$(FAB) development install_repository
	@$(FAB) development select_sample_packages
	@$(FAB) development get_sample_packages
	@$(FAB) development index_sample_packages


install_repository: dependencies

	@$(FAB) development install_repository

select_samples: dependencies

	@$(FAB) development select_sample_packages

get_samples: dependencies

	@$(FAB) development get_sample_packages
	
get_selected: dependencies

	@$(FAB) development get_selected
	
index_selected: dependencies

	@$(FAB) development index_selected

index_samples: dependencies

	@$(FAB) development index_sample_packages
	
# -----------------------------------------------------------------------------

filldb_from_local: dependencies

	@$(FAB) development filldb_from_local 
	
filldb_from_remote: dependencies

	@$(FAB) development filldb_from_remote
	

# INDEX TASKS -----------------------------------------------------------------

rebuild_index: dependencies

	@$(FAB) development rebuild_index
	
clean_tasks: dependencies

	@$(FAB) development clean_tasks
	
# -----------------------------------------------------------------------------

# TESTS TASKS -----------------------------------------------------------------

wipe_repo: dependencies

	@$(FAB) development wipe_repo
	
# -----------------------------------------------------------------------------
	
resetdb:

	@$(FAB) development resetdb
	
update_virtualenv: dependencies

	@$(FAB) development update_virtualenv

update_catalog: dependencies 

	@$(FAB) development update_catalog

compile_catalog: dependencies 

	@$(FAB) development compile_catalog

init_catalog: dependencies 

	@$(FAB) development init_catalog

extract_messages: dependencies 

	@$(FAB) development extract_messages

tx_push: dependencies 

	@$(FAB) development tx_push

tx_pull: dependencies 

	@$(FAB) development tx_pull


# BUILD TASKS ------------------------------------------------------------------------------

build: dependencies

	@$(FAB) development build

build_sphinx: dependencies

	@$(FAB) development build_sphinx

build_mo: dependencies

	@$(FAB) development build_mo

build_css: dependencies

	@$(FAB) development build_css

build_js: dependencies

	@$(FAB) development build_js

build_man: dependencies

	@$(FAB) development build_man


# CLEAN TASKS ------------------------------------------------------------------------------

clean: dependencies

	@$(FAB) development clean

clean_css: dependencies

	@$(FAB) development clean_css

clean_js: dependencies

	@$(FAB) development clean_js

clean_mo: dependencies

	@$(FAB) development clean_mo

clean_sphinx: dependencies

	@$(FAB) development clean_sphinx

clean_man: dependencies

	@$(FAB) development clean_man

clean_dist: dependencies

	@$(FAB) development clean_dist

clean_pyc: dependencies

	@$(FAB) development clean_pyc

test: dependencies

	@$(FAB) development test

install: dependencies

	@$(FAB) development install

bdist: dependencies

	@$(FAB) development bdist

sdist: dependencies

	@$(FAB) development sdist

report_setup_data: dependencies

	@$(FAB) development report_setup_data