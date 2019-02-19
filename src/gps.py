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
GPSLATNORM = 0
GPSLONNORM = 0
GPSTIME = ""
GPSSTATUS = "INVALID"
GPSTIMESTAMP = 0
GPSLASTSTATUSMS = 0

serialPort = None

current_milli_time = lambda: int(time.time() * 1000)

def handle_newline(line):
	global GPSLAT
	global GPSLATNORM
	global GPSLON
	global GPSLONNORM
	global GPSTIME
	global GPSSTATUS
	global GPSLASTSTATUSMS

	if line.startswith("$GPGLL") or line.startswith("$GNGLL") or line.startswith("$GLGLL"):
		#print line
		GPSLAT = line[7:9] + " " + line[9:17] + " " + line[18:19]
		GPSLATNORM = (float(line[7:9]) + float(line[9:17]) / 60.0) * (1 if line[18:19].lower() == "n" else -1)
		GPSLON = line[20:23] + " " + line[23:31] + " " + line[32:33]
		GPSLONNORM = (float(line[20:23]) + float(line[23:31]) / 60.0) * (1 if line[32:33].lower() == "e" else -1)
		GPSTIME = line[34:36] + ":" + line[36:38] + ":" + line[38:43]
		if line[44:45] == "A":
			GPSSTATUS = "VALID"
		else:
			GPSSTATUS = "INVALID"
		GPSLASTSTATUSMS = current_milli_time()
	if line.startswith("$GNGGA"):
                #print line
                GPSLAT = line[17:19] + " " + line[19:27] + " " + line[28:29]
                GPSLATNORM = (float(line[17:19]) + float(line[19:27]) / 60.0) * (1 if line[28:29].lower() == "n" else -1)
                GPSLON = line[30:33] + " " + line[33:41] + " " + line[42:43]
                GPSLONNORM = (float(line[30:33]) + float(line[33:41]) / 60.0) * (1 if line[42:43].lower() == "e" else -1)
                GPSTIME = line[7:9] + ":" + line[9:11] + ":" + line[11:16]
		GPSSTATUS = "UNKNOWN"
                GPSLASTSTATUSMS = current_milli_time()
	if line.startswith("$GNRMC") and False:
                #print line
		GPSLAT = line[19:21] + " " + line[21:29] + " " + line[30:31]
                GPSLATNORM = (float(line[19:21]) + float(line[21:29]) / 60.0) * (1 if line[30:31].lower() == "n" else -1)
                GPSLON = line[32:35] + " " + line[35:43] + " " + line[44:45]
                GPSLONNORM = (float(line[32:35]) + float(line[35:43]) / 60.0) * (1 if line[44:45].lower() == "e" else -1)
                GPSTIME = line[7:9] + ":" + line[9:11] + ":" + line[11:16]
                if line[17:18] == "A":
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



