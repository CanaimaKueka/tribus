#!/usr/bin/env bash
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# satisfy-depends.sh - A script to satisfy Tribus dependencies on several
#                      GNU/Linux distributions.


# Supported distributions by Package Manager
DPKG_BASED="debian ubuntu canaima"
YUM_BASED="fedora"
PACMAN_BASED="arch"
EMERGE_BASED="gentoo"

# Tribus dependencies listed by Package Manager
DPKG_DEPENDS="docker.io fabric"
YUM_DEPENDS="docker-io fabric"
PACMAN_DEPENDS="docker fabric"
EMERGE_DEPENDS="docker fabric"

DEBIAN_MIRROR="http://http.us.debian.org/debian"
UBUNTU_MIRROR="http://archive.ubuntu.com/ubuntu"

# Where are our helper programs?
LSB_RELEASE="$( which lsb_release )"
MV="$( which mv )"
ECHO="$( which echo )"
SUDO="$( which sudo )"
APTGET="$( which apt-get )"
YUM="$( which yum )"

APTGETCMD="env DEBIAN_FRONTEND=noninteractive ${APTGET}"
APTGETOPTS="-qq -o Apt::Install-Recommends=false \
-o Apt::Get::Assume-Yes=true \
-o Apt::Get::AllowUnauthenticated=true \
-o DPkg::Options::=--force-confmiss \
-o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite \
-o DPkg::Options::=--force-unsafe-io"

YUMCMD="${YUM}"
YUMOPTS="-y"

# Let's try to identify which is the Operating System we are running in.
# If we dont have lsb_release, then we have to do some guessing.
if [ -n "${LSB_RELEASE}" ]; then

    DISTRO="$( ${LSB_RELEASE} -is | tr '[:upper:]' '[:lower:]' )"
    CODENAME="$( ${LSB_RELEASE} -cs | tr '[:upper:]' '[:lower:]' )"

else

    ${ECHO} 1>&2
    ${ECHO} 1>&2 " Tribus couldn't find an implementation of lsb_release."
    ${ECHO} 1>&2 " There will be difficulties guessing the version of your OS."
    ${ECHO} 1>&2

    sleep 5

    if [ -z "${DISTRO}" ] && [ -r "/etc/fedora-release" ]; then
        DISTRO="fedora"
        CODENAME="$( . "/etc/os-release" && ${ECHO} "${VERSION,,}" | \
            awk -F'(' '{ print $2 }' | sed 's/)//g' )"
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/debian_version" ]; then
        if [ -z "${DISTRO}" ] && [ -r "/etc/os-release" ]; then
            DISTRO="$( . "/etc/os-release" && ${ECHO} "${ID,,}" )"
        fi
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/lsb-release" ]; then
        DISTRO="$( . "/etc/lsb-release" && ${ECHO} "${DISTRIB_ID,,}" )"
        CODENAME="$( . "/etc/lsb-release" && ${ECHO} "${DISTRIB_CODENAME,,}" )"
    fi

fi

# This means we couldn't guess the name of your GNU/Linux Distribution
if [ -z "${DISTRO}" ]; then

    ${ECHO} 1>&2
    ${ECHO} 1>&2 " Tribus couldn't identify your OS, you will need to install"
    ${ECHO} 1>&2 " the following dependencies manually:"
    ${ECHO} 1>&2
    ${ECHO} 1>&2 "  - fabric (http://fabfile.org)"
    ${ECHO} 1>&2 "  - docker (http://docker.io)"
    ${ECHO} 1>&2

    exit 1

fi


