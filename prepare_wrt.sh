#!/bin/sh

wget http://10.0.2.2:8000/kmod-drv-mpc8xxx_4.14.171-1_aarch64_generic.ipk
opkg install kmod-drv-mpc8xxx_4.14.171-1_aarch64_generic.ipk

#gpio
opkg update
opkg install libgpiod
opkg install gpiod-tools

#python
opkg install python3
opkg install python3-flask
opkg install python3-pip

#sound
opkg install alsa-utils
opkg install pciutils
opkg install kmod-sound-hda-intel
alsactl init
opkg install mpd-full
opkg install mpc

#utils
opkg install screen
opkg install curl

#pip
pip3 install gpiod
pip3 install python-mpd2
pip3 install requests

# set high mpd timeout to prevent client disconnecting
echo 'connection_timeout    "2000000"' >> /etc/mpd.conf
#resest
/etc/init.d/mpd restart
