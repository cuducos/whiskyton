#!/usr/bin/env bash

# Python
apt-get update
apt-get install -y python-setuptools git
apt-get install -y python-dev zlib1g-dev libxml2-dev libxslt-dev # required by pyquery
easy_install pip

# Node.js and CoffeeScript
apt-get install -y curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g bower

# install project dependencies
pip install -r /vagrant/requirements.txt

# install dev tools
apt-get install -y sqlite3
pip install ipython