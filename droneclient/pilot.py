#!/usr/bin/env python

import sys, traceback
import threading
import time, datetime, json

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

current_milli_time = lambda: int(time.time() * 1000)



vehicle = None
vehicleLock = threading.RLock()
URL = None
BAUD = None

def lockV():
	vehicleLock.acquire()

def unlockV():
	vehicleLock.release()

def initVehicle():
        global URL
        global BAUD
        global vehicle

	lockV()
	try:
		if vehicle != None:

			#close vehicle
			try:
				vehicle.close()
				vehicle = None
			except Exception as inst:
				vehicle = None

		#open vehicle
		while vehicle == None:
			try:
				vehicle = connect(URL, baud=BAUD, wait_ready=True)

			except Exception as inst:
				vehicle = None
				#traceback.print_exc()
				time.sleep(5)
	finally:
		unlockV()



def pilotMonitor():

	#wait to initialize the pilot
	initVehicle()

	#read loop

	while True:
		try:
			time.sleep(1)
			if vehicle.last_heartbeat > 2:
				#print "REINIT VEHICLE CONNECTION"
				initVehicle()

		except Exception as inst:
			#traceback.print_exc()
			initVehicle()




	
def pilotinit(url, baud):
	global thread
	global URL
	global BAUD
	URL = url
	BAUD = baud
	thread = threading.Thread(target=pilotMonitor)
	thread.daemon = True
	thread.start()


def arm():
	lockV()
	try:
		# Don't let the user try to arm until autopilot is ready
		while not vehicle.is_armable:
			print " Waiting for vehicle to initialise..."
			time.sleep(1)

		print "Arming motors"
		# Copter should arm in GUIDED mode
		vehicle.mode    = VehicleMode("GUIDED")
		vehicle.armed   = True

		while not vehicle.armed:
			print " Waiting for arming..."
			time.sleep(1)

		return "OK"
	finally:
		unlockV()

def simple_takeoff(aTargetAltitude):
	lockV()
	try:
		print "Taking off!"
		vehicle.simple_takeoff(aTargetAltitude)

		# Check that vehicle has reached takeoff altitude
		while True:
			print " Altitude: ", vehicle.location.global_relative_frame.alt

			if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
				print "Reached target altitude"
				break
			time.sleep(1)

		return "OK"
	finally:
		unlockV()




