#! /bin/sh
# This script starts the anti-theft system

echo "Booting...."

ENV_HOME = "/home/pi/env/anti-theft"
APP_HOME = "/home/pi/src/anti-theft"
MAIN_SCRIPT = "${APP_HOME}/main.py"

# Activate env
source "${ENV_HOME}/activate"
sudo python $MAIN_SCRIPT 192.168.43.190