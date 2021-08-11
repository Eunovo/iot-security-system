#! /bin/sh
# This script should be executed after every deployment
# Packages can be installed here
# Other setup can also be performed here

echo "Installing...."

ENV_HOME="/home/pi/env/anti-theft"

sudo apt-get update
sudo apt-get install python3-picamera python3-gpiozero

# Activate env
source "${ENV_HOME}/activate"
python3 -m pip install websockets