if [ "${DPKG_BASED}" != "${DPKG_BASED/${DISTRO}}" ]; then

    # If our dependencies are met, let's exit early
    if [ -n "$( which fab )" ] && [ -n "$( which docker.io )" ]; then

        ${ECHO} "All dependencies are satisfied."
        exit 0

    fi

    if ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "wheezy" ]) || \
        ([ "${DISTRO}" == "canaima" ] && [ "${CODENAME}" == "kerepakupai" ]) || \
        ([ "${DISTRO}" == "canaima" ] && [ "${CODENAME}" == "kukenan" ]); then

        ${MV} "/etc/apt/sources.list" "/etc/apt/sources.list.bk"
        ${MV} "/etc/apt/sources.list.d" "/etc/apt/sources.list.d.bk"

        ${ECHO} "deb ${DEBIAN_MIRROR} wheezy main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t wheezy \
            iptables perl libapparmor1 libdevmapper1.02.1 \
            libsqlite3-0 adduser libc6

        ${ECHO} "deb ${DEBIAN_MIRROR} wheezy-backports main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t wheezy-backports \
            init-system-helpers fabric

        ${ECHO} "deb ${DEBIAN_MIRROR} jessie main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t jessie docker.io

        ${MV} "/etc/apt/sources.list.bk" "/etc/apt/sources.list"
        ${MV} "/etc/apt/sources.list.d.bk" "/etc/apt/sources.list.d"

        ${APTGETCMD} ${APTGETOPTS} update

    elif ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "jessie" ]) || \
        ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "sid" ]); then

        ${MV} "/etc/apt/sources.list" "/etc/apt/sources.list.bk"
        ${MV} "/etc/apt/sources.list.d" "/etc/apt/sources.list.d.bk"

        ${ECHO} "deb ${DEBIAN_MIRROR} ${CODENAME} main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install ${DPKG_DEPENDS}

        ${MV} "/etc/apt/sources.list.bk" "/etc/apt/sources.list"
        ${MV} "/etc/apt/sources.list.d.bk" "/etc/apt/sources.list.d"

        ${APTGETCMD} ${APTGETOPTS} update

    elif ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "oneiric" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "precise" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "quantal" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "raring" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "saucy" ]); then

        ${MV} "/etc/apt/sources.list" "/etc/apt/sources.list.bk"
        ${MV} "/etc/apt/sources.list.d" "/etc/apt/sources.list.d.bk"

        ${ECHO} "deb ${UBUNTU_MIRROR} ${CODENAME} main" \
            >> "/etc/apt/sources.list"
        ${ECHO} "deb ${UBUNTU_MIRROR} ${CODENAME} universe" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t ${CODENAME} \
            iptables perl libapparmor1 libdevmapper1.02.1 \
            libsqlite3-0 adduser libc6

        ${ECHO} "deb ${DEBIAN_MIRROR} wheezy-backports main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t wheezy-backports \
            init-system-helpers fabric

        ${ECHO} "deb ${DEBIAN_MIRROR} jessie main" \
            >> "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install -t jessie docker.io

        ${MV} "/etc/apt/sources.list.bk" "/etc/apt/sources.list"
        ${MV} "/etc/apt/sources.list.d.bk" "/etc/apt/sources.list.d"

        ${APTGETCMD} ${APTGETOPTS} update

    elif ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "trusty" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "utopic" ]); then

        ${MV} "/etc/apt/sources.list" "/etc/apt/sources.list.bk"
        ${MV} "/etc/apt/sources.list.d" "/etc/apt/sources.list.d.bk"

        ${ECHO} "deb ${UBUNTU_MIRROR} ${CODENAME} main" \
            > "/etc/apt/sources.list"
        ${ECHO} "deb ${UBUNTU_MIRROR} ${CODENAME} universe" \
            > "/etc/apt/sources.list"

        ${APTGETCMD} ${APTGETOPTS} update
        ${APTGETCMD} ${APTGETOPTS} install ${DPKG_DEPENDS}

        ${MV} "/etc/apt/sources.list.bk" "/etc/apt/sources.list"
        ${MV} "/etc/apt/sources.list.d.bk" "/etc/apt/sources.list.d"

        ${APTGETCMD} ${APTGETOPTS} update

    else

        ${ECHO} 1>&2
        ${ECHO} 1>&2 " Sorry. You are using an unsupported version of ${DISTRO}."
        ${ECHO} 1>&2
        ${ECHO} 1>&2 " You will need to install the following dependencies"
        ${ECHO} 1>&2 " manually:"
        ${ECHO} 1>&2
        ${ECHO} 1>&2 "  - fabric (http://fabfile.org)"
        ${ECHO} 1>&2 "  - docker (http://docker.io)"
        ${ECHO} 1>&2
        ${ECHO} 1>&2 " Please open a ticket requesting support for your distribution:"
        ${ECHO} 1>&2 " http://github.com/CanaimaGNULinux/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

elif [ "${YUM_BASED}" != "${YUM_BASED/${DISTRO}}" ]; then

    # If our dependencies are met, let's exit early
    if [ -n "$( which fab )" ] && [ -n "$( which docker )" ]; then

        ${ECHO} "All dependencies are satisfied."
        exit 0

    fi

    if ([ "${DISTRO}" == "fedora" ] && [ "${CODENAME}" == "shrodinger" ]) || \
        ([ "${DISTRO}" == "fedora" ] && [ "${CODENAME}" == "heisenbug" ]); then

        ${YUMCMD} ${YUMOPTS} install ${YUM_DEPENDS}

    else

        ${ECHO} 1>&2
        ${ECHO} 1>&2 " Sorry. You are using an unsupported version of ${DISTRO}."
        ${ECHO} 1>&2
        ${ECHO} 1>&2 " You will need to install the following dependencies"
        ${ECHO} 1>&2 " manually:"
        ${ECHO} 1>&2
        ${ECHO} 1>&2 "  - fabric (http://fabfile.org)"
        ${ECHO} 1>&2 "  - docker (http://docker.io)"
        ${ECHO} 1>&2
        ${ECHO} 1>&2 " Please open a ticket requesting support for your distribution:"
        ${ECHO} 1>&2 " http://github.com/CanaimaGNULinux/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

elif [ "${PACMAN_BASED}" != "${PACMAN_BASED/${DISTRO}}" ]; then

    pacman -S docker

elif [ "${EMERGE_BASED}" != "${EMERGE_BASED/${DISTRO}}" ]; then

    emerge -av app-emulation/docker

else

    ${ECHO} 1>&2
    ${ECHO} 1>&2 " Sorry. You are using ${DISTRO}."
    ${ECHO} 1>&2
    ${ECHO} 1>&2 " Tribus does not support your current GNU/Linux distribution."
    ${ECHO} 1>&2 " You will need to install the following dependencies"
    ${ECHO} 1>&2 " manually:"
    ${ECHO} 1>&2
    ${ECHO} 1>&2 "  - fabric (http://fabfile.org)"
    ${ECHO} 1>&2 "  - docker (http://docker.io)"
    ${ECHO} 1>&2
    ${ECHO} 1>&2 " Please open a ticket requesting support for your distribution:"
    ${ECHO} 1>&2 " http://github.com/CanaimaGNULinux/tribus/issues"
    ${ECHO} 1>&2

    exit 1

fi