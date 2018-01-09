#! /bin/bash

sudo apt-get update
sudo apt-get install -y emacs
sudo apt-get install -y htop
sudo apt-get install -y haproxy
sudo apt-get install -y tor
sudo apt-get install -y gcc
sudo apt-get install -y g++
sudo apt-get install -y make
wget http://delegate.hpcc.jp/anonftp/DeleGate/delegate9.9.13.tar.gz
tar -xvf delegate9.9.13.tar.gz
cd delegate9.9.13
make
cd ..
sudo service tor stop
