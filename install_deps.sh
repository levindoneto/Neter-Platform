#!/bin/bash

# Script for installing the needed dependencies for setting up the project

# Author: Levindo Gabriel Taschetto Neto
clear;
echo "INSTALLING MININET v2.2.2";
git clone git://github.com/mininet/mininet;
cd mininet;
git checkout 2.2.2;
cd ../;
mininet/util/install.sh -a;
sudo mn --test pingall;

echo "INSTALLING PYTHON 3.6";
sudo add-apt-repository ppa:deadsnakes/ppa;
sudo apt update;
sudo apt install python3.6;
python3.6 -V;
