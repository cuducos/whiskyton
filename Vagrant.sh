#!/usr/bin/env bash

# Python
apt-get update
sudo apt-get install -y python-setuptools ipython
easy_install pip

# Node.js and CoffeeScript
apt-get install -y curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g bower

# install project dependencies
pip install -r /vagrant/requirements.txt