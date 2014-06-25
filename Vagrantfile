# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "debian"
  config.vm.box_url = "https://s3-eu-west-1.amazonaws.com/ffuenf-vagrant-boxes/debian/debian-7.2.0-amd64.box"
  config.vm.network :forwarded_port, guest: 80, host: 8000
  # config.vm.provider :virtualbox do |vb|
  #  
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
  config.vm.provision :shell, :path => "provision.sh"
  config.vm.synced_folder ".", "/home/vagrant"
  config.vm.provision :shell, :inline => "make environment"
  config.vm.provision :shell, :inline => "make runserver" 
 
end
