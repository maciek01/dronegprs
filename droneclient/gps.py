#!/usr/bin/env python

import sys, traceback
import serial, threading
import time, datetime



readOn = True

buffer = ""
getLine = ""

thread = None

GPSLAT = ""
GPSLON = ""
GPSTIME = ""
GPSSTATUS = "INVALID"
GPSTIMESTAMP = 0

def handle_newline(line):
	global GPSLAT
	global GPSLON
	global GPSTIME
	global GPSSTATUS

	if line.startswith("$GPGLL") or line.startswith("$GNGLL") or line.startswith("$GLGLL"):
		GPSLAT = line[7:9] + " " + line[9:17] + " " + line[18:19]
		GPSLON = line[20:23] + " " + line[23:31] + " " + line[32:33]
		GPSTIME = line[34:36] + ":" + line[36:38] + ":" + line[38:43]
		if line[44:45] == "A":
			GPSSTATUS = "VALID"
		else:
			GPSSTATUS = "INVALID"

def handle_data(data):
	global buffer
	global getLine
	for d in data:
		if d == '\n':
			getLine = buffer
			buffer = ""
			#print (getLine)
			handle_newline(getLine)
		else:
			buffer = buffer + str(d)

def read_from_port(ser):
	global readOn
	while readOn:
		try:
			if ser.inWaiting() > 0:
				handle_data(ser.read(ser.inWaiting()))
		except Exception as inst:
			traceback.print_exc()
	
def gpsinit(gpsport, gpsbaud):
	global thread
	serial_port = serial.Serial(gpsport, baudrate=gpsbaud, timeout=None)
	thread = threading.Thread(target=read_from_port, args=(serial_port,))
	thread.daemon = True
	thread.start()



