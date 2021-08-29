#! /bin/sh
# This script starts the anti-theft system

echo "Booting...."

APP_HOME="/home/pi/iot-security-system"


sudo apt-get update -y
sudo apt-get install -y python3-picamera python3-gpiozero

cd $APP_HOME
sudo python3 --version
sudo python3 -m pip install requests
sudo python3 -m pip install websockets
sudo python3 main.py ws://anti-theft.herokuapp.com https://anti-theft.herokuapp.com/log
