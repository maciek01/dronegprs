#!/usr/bin/env python

import sys, traceback
import serial, threading
import time, datetime
import os.path, csv

#external status

MODEMSTATUS = "OFF"
MODEMSIGNAL = "NONE"
LASTRESULT = ""
TESTRESULT = False

readOn = False


buffer = ""
getLine = ""

rx_thread = None
tx_thread = None

portLock = threading.RLock()

expect_body = False
resp = None

pilotData = None

mt_idx = 0
mt_status = 1
mt_src_addr = 2
mt_fill = 3
mt_date = 4

mt_header = None
mt_body = None


serialPort = None

current_milli_time = lambda: int(time.time() * 1000)


def lockP():
        portLock.acquire()

def unlockP():
        portLock.release()

def handle_newline(line):

	global MODEMSTATUS
	global MODEMSIGNAL
	global LASTRESULT
	global TESTRESULT
	global expect_body
	global resp

	global mt_header
	global mt_body


	MODEMSTATUS = "ON"
	LASTRESULT = line

	print line
	if expect_body:
		mt_body = line
		expect_body = False
		newResp = []
		if mt_body.lower().strip().startswith("stat") and mt_header[mt_status] == "REC UNREAD":
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r\n")
			msg_parts = splitMsg(smsStatus())
			for part in msg_parts:
				newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r\n")
				newResp.append(part + chr(26))
		if mt_body.lower().strip().startswith("stat") and mt_header[mt_status] == "REC READ":
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r\n")
		if not mt_body.lower().strip().startswith("stat"):
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r\n")
			newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r\n")
			newResp.append("Valid commands: stat rtl help" + chr(26))
			msg_parts = splitMsg(smsStatus())
			for part in msg_parts:
                                newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r\n")
                                newResp.append(part + chr(26))


		if len(newResp) != 0:
			resp = newResp

	if line.startswith("+CSQ:"):
		MODEMSIGNAL = line[6:]

	if line.startswith("+CPIN: READY"):
		TESTRESULT = True

	if line.startswith("+CMGL: "):
		reader = csv.reader(line[7:].split('\n'), delimiter=',')
		for row in reader:
			mt_header = row
		expect_body = True


def splitMsg(msg):
	maxLen = 120

	lines = msg.split('\r')
	sms = ""
	newMsgs = []
	for item in lines:

		if len(sms) != 0 and len(sms) + len(item) + 1 > maxLen:
			newMsgs.append(sms[:maxLen])
			sms = item[:maxLen]
		else:
			sms = sms + ('\r' if sms != "" else '') + item[:maxLen]
	if sms != "":
		newMsgs.append(sms[:maxLen])
		sms = ""

	return newMsgs



def smsStatus():
	global MODEMSIGNAL
	global pilotData

	res = ""

	data = pilotData

	if data != None:
		res = res + "gps Lat:" + str(data["gpsLat"]) + "\r"
		res = res + "gps Lon:" + str(data["gpsLon"]) + "\r"
		res = res + "gps Alt:" + str(data["gpsAlt"]) + "\r"
		res = res + "gps Speed:" + str(data["gpsSpeed"]) + "\r"
		res = res + "gps Sats:" + str(data["gpsNumSats"]) + "\r"
		res = res + "heading:" + str(data["heading"]) + "\r"
		res = res + "bat V:" + str(data["currVolts"]) + "\r"
		res = res + "bat mAh:" + str(data["currTotmAh"]) + "\r"
		res = res + "bat Curr:" + str(data["currA"]) + "\r"
	res = res + "GSM SIGNAL:" + MODEMSIGNAL
	if data != None:
		res = res + "\rlast msg:" + str(data["message"]) + "\r"

	return res




def handle_data(data):
	global buffer
	global getLine
	for d in data:
		if d == '\n':
			getLine = buffer
			buffer = ""
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
			lockP()
			try:
				if ser.inWaiting() > 0:
					handle_data(ser.read(ser.inWaiting()))
			finally:
				unlockP()
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
	global resp

	while serialPort == None and readOn:
		time.sleep(sleepS)

	print("connected TX")
	initSMS(serialPort)

	cnt = 0 # use ERROR response check
	while readOn:
		try:
			time.sleep(sleepS)

			if resp != None:
				sendRESP()
				resp = None

			sendSigReq(serialPort)
			sendInboxReq(serialPort)

			cnt = cnt + 1
			if cnt % 10 == 0:
				cnt = 0
				initSMS(serialPort) #reinitialize sms

                except Exception as inst:
                        traceback.print_exc()

	print("disconnected TX")

def sendRESP():
	for line in resp:
		lockP()
		try:
			serialPort.write(line)
			flushPort(serialPort)
			time.sleep(2)
				
		finally:
			unlockP()


def flushPort(ser):
	ser.flush()

def initSMS(ser):
	lockP()
	try:
		ser.write("AT+CMGF=1\r\n")
		flushPort(ser)
		time.sleep(0.5)
		ser.write("AT+CGSMS=1\r\n")
		flushPort(ser)
		time.sleep(0.5)
		ser.write("AT+CSMP=17,167,0,242\r\n") #flash message
		flushPort(ser)
		time.sleep(0.5)
	finally:
		unlockP()

def sendInboxReq(ser):
	lockP()
	try:
		ser.write("AT+CMGL=\"ALL\"\r\n") #examine inbox
		flushPort(ser)
		time.sleep(0.5)
	finally:
		unlockP()

def sendSigReq(ser):
	lockP()
	try:
		ser.write("AT+CSQ\r\n")
		flushPort(ser)
		time.sleep(0.5)
	finally:
		unlockP()

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




