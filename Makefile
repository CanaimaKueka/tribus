#!/usr/bin/make -f
#
# Copyright (C) 2013-2014 Tribus Developers
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
# ------------------------------------------------------------------------------

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

generate_debian_base_image_i386: dependencies

	@$(FAB) generate_debian_base_image_i386

generate_debian_base_image_amd64: dependencies

	@$(FAB) generate_debian_base_image_amd64

generate_tribus_base_image_i386: dependencies

	@$(FAB) generate_tribus_base_image_i386

generate_tribus_base_image_amd64: dependencies

	@$(FAB) generate_tribus_base_image_amd64

kill_all_containers: dependencies

	@$(FAB) docker_kill_all_containers

kill_all_images: dependencies

	@$(FAB) docker_kill_all_images

kill_tribus_images: dependencies

	@$(FAB) docker_kill_tribus_images


# COMMON TASKS -----------------------------------------------------------------
# ------------------------------------------------------------------------------

environment: dependencies

	@$(FAB) environment

start: dependencies

	@$(FAB) django_runserver

stop: dependencies

	@$(FAB) docker_stop_container

login: dependencies

	@$(FAB) docker_login_container

reset: dependencies

	@$(FAB) docker_reset_container

update: dependencies

	@$(FAB) docker_update_container

sync: dependencies

	@$(FAB) django_syncdb

shell: dependencies

	@$(FAB) django_shell


# REPOSITORY TASKS ------------------------------------------------------

create_test_repository: dependencies

	@$(FAB) install_repository
	@$(FAB) select_sample_packages
	@$(FAB) get_sample_packages
	@$(FAB) index_sample_packages


install_repository: dependencies

	@$(FAB) install_repository

select_samples: dependencies

	@$(FAB) select_sample_packages

get_samples: dependencies

	@$(FAB) get_sample_packages

get_selected: dependencies

	@$(FAB) get_selected

index_selected: dependencies

	@$(FAB) index_selected

index_samples: dependencies

	@$(FAB) index_sample_packages

# -----------------------------------------------------------------------------

filldb_from_local: dependencies

	@$(FAB) filldb_from_local

filldb_from_remote: dependencies

	@$(FAB) filldb_from_remote


# INDEX TASKS -----------------------------------------------------------------

rebuild_index: dependencies

	@$(FAB) haystack_rebuild_index

purge_tasks: dependencies

	@$(FAB) celery_purge_tasks

# -----------------------------------------------------------------------------

# TESTS TASKS -----------------------------------------------------------------

wipe_repo: dependencies

	@$(FAB) wipe_repo

# -----------------------------------------------------------------------------

update_catalog: dependencies

	@$(FAB) update_catalog

compile_catalog: dependencies

	@$(FAB) compile_catalog

init_catalog: dependencies

	@$(FAB) init_catalog

extract_messages: dependencies

	@$(FAB) extract_messages

tx_push: dependencies

	@$(FAB) tx_push

tx_pull: dependencies

	@$(FAB) tx_pull


# BUILD TASKS ------------------------------------------------------------------------------

build: dependencies

	@$(FAB) build

build_sphinx: dependencies

	@$(FAB) build_sphinx

build_mo: dependencies

	@$(FAB) build_mo

build_css: dependencies

	@$(FAB) build_css

build_js: dependencies

	@$(FAB) build_js

build_man: dependencies

	@$(FAB) build_man


# CLEAN TASKS ------------------------------------------------------------------------------

clean: dependencies

	@$(FAB) clean

clean_css: dependencies

	@$(FAB) clean_css

clean_js: dependencies

	@$(FAB) clean_js

clean_mo: dependencies

	@$(FAB) clean_mo

clean_sphinx: dependencies

	@$(FAB) clean_sphinx

clean_man: dependencies

	@$(FAB) clean_man

clean_dist: dependencies

	@$(FAB) clean_dist

clean_pyc: dependencies

	@$(FAB) clean_pyc

test: dependencies

	@$(FAB) test

install: dependencies

	@$(FAB) install

bdist: dependencies

	@$(FAB) bdist

sdist: dependencies

	@$(FAB) sdist

report_setup_data: dependencies

	@$(FAB) report_setup_data

.PHONY: environment
