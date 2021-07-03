#! /bin/sh
# This script starts the anti-theft system

echo "Booting...."

ENV_HOME = "/home/pi/env/anti-theft"

# Activate env
source "${ENV_HOME}/activate"
python main.py