echo 'deb http://http.us.debian.org/debian wheezy main' > /etc/apt/sources.list

# prevent init scripts from running during install/update
{
    echo $'#!/bin/sh\nexit 101'
} | tee /usr/sbin/policy-rc.d > /dev/null

chmod +x /usr/sbin/policy-rc.d
dpkg-divert --local --rename --add /sbin/initctl
ln -sf /bin/true /sbin/initctl

# Speedup Dpkg
{
    echo 'force-unsafe-io'
} | tee /etc/dpkg/dpkg.cfg.d/speedup > /dev/null

# Custom optimizations
{
    echo 'Apt::Install-Recommends "false";'
    echo 'Apt::Get::Assume-Yes "true";'
    echo 'Apt::Get::AllowUnauthenticated "true";'
    echo 'DPkg::Options:: "--force-confmiss";'
    echo 'DPkg::Options:: "--force-confnew";'
    echo 'DPkg::Options:: "--force-overwrite";'
    echo 'DPkg::Options:: "--force-unsafe-io";'
} | tee /etc/apt/apt.conf.d/custom > /dev/null

# and remove the translations, too
{
    echo 'Acquire::Languages "none";'
} | tee /etc/apt/apt.conf.d/no-languages > /dev/null

# Remove 5s grub timeout to speed up booting
cat <<EOF > /etc/default/grub
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.

GRUB_DEFAULT=0
GRUB_TIMEOUT=0
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
GRUB_CMDLINE_LINUX="debian-installer=en_US"
EOF

update-grub

# Update the box
apt-get update
apt-get install linux-headers-amd64 build-essential ca-certificates
apt-get install zlib1g-dev libssl-dev libreadline-gplv2-dev curl unzip

# Set up Vagrant.
date > /etc/vagrant_box_build_time

# Set up sudo
echo 'vagrant ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/vagrant

# Tweak sshd to prevent DNS resolution (speed up logins)
echo 'UseDNS no' >> /etc/ssh/sshd_config

# Install vagrant keys
mkdir -pm 700 /home/vagrant/.ssh
curl -Lo /home/vagrant/.ssh/authorized_keys \
  'https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub'
chmod 0600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant/.ssh

# Customize the message of the day
echo 'Welcome to your Vagrant-built virtual machine.' > /var/run/motd

echo "pre-up sleep 2" >> /etc/network/interfaces

if test -f .vbox_version; then

    # The netboot installs the VirtualBox support (old) so we have to remove it
    if test -f /etc/init.d/virtualbox-ose-guest-utils; then
        service virtualbox-ose-guest-utils stop
    fi

    rmmod -f vboxguest

    apt-get purge virtualbox-ose-guest-x11 virtualbox-ose-guest-dkms
    apt-get purge virtualbox-ose-guest-utils

    # Install dkms for dynamic compiles
    # If libdbus is not installed, virtualbox will not autostart
    apt-get install dkms libdbus-1-3

    # Install the VirtualBox guest additions
    VBOX_VERSION=$(cat .vbox_version)
    VBOX_ISO=VBoxGuestAdditions_$VBOX_VERSION.iso
    mount -o loop ${VBOX_ISO} /mnt
    yes | sh /mnt/VBoxLinuxAdditions.run
    umount /mnt
    rm ${VBOX_ISO}

    # Start the newly build driver
    service vboxadd start

    # Make a temporary mount point
    mkdir /tmp/veewee-validation

    # Test mount the veewee-validation
    mount -t vboxsf veewee-validation /tmp/veewee-validation

fi

# Clean up
apt-get purge linux-headers-amd64 build-essential ca-certificates
apt-get purge dkms zlib1g-dev libssl-dev libreadline-gplv2-dev curl unzip
apt-get autoremove
apt-get autoclean
apt-get clean

find / -name "*.pyc" -print0 | xargs -0r rm -rf
find /tmp -type f -print0 | xargs -0r rm -rf
find /var/tmp -type f -print0 | xargs -0r rm -rf
find /var/log -type f -print0 | xargs -0r rm -rf
find /var/cache/apt -type f -print0 | xargs -0r rm -rf
find /var/lib/apt/lists -type f -print0 | xargs -0r rm -rf
find /var/lib/dhcp -type f -print0 | xargs -0r rm -rf
find /var/lib/dkms -type f -print0 | xargs -0r rm -rf
find /usr/share/man -type f -print0 | xargs -0r rm -rf
find /usr/share/doc -type f -print0 | xargs -0r rm -rf
find /usr/share/locale -type f -print0 | xargs -0r rm -rf

# Make sure Udev doesn't block our network
rm -rf /lib/udev/rules.d/75-persistent-net-generator.rules
rm -rf /etc/udev/rules.d/70-persistent-net.rules
rm -rf /dev/.udev/
mkdir -p /etc/udev/rules.d/70-persistent-net.rules

# Zero out the free space to save space in the final image:
dd if=/dev/zero of=/EMPTY bs=1M
rm -rf /EMPTY
