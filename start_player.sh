#!/bin/sh
screen -m -d server.py
cd songs
screen -m -d python3 -m http.server
