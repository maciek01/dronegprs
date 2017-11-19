#!/bin/bash

#exec 1> >(logger -s -t $(basename $0)) 2>&1

cd /home/pi/dronegprs/droneclient

#start drone controller

#/usr/bin/python /home/pi/dronegprs/droneclient/src/Main.py 2>&1 >>/dev/null &
/usr/bin/python /home/pi/dronegprs/droneclient/src/Main.py 2>&1 &

echo $! >/var/run/droneclientd/droneclientd.pid

