apt_package_install_list=()
apt_package_check_list=(
	fabric
)

# echo "deb http://http.us.debian.org/debian jessie main contrib non-free" >> /etc/apt-sources.list
echo "Check for apt packages to install..."

# Loop through each of our packages that should be installed on the system. If
# not yet installed, it should be added to the array of packages to install.
for pkg in "${apt_package_check_list[@]}"; do
	package_version="$(dpkg -s $pkg 2>&1 | grep 'Version:' | cut -d " " -f 2)"
	if [[ -n "${package_version}" ]]; then
		space_count="$(expr 20 - "${#pkg}")" #11
		pack_space_count="$(expr 30 - "${#package_version}")"
		real_space="$(expr ${space_count} + ${pack_space_count} + ${#package_version})"
		printf " * $pkg %${real_space}.${#package_version}s ${package_version}\n"
	else
		echo " *" $pkg [not installed]
		apt_package_install_list+=($pkg)
	fi
done

if [[ ${#apt_package_install_list[@]} = 0 ]]; then
                echo -e "No apt packages to install.\n"
        else
                
                # mv /etc/apt/sources.list /etc/apt/sources.list.bak
                # touch /etc/apt/sources.list
                # echo "deb http://http.us.debian.org/debian jessie main contrib non-free" >> /etc/apt/sources.list
sed 's/wheezy/testing/g' < /etc/apt/sources.list > /etc/apt/sources.list.bak; mv /etc/apt/sources.list.bak /etc/apt/sources.list
                echo "Running apt-get update..."
                aptitude update --assume-yes
                aptitude dist-upgrade --assume-yes
                # install required packages
                echo "Installing apt-get packages..."
                aptitude install --assume-yes ${apt_package_install_list[@]}
                # sed '$d' < /etc/apt/sources.list > /etc/apt/sources.list.bak; mv /etc/apt/sources.list.bak /etc/apt/sources.list
                # mv /etc/apt/sources.list.bak /etc/apt/sources.list
                aptitude update --assume-yes
                # Clean up apt caches
                apt-get clean
        fi
