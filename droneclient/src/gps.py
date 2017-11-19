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
GPSLASTSTATUSMS = 0

serialPort = None

current_milli_time = lambda: int(time.time() * 1000)

def handle_newline(line):
	global GPSLAT
	global GPSLON
	global GPSTIME
	global GPSSTATUS
	global GPSLASTSTATUSMS

	if line.startswith("$GPGLL") or line.startswith("$GNGLL") or line.startswith("$GLGLL"):
		GPSLAT = line[7:9] + " " + line[9:17] + " " + line[18:19]
		GPSLON = line[20:23] + " " + line[23:31] + " " + line[32:33]
		GPSTIME = line[34:36] + ":" + line[36:38] + ":" + line[38:43]
		if line[44:45] == "A":
			GPSSTATUS = "VALID"
		else:
			GPSSTATUS = "INVALID"
		GPSLASTSTATUSMS = current_milli_time()

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

def read_from_port(gpsport, gpsbaud):
	global readOn
	global serialPort

	#wait to initialize the port
	while serialPort == None:
		try:
			serialPort = serial.Serial(gpsport, baudrate=gpsbaud, timeout=None)
		except Exception as inst:
			serialPort = None
			traceback.print_exc()
			time.sleep(5)

	#read loop
	ser = serialPort
	while readOn:
		try:
			if ser.inWaiting() > 0:
				handle_data(ser.read(ser.inWaiting()))
		except Exception as inst:
			traceback.print_exc()
	
def gpsinit(gpsport, gpsbaud):
	global thread
	thread = threading.Thread(target=read_from_port, args=(gpsport,gpsbaud,))
	thread.daemon = True
	thread.start()



