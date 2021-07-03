#! /bin/sh
# This script should be executed after every deployment
# Packages can be installed here
# Other setup can also be performed here

echo "Installing...."

ENV_HOME="/home/pi/env/anti-theft"

sudo apt-get install python3-picamera

# Activate env
#source "${ENV_HOME}/activate"