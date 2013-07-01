#!/bin/sh -e
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/functions/defaults.sh
# DESCRIPCIÓN: Rutina para la definición de los valores por defecto de las
#              principales variables.
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

TIMESTAMP="$( date +%Y%m%d%H%M )"
NATIVE_ARCH="$( dpkg --print-architecture )"
LOGFILE="${LOGFILE:-build.${TIMESTAMP}.log}"

CONFIG="${CONFIG:-${BASEDIR}/scripts/config.sh}"
LIBRARY="${LIBRARY:-${BASEDIR}/scripts/library.sh}"
VARIABLES="${VARIABLES:-${CONFDIR}/config/core}"
FUNCTIONS="${FUNCTIONS:-${BASEDIR}/scripts/functions}"
MODULES="${MODULES:-${BASEDIR}/scripts/modules}"
PROFILES="${PROFILES:-${BASEDIR}/profiles}"
SCRIPTS="${SCRIPTS:-${BASEDIR}/scripts}"
ISOS="${ISOS:-${BASEDIR}/isos}"
TEMPLATES="${TEMPLATES:-${BASEDIR}/templates}"

BUILD_OP_MODE="${BUILD_OP_MODE:-normal}"
BUILD_PRINT_MODE="${BUILD_PRINT_MODE:-normal}"
PROFILE_OP_MODE="${PROFILE_OP_MODE:-create}"
SAVE_OP_MODE="${SAVE_OP_MODE:-normal}"

KVM_DISK_FILE="${KVM_DISK_FILE:-${ISOS}/kvm/canaima-semilla-hdd.img}"
KVM_DISK_MODE="${KVM_DISK_MODE:-d}"
KVM_NEW_DISK_SIZE="${KVM_NEW_DISK_SIZE:-10}"
KVM_NEW_DISK="${KVM_NEW_DISK:-false}"
KVM_PROC="${KVM_PROC:-1}"
KVM_MEM="${KVM_MEM:-256}"
