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
# bash
# sudo
# make
# lsb-release
# coreutils
# debianutils

ROOT="root"
USER="$( id -un )"

# Supported distributions by Package Manager
DPKG_BASED="debian ubuntu canaima"
YUM_BASED="fedora centos"
PACMAN_BASED="arch"
EMERGE_BASED="gentoo"

# Tribus dependencies listed by Package Manager
DPKG_DEPENDS="docker.io fabric"
YUM_DEPENDS="docker-io fabric"
PACMAN_DEPENDS="docker fabric"
EMERGE_DEPENDS="dev-python/fabric app-emulation/docker"

DEBIAN_MIRROR="http://http.us.debian.org/debian"
UBUNTU_MIRROR="http://archive.ubuntu.com/ubuntu"

# Where are our helper programs?
LSB_RELEASE="$( which lsb_release )"
MV="$( which mv )"
ECHO="$( which echo )"
SU="$( which su )"
SUDO="$( which sudo )"

# Package Manager binaries
APTGET="$( which apt-get )"
YUM="$( which yum )"
PACMAN="$( which pacman )"
EMERGE="$( which emerge )"

# Package Manager commands and options
APTGETCMD="env DEBIAN_FRONTEND=noninteractive ${APTGET}"
APTGETOPTS="-qq -o Apt::Install-Recommends=false \
-o Apt::Get::Assume-Yes=true \
-o Apt::Get::AllowUnauthenticated=true \
-o DPkg::Options::=--force-confmiss \
-o DPkg::Options::=--force-confnew \
-o DPkg::Options::=--force-overwrite \
-o DPkg::Options::=--force-unsafe-io"
YUMCMD="${YUM}"
YUMOPTS="--assumeyes --nogpgcheck --quiet"
PACMANCMD="${PACMAN}"
PACMANOPTS="--refresh --noconfirm --noprogressbar --quiet"
EMERGECMD="env ACCEPT_KEYWORDS='~amd64 ~i386' ${EMERGE}"
EMERGEOPTS="--quiet"


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
            sed 's/.*(\(.*\)).*/\1/g' )"
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/centos-release" ]; then
        DISTRO="centos"
        VERSION="$( cat /etc/centos-release | awk '{print $3}' )"
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/gentoo-release" ]; then
        DISTRO="gentoo"
        VERSION="$( cat /etc/gentoo-release | awk '{print $5}' )"
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/arch-release" ]; then
        DISTRO="arch"
    fi

    if [ -z "${DISTRO}" ] && [ -r "/etc/debian_version" ]; then

        if [ -z "${DISTRO}" ] && [ -r "/etc/os-release" ]; then

            DISTRO="$( . "/etc/os-release" && ${ECHO} "${ID,,}" )"

            if [ "${DISTRO}" == "debian" ]; then

                CODENAME="$( . "/etc/os-release" && \
                    ${ECHO} "${PRETTY_NAME,,}" | awk '{print $3}' | \
                    awk -F'/' '{print $2}' )"

            elif [ "${DISTRO}" == "ubuntu" ]; then

                CODENAME="$( . "/etc/os-release" && ${ECHO} "${VERSION,,}" | \
                    awk '{print $2}' )"

            elif [ "${DISTRO}" == "canaima" ]; then

                CODENAME="$( . "/etc/os-release" && ${ECHO} "${VERSION,,}" | \
                    sed 's/.*(\(.*\)).*/\1/g' )"

            fi

        fi

        if [ -z "${DISTRO}" ] && [ -r "/etc/lsb-release" ]; then

            DISTRO="$( . "/etc/lsb-release" && ${ECHO} "${DISTRIB_ID,,}" )"

            if [ "${DISTRO}" == "ubuntu" ]; then

                CODENAME="$( . "/etc/lsb-release" && \
                    ${ECHO} "${DISTRIB_CODENAME,,}" )"

            fi

        fi

    fi

fi

