#!/usr/bin/env bash

set -e
set -x

REPO="${1}"
SUITE="${2}"
ARCH="${3}"

VARIANT='minbase'
INCLUDE='iproute,iputils-ping'
MIRROR="http://http.us.debian.org/debian"
TARGET="/tmp/docker-rootfs-debootstrap-${SUITE}-$$-${RANDOM}"

cd "$( dirname "$( readlink -f "${BASH_SOURCE}" )" )"
RETURNTO="$( pwd -P )"

# bootstrap
mkdir -p "${TARGET}"
sudo debootstrap --verbose --variant="${VARIANT}" \
	--include="${INCLUDE}" --arch="${ARCH}" \
	"${SUITE}" "${TARGET}" "${MIRROR}"

cd "${TARGET}"

# prevent init scripts from running during install/update
{
	echo $'#!/bin/sh\nexit 101'
} | sudo tee usr/sbin/policy-rc.d > /dev/null

sudo chmod +x usr/sbin/policy-rc.d
sudo chroot . dpkg-divert --local --rename --add /sbin/initctl
sudo ln -sf /bin/true sbin/initctl

# Speedup Dpkg
{
	echo 'force-unsafe-io'
} | sudo tee etc/dpkg/dpkg.cfg.d/speedup > /dev/null

# Custom optimizations
{
	echo 'Apt::Install-Recommends "false";'
	echo 'Apt::Get::Assume-Yes "true";'
	echo 'Apt::Get::AllowUnauthenticated "true";'
	echo 'DPkg::Options:: "--force-confmiss";'
	echo 'DPkg::Options:: "--force-confnew";'
	echo 'DPkg::Options:: "--force-overwrite";'
	echo 'DPkg::Options:: "--force-unsafe-io";'
} | sudo tee etc/apt/apt.conf.d/custom > /dev/null

# and remove the translations, too
{
	echo 'Acquire::Languages "none";'
} | sudo tee etc/apt/apt.conf.d/no-languages > /dev/null

# shrink the image, since apt makes us fat (wheezy: ~157.5MB vs ~120MB)
sudo chroot . apt-get clean

# Remove other stuff
find usr -name "*.pyc" -print0 | xargs -0r sudo rm -rfv
find var/cache/apt -type f -print0 | xargs -0r sudo rm -rfv
find var/lib/apt/lists -type f -print0 | xargs -0r sudo rm -rfv
find usr/share/man -type f -print0 | xargs -0r sudo rm -rfv
find usr/share/doc -type f -print0 | xargs -0r sudo rm -rfv
find usr/share/locale -type f -print0 | xargs -0r sudo rm -rfv
find var/log -type f -print0 | xargs -0r sudo rm -rfv
find var/tmp -type f -print0 | xargs -0r sudo rm -rfv
find tmp -type f -print0 | xargs -0r sudo rm -rfv

# create the image (and tag ${REPO}:${SUITE})
sudo tar --numeric-owner -c . | sudo docker.io import - ${REPO}:${SUITE}

# cleanup
cd "${RETURNTO}"
sudo rm -rf "${TARGET}"