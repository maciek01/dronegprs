#!/usr/bin/env python


import gps,time

gps.gpsinit("/dev/serial0", 38400)

while True:
	print "Lat/Lon: " + gps.GPSLAT + " / " + gps.GPSLON
	print "Time UTC: " + gps.GPSTIME
	print "Status: " + gps.GPSSTATUS
	print "Status ts: ", gps.GPSLASTSTATUSMS
	print ""
	time.sleep(1)


