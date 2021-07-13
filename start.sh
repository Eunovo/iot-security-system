#! /bin/sh
# This script starts the anti-theft system

echo "Booting...."

ENV_HOME="/home/pi/env/anti-theft"
APP_HOME="/home/pi/src/anti-theft"

# Activate env
source "${ENV_HOME}/activate"
cd $APP_HOME
sudo python main.py ws://anti-theft.herokuapp.com