#! /bin/sh
# This script starts the anti-theft system

echo "Booting...."

# ENV_HOME="/home/pi/env/anti-theft"
APP_HOME="/home/pi/iot-security-system"

# Activate env
# source "${ENV_HOME}/bin/activate"
cd $APP_HOME
sudo python3 --version
sudo python3 main.py ws://anti-theft.herokuapp.com
