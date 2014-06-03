#!/usr/bin/env bash

set -e
set -x

variant='minbase'
include='iproute,iputils-ping,eatmydata,apt-cacher-ng'

repo="$1"
suite="$2"
arch="$3"
mirror="http://http.us.debian.org/debian"

docker='docker.io'
lsbDist='Debian'

target="/tmp/docker-rootfs-debootstrap-$suite-$$-$RANDOM"

cd "$( dirname "$( readlink -f "$BASH_SOURCE" )" )"
returnTo="$( pwd -P )"

# bootstrap
mkdir -p "$target"
sudo debootstrap --verbose --variant="$variant" --include="$include" --arch="$arch" "$suite" "$target" "$mirror"

cd "$target"

# prevent init scripts from running during install/update
#  policy-rc.d (for most scripts)
{
	echo $'#!/bin/sh\nexit 101'
} | sudo tee usr/sbin/policy-rc.d > /dev/null

sudo chmod +x usr/sbin/policy-rc.d
#  initctl (for some pesky upstart scripts)
sudo chroot . dpkg-divert --local --rename --add /sbin/initctl
sudo ln -sf /bin/true sbin/initctl
# see https://github.com/dotcloud/docker/issues/446#issuecomment-16953173

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
	echo 'Acquire::http::proxy "http://localhost:3142";'
} | sudo tee etc/apt/apt.conf.d/custom > /dev/null

# and remove the translations, too
{
	echo 'Acquire::Languages "none";'
} | sudo tee etc/apt/apt.conf.d/no-languages > /dev/null

# shrink the image, since apt makes us fat (wheezy: ~157.5MB vs ~120MB)
sudo chroot . apt-get clean

# Remove other stuff
find usr -name "*.pyc" -print0 | xargs -0r sudo rm -rfv
find var/cache/apt/archives -type c -print0 | xargs -0r sudo rm -rfv
find var/lib/apt/lists -type c -print0 | xargs -0r sudo rm -rfv
find var/cache/man -type c -print0 | xargs -0r sudo rm -rfv
find usr/share/doc -type c -print0 | xargs -0r sudo rm -rfv
find var/log -type c -print0 | xargs -0r sudo rm -rfv
find var/tmp -type c -print0 | xargs -0r sudo rm -rfv
find tmp -type c -print0 | xargs -0r sudo rm -rfv

sudo rm -rf var/cache/apt/srcpkgcache.bin
sudo rm -rf var/cache/apt/pkgcache.bin

# create the image (and tag $repo:$suite)
sudo tar --numeric-owner -c . | $docker import - $repo:$suite

# test the image
$docker run -i -t $repo:$suite echo success

# cleanup
cd "$returnTo"
sudo rm -rf "$target"