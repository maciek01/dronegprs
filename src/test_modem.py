#!/usr/bin/env python


import modem,time

modem.modeminit("/dev/ttyUSB3", 38400, 5)

while True:
	print "Status: |" + modem.MODEMSTATUS + "|"
	print "Signal: |" + modem.MODEMSIGNAL + "|"
	print ""
	time.sleep(1)


