#!/bin/bash

sed -i 's/\r$//' init.sh; # Remove trailing \r character
clear;
echo "_________________________________________________________________________";
echo "Setting Node JS (npm) up";
sudo apt-get update;
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -;
sudo apt-get install -y nodejs;
echo "_________________________________________________________________________";
echo "Deploying hosting with the use of Firebase (this might take some minutes)";
echo "The platform will be availabe on https://placidus.firebaseapp.com";
echo "_________________________________________________________________________";
echo "Press [CTRL]+[C] to finish the execution";
echo "_________________________________________________________________________";
pushd ../;
sudo npm install -g firebase-tools;
sudo firebase login;
sudo firebase deploy --only hosting;