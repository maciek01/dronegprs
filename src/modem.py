#!/usr/bin/env python

import sys, traceback
import serial, threading
import time, datetime
import os.path, csv



readOn = False

buffer = ""
getLine = ""

rx_thread = None
tx_thread = None

MODEMSTATUS = "OFF"
MODEMSIGNAL = "NONE"
LASTRESULT = ""
TESTRESULT = False
EXPECT_BODY = False

mt_idx = 0
mt_status = 1
mt_src_addr = 2
mt_fill = 3
mt_date = 4

mt_header = [None,None,None,None,None]
mt_body = None


serialPort = None

current_milli_time = lambda: int(time.time() * 1000)

def handle_newline(line):

	global MODEMSTATUS
	global MODEMSIGNAL
	global LASTRESULT
	global TESTRESULT
	global EXPECT_BODY

	global mt_header
	global mt_body


	MODEMSTATUS = "ON"
	LASTRESULT = line

	if EXPECT_BODY:
		mt_body = line
		EXPECT_BODY = False
		print mt_body
	if line.startswith("+CSQ:"):
		MODEMSIGNAL = line[6:]
	if line.startswith("+CPIN: READY"):
		TESTRESULT = True
	if line.startswith("+CMGL: "):
		reader = csv.reader(line[7:].split('\n'), delimiter=',')
		idx = 0
		for row in reader:
			mt_header[idx] = row
			idx = idx + 1
		EXPECT_BODY = True
		print mt_header
	if line.startswith("+CMGR: "):
                reader = csv.reader(line[7:].split('\n'), delimiter=',')
                idx = 1
                for row in reader:
			mt_header[idx] = row
			idx = idx + 1
		EXPECT_BODY = True


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

def openSerial(modemport, modembaud, quiet):
	global serialPort

	serialPort = None
	try:
		serialPort = serial.Serial(modemport, baudrate=modembaud, timeout=None)
	except Exception as inst:
		serialPort = None
		if not quiet:
			traceback.print_exc()


def read_from_port(modemport, modembaud):
	global readOn
	global serialPort
	global MODEMSTATUS
	global MODEMSIGNAL

	time.sleep(5)

	while readOn and not os.path.isfile("/home/pi/modemup"):
		time.sleep(1)

	#wait to initialize the port
	while serialPort == None and readOn:
		openSerial(modemport, modembaud, False)
		if serialPort == None:
			MODEMSTATUS = "OFF"
			MODEMSIGNAL = "NONE"
			time.sleep(5)

	print("connected RX")

	#read loop
	ser = serialPort

	while readOn and ser != None:
		try:
			if ser.inWaiting() > 0:
				handle_data(ser.read(ser.inWaiting()))
			MODEMSTATUS = "ON"
			time.sleep(1)
		except Exception as inst:
			MODEMSTATUS = "OFF"
			traceback.print_exc()
			time.sleep(5)

	try:
		ser.close()
	except Exception as inst:
		traceback.print_exc()

	serialPort = None
	print("disconnected RX")
	MODEMSTATUS = "OFF"

def get_status(sleepS):
        global readOn
        global serialPort

	while serialPort == None and readOn:
		time.sleep(sleepS)

	print("connected TX")
	serialPort.write("AT+CMGF=1\r\n")
	time.sleep(1)
	serialPort.write("AT+CGSMS=1\r\n")
	time.sleep(1)
	serialPort.write("AT+CSMP=17,167,0,242\r\n") #flash message
	time.sleep(1)
        serialPort.write("AT+CMGL=\"ALL\"\r\n") #examine inbox


	while readOn:
		try:	
			time.sleep(sleepS)
			serialPort.write("AT+CSQ\r\n")
                except Exception as inst:
                        traceback.print_exc()
	print("disconnected TX")

def isModem(port, baud):

	global serialPort
	global TESTRESULT

        while not os.path.isfile("/home/pi/modemup"):   #create file by hand to break the loop
                time.sleep(1)

	if not os.path.isfile("/home/pi/modemup"):
		return False

	openSerial(port, baud, True)

	if serialPort == None:
		return False

	serialPort.write("AT+CPIN?\r\n")
	cnt = 0
	while cnt < 5:
                try:
			time.sleep(1)
			cnt = cnt + 1
                        if serialPort.inWaiting() > 0:
                                handle_data(serialPort.read(serialPort.inWaiting()))
                except Exception as inst:
                        traceback.print_exc()

	serialPort.close()
	serialPort = None

	return TESTRESULT

def findModem(ports, baud):
	for port in ports:
		if isModem(port, baud):
			return port

	return ""




	
def modeminit(modemport, modembaud, sleepS, isMonitor):
	global rx_thread
	global tx_thread
	global readOn

	readOn = True

	rx_thread = threading.Thread(target=read_from_port, args=(modemport,modembaud,))
	rx_thread.daemon = True
	rx_thread.start()

	if isMonitor:
		tx_thread = threading.Thread(target=get_status, args=(sleepS,))
		tx_thread.daemon = True
		tx_thread.start()


def modemstop():
	global readOn
	global tx_thread
	global rx_thread

	readOn = False

	if rx_thread != None:
		try:
			rx_thread.join()
		except Exception as inst:
			traceback.print_exc()
		rx_thread = None

	if tx_thread != None:
		try:
			tx_thread.join()
		except Exception as inst:
			traceback.print_exc()
		tx_thread = None




