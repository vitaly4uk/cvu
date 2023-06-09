# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/ubuntu-22.04"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true

    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell" do |s|
    s.inline = <<-SHELL
        sudo apt update
        sudo apt -y upgrade
        sudo apt -y install python3-dev python3-pip
        sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
        wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        sudo apt update
        sudo apt -y install postgresql-14 postgresql-client-14
        sudo apt-get build-dep -y python3-psycopg2
        cd /vagrant
        sudo -H pip3 install -r requirements.txt
        if [ "$(sudo -u postgres psql -l | grep vagrant | head -n 1 | awk '{print $1}')" != "vagrant" ]
        then
          printf "Create DB vagrant with user $(whoami)"
          sudo -u postgres createdb vagrant
          sudo -u postgres psql -c "create user $(whoami) with superuser password 'vagrant'"
          if [ $? -ne 0 ]
          then
            sudo -u postgres psql -c "alter user $(whoami) with superuser password 'vagrant'"
          fi
          if [ ! -f ./local_settings.py ]
          then
            cp ./local_settings.templ.py ./local_settings.py
          fi
        fi
        if [ ! -f ./manage.py ]
        then
          django-admin startproject project .
          cat <<EOT >> ./project/settings.py

try:
    from local_settings import *
except ImportError:
    pass
EOT
        fi
        if [ -f ./latest.dump ]
        then
            PGPASSWORD=vagrant pg_restore --verbose --clean --no-acl --no-owner -h localhost -U $(whoami) -d vagrant latest.dump
        else
            python3 ./manage.py migrate  --noinput
        fi
        python3 ./manage.py test --noinput
      SHELL
    s.privileged = false
  end
end
