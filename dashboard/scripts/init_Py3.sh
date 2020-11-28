#!/bin/bash

sed -i 's/\r$//' init.sh; # Remove trailing \r character
clear;
echo "Setting Up and Initializing the Placidus";
echo "__________________________________________________";
echo "The platform is running on http://dawntech.brazilsouth.cloudapp.azure.com:8080";
echo "Press [CTRL]+[C] for finishing the execution";
echo "__________________________________________________";
pushd ../public; # Go to the directory where the web app's files are in
python3 ../public/server.py;

echo "The server has stopped running";