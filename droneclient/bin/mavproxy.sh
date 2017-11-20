#!/bin/bash

#screen -d -m /usr/local/bin/mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --aircraft drone1 --out localhost:14550 2>&1 >/home/pi/mav.log
screen -dmS mavlinkd "/usr/local/bin/mavproxy.py --master=/dev/ttyAMA0 --baudrate 57600 --aircraft drone1 --out localhost:14550 2>&1 >>~/mav.log"


