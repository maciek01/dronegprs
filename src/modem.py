#!/usr/bin/env python

import sys, traceback
import serial, threading
import time, datetime



readOn = True

buffer = ""
getLine = ""

rx_thread = None
tx_thread = None

MODEMSTATUS = "OFF"
MODEMSIGNAL = "NONE"

serialPort = None

current_milli_time = lambda: int(time.time() * 1000)

def handle_newline(line):

	global MODEMSTATUS
	global MODEMSIGNAL

	MODEMSTATUS = "ON"
	if line.startswith("+CSQ:"):
		MODEMSIGNAL = line[6:]


def handle_data(data):
	global buffer
	global getLine
	for d in data:
		if d == '\n':
			getLine = buffer
			buffer = ""
			#print ("modem RX=",getLine)
			handle_newline(getLine)
		elif d != '\r':
			buffer = buffer + str(d)

def read_from_port(modemport, modembaud):
	global readOn
	global serialPort
	global MODEMSTATUS
	global MODEMSIGNAL

	#wait to initialize the port
	while serialPort == None:
		try:
			serialPort = serial.Serial(modemport, baudrate=modembaud, timeout=None)
		except Exception as inst:
			serialPort = None
			traceback.print_exc()
			MODEMSTATUS = "OFF"
			MODEMSIGNAL = "NONE"
			time.sleep(5)

	print("connected RX")
	MODEMSTATUS = "ON"

	#read loop
	ser = serialPort
	while readOn:
		try:
			if ser.inWaiting() > 0:
				handle_data(ser.read(ser.inWaiting()))
		except Exception as inst:
			traceback.print_exc()
			time.sleep(5)

def get_status(sleepS):
        global readOn
        global serialPort

	while serialPort == None:
		time.sleep(sleepS)

	print("connected TX")
	while readOn:
		time.sleep(sleepS)
		serialPort.write("AT+CSQ\r\n")

	
def modeminit(modemport, modembaud, sleepS):
	global rx_thread
	global tx_thread
	rx_thread = threading.Thread(target=read_from_port, args=(modemport,modembaud,))
	rx_thread.daemon = True
	rx_thread.start()

        tx_thread = threading.Thread(target=get_status, args=(sleepS,))
        tx_thread.daemon = True
        tx_thread.start()



