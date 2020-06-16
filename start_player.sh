#!/bin/sh

#probe gpiod
modprobe gpio-mpc8xxx
cd songs
screen -m -d python3 -m http.server
cd ..
#run flask
screen -m -d server.py
