#!/bin/sh
# run mpd
screen -m -d mpd

#run flask
screen -m -d server.py
cd songs
screen -m -d python3 -m http.server