# This means we couldn't guess the name of your GNU/Linux Distribution
if [ -z "${DISTRO}" ] || [ -z "${CODENAME}" ]; then

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

        exit 0

    fi

    if ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "wheezy" ]) || \
        ([ "${DISTRO}" == "canaima" ] && [ "${CODENAME}" == "kerepakupai" ]) || \
        ([ "${DISTRO}" == "canaima" ] && [ "${CODENAME}" == "kukenan" ]); then

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list /etc/apt/sources.list.bk"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d /etc/apt/sources.list.d.bk"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} wheezy main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t wheezy \
            iptables perl libapparmor1 libdevmapper1.02.1 \
            libsqlite3-0 adduser libc6"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} wheezy-backports main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t wheezy-backports \
            init-system-helpers fabric"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} jessie main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t jessie docker.io"

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.bk /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d.bk /etc/apt/sources.list.d"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"

    elif ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "jessie" ]) || \
        ([ "${DISTRO}" == "debian" ] && [ "${CODENAME}" == "sid" ]); then

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list /etc/apt/sources.list.bk"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d /etc/apt/sources.list.d.bk"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} ${CODENAME} main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install ${DPKG_DEPENDS}"

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.bk /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d.bk /etc/apt/sources.list.d"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"

    elif ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "oneiric" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "precise" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "quantal" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "raring" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "saucy" ]); then

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list /etc/apt/sources.list.bk"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d /etc/apt/sources.list.d.bk"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${UBUNTU_MIRROR} ${CODENAME} main\" \
            > /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${ECHO} \"deb ${UBUNTU_MIRROR} ${CODENAME} universe\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t ${CODENAME} \
            iptables perl libapparmor1 libdevmapper1.02.1 \
            libsqlite3-0 adduser libc6"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} wheezy-backports main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t wheezy-backports \
            init-system-helpers fabric"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${DEBIAN_MIRROR} jessie main\" \
            > /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install -t jessie docker.io"

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.bk /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d.bk /etc/apt/sources.list.d"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"

    elif ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "trusty" ]) || \
        ([ "${DISTRO}" == "ubuntu" ] && [ "${CODENAME}" == "utopic" ]); then

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list /etc/apt/sources.list.bk"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d /etc/apt/sources.list.d.bk"

        ${SUDO} ${BASH} -c "${ECHO} \"deb ${UBUNTU_MIRROR} ${CODENAME} main\" \
            > /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${ECHO} \"deb ${UBUNTU_MIRROR} ${CODENAME} universe\" \
            >> /etc/apt/sources.list"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"
        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} install ${DPKG_DEPENDS}"

        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.bk /etc/apt/sources.list"
        ${SUDO} ${BASH} -c "${MV} /etc/apt/sources.list.d.bk /etc/apt/sources.list.d"

        ${SUDO} ${BASH} -c "${APTGETCMD} ${APTGETOPTS} update"

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
        ${ECHO} 1>&2 " http://github.com/tribusdev/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

elif [ "${YUM_BASED}" != "${YUM_BASED/${DISTRO}}" ]; then

    # If our dependencies are met, let's exit early
    if [ -n "$( which fab )" ] && [ -n "$( which docker )" ]; then

        exit 0

    fi

    if ([ "${DISTRO}" == "fedora" ] && [ "${CODENAME}" == "shrodinger" ]) || \
        ([ "${DISTRO}" == "fedora" ] && [ "${CODENAME}" == "heisenbug" ]); then

        ${SUDO} ${BASH} -c "${YUMCMD} ${YUMOPTS} install ${YUM_DEPENDS}"

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
        ${ECHO} 1>&2 " http://github.com/tribusdev/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

elif [ "${PACMAN_BASED}" != "${PACMAN_BASED/${DISTRO}}" ]; then

    # If our dependencies are met, let's exit early
    if [ -n "$( which fab )" ] && [ -n "$( which docker )" ]; then

        exit 0

    fi

    if [ "${DISTRO}" == "arch" ]; then

        ${SUDO} ${BASH} -c "${PACMANCMD} ${PACMANOPTS} -S ${PACMAN_DEPENDS}"

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
        ${ECHO} 1>&2 " http://github.com/tribusdev/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

elif [ "${EMERGE_BASED}" != "${EMERGE_BASED/${DISTRO}}" ]; then

    # If our dependencies are met, let's exit early
    if [ -n "$( which fab )" ] && [ -n "$( which docker )" ]; then

        exit 0

    fi

    if [ "${DISTRO}" == "gentoo" ]; then

        ${SUDO} ${BASH} -c "${EMERGECMD} ${EMERGEOPTS} --sync"
        ${SUDO} ${BASH} -c "${EMERGECMD} ${EMERGEOPTS} ${EMERGE_DEPENDS}"

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
        ${ECHO} 1>&2 " http://github.com/tribusdev/tribus/issues"
        ${ECHO} 1>&2

        exit 1

    fi

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
    ${ECHO} 1>&2 " http://github.com/tribusdev/tribus/issues"
    ${ECHO} 1>&2

    exit 1

fi
