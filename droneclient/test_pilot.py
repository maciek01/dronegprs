#!/usr/bin/env python


import time

import pilot

pilot.pilotinit("udp:localhost:14550", 115200)

while True:
	time.sleep(1)


