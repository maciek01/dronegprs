#!/usr/bin/env python

import sys, traceback
import serial, threading
import time, datetime
import os.path, csv
import command_processor


##########################################################################

#external status
MODEMSTATUS = "OFF"
MODEMSIGNAL = "NONE"
LASTRESULT = ""
TESTRESULT = False

#active flag
readOn = False

#modem response handling
buffer = ""
getLine = ""

#threads
rx_thread = None
tx_thread = None

#dont read and write from the same port at the same time - needed??
portLock = threading.RLock()

#ready for SMS message content
expect_body = False

#MT message response to be sent to requestor
resp = None

#pilot state
pilotData = None

#MT structure - constants
mt_idx = 0
mt_status = 1
mt_src_addr = 2
mt_fill = 3
mt_date = 4

#MT header
mt_header = None

#modem port
serialPort = None

#time
current_milli_time = lambda: int(time.time() * 1000)


#####################################################################################

def lockP():
        portLock.acquire()

def unlockP():
        portLock.release()

def strip00(line):
	index00 = line.find("00")
	while index00 != -1:
		line = line[:index00] + line[index00+2:]
		index00 = line.find("00")

	return line

def hex2ascii(line):
	return line.decode("hex")
		

def handle_newline(line):

	global MODEMSTATUS
	global MODEMSIGNAL
	global LASTRESULT
	global TESTRESULT
	global expect_body
	global resp
	global mt_header


	MODEMSTATUS = "ON"
	LASTRESULT = line

	print line
	if expect_body:
		mt_body = line

		if mt_body.startswith("00"):
			mt_body = strip00(mt_body)
			mt_body = hex2ascii(mt_body)
			print mt_body

		mt_body = mt_body.lower().strip()

		expect_body = False
		newResp = []
		bodyHandled = False

		if not bodyHandled and mt_header[mt_status] == "REC READ":
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r")
			bodyHandled = True


		if not bodyHandled and mt_body.startswith("stat"):
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r")
			msg_parts = splitMsg(smsStatus())
			for part in msg_parts:
				newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r")
				newResp.append(part + chr(26))
			bodyHandled = True
		if not bodyHandled and mt_body.startswith("rtl"):
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r")
			newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r")
			newResp.append("rtl received" + chr(26))
			bodyHandled = True

			action = {
				"unitId": "",
				"command": {
					"name": "RTL",
					"parameters": []
				}
			}

			command_processor.commandQueue.put(action)

		if not bodyHandled:
			newResp.append("AT+CMGD=" + mt_header[mt_idx] + "\r")
			newResp.append("AT+CMGS=\"" + mt_header[mt_src_addr] + "\"\r")
			newResp.append("valid commands: stat, rtl, help" + chr(26))
			bodyHandled = True


		if len(newResp) != 0:
			resp = newResp

	else:	#not expect_body
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
		if "mode" not in data:
			res = res + "no FC data\r"
		else:
			res = res + "mode:" + str(data["mode"]) + "/" + str(data["status"]) + "\r"
			res = res + "bat V:" + str(data["currVolts"]) + "\r"
			res = res + "bat mAh:" + str(data["currTotmAh"]) + "\r"
			res = res + "bat Curr:" + str(data["currA"]) + "\r"
	res = res + "GSM SIGNAL:" + MODEMSIGNAL
	if data != None and "message" in data:
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


#reader thread
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
		except IOError as inst: #this handling is wrong - reinit the whole process instead
			MODEMSTATUS = "OFF"
			traceback.print_exc()
			time.sleep(5)
			try:
				ser.close()
			except Exception as inst:
				traceback.print_exc()
			openSerial(modemport, modembaud, False)
			ser = serialPort
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

#writter thread
def get_status(sleepS):
	global readOn
	global serialPort
	global resp

	while serialPort == None and readOn:
		time.sleep(sleepS)

	print("connected TX")
	initSMS(serialPort)

	while readOn:
		try:
			time.sleep(sleepS)

			if resp != None:
				sendRESP()
				resp = None

			#sendSigReq(serialPort) #this is now automatic
			sendInboxReq(serialPort)


		except Exception as inst:
			initSMS(serialPort) #reinitialize sms
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
		ser.write("AT+CMGF=1\r") #text format
		flushPort(ser)
		time.sleep(0.5)
		ser.write("AT+CGSMS=1\r")
		flushPort(ser)
		time.sleep(0.5)
		ser.write("AT+CSMP=17,167,0,242\r") #flash/regular message
		flushPort(ser)
		time.sleep(0.5)
		ser.write("AT+AUTOCSQ=1,0\r") #request signal update every 5 secs
		flushPort(ser)
		time.sleep(0.5)
	finally:
		unlockP()

def sendInboxReq(ser):
	lockP()
	try:
		ser.write("AT+CMGL=\"ALL\"\r") #examine inbox
		flushPort(ser)
		time.sleep(0.5)
	finally:
		unlockP()

def sendSigReq(ser):
	lockP()
	try:
		ser.write("AT+CSQ\r")
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

	serialPort.write("AT+CPIN?\r")
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

        while not os.path.isfile("/home/pi/modemup"):   #create file by hand to break the loop
                time.sleep(1)

        if not os.path.isfile("/home/pi/modemup"):
                return False


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




