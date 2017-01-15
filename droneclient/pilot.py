#!/usr/bin/env python

import sys, traceback
import threading
import time, datetime, json
#import pilot

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

current_milli_time = lambda: int(time.time() * 1000)



vehicle = None
vehicleLock = threading.RLock()
URL = None
BAUD = None


########################### THREAD HELPERS #####################################

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


####################### MAIN THREAD ############################################
def pilotMonitor():

	#wait to initialize the pilot
	initVehicle()

	#read loop

	while True:
		try:
			time.sleep(1)
			if vehicle.last_heartbeat > 5:
				print "REINIT VEHICLE CONNECTION"
				initVehicle()

		except Exception as inst:
			#traceback.print_exc()
			initVehicle()



###################### INIT HANDLER ############################################
	
def pilotinit(url, baud):
	global thread
	global URL
	global BAUD
	URL = url
	BAUD = baud
	thread = threading.Thread(target=pilotMonitor)
	thread.daemon = True
	thread.start()

############################ COMMAND HANDLERS ##################################

def arm(data):

        global vehicle

	lockV()
	try:
		print "ARM"
		
		while not vehicle.is_armable:
			print " Waiting for vehicle to initialise..."
			time.sleep(1)
	
		vehicle.mode    = VehicleMode("GUIDED")
		vehicle.armed   = True
		
		while not vehicle.armed:
			print " Waiting for arming..."
			time.sleep(1)	
		print " armed"	
		
		return "OK"	
		
	finally:
		unlockV()

def disarm(data):

        global vehicle

	lockV()
	try:
		print "DISARM"
			
		vehicle.armed   = False
	
		print " disarming"
		return "OK"	
		
	finally:
		unlockV()


def takeoff(data):

        global vehicle

	lockV()
	try:
	
		aTargetAltitude = 20 #data.operatingAltitude

		#request and wait for the arm thread to be armed	
		arm(data)

		print "TAKEOFF"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
			
		vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
	
		# Check that vehicle has reached takeoff altitude
		#while True:
		#	print " Altitude: ", vehicle.location.global_relative_frame.alt 
		#	if pilot.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95: 
		#		print " Reached target altitude"
		#		break
		#	time.sleep(1)
		
		print " took off"			
			

		return "OK"
	finally:
		unlockV()

def land(data):

        global vehicle
        
	lockV()
	try:
		print "LAND"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
			
		vehicle.mode = VehicleMode("LAND")
		print " landing"
	
		return "OK"

	finally:
		unlockV()

def position(data):

        global vehicle
        
	lockV()
	try:
		print "POSITION"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
			
		return "OK"

	finally:
		unlockV()
		
def rtl(data):

        global vehicle
        
	lockV()
	try:
		print "RTL"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"

		return "OK"

	finally:
		unlockV()
		
		
def goto(data):

        global vehicle
        
	lockV()
	try:
		print "GOTO"
		point1 = LocationGlobalRelative(42.5231211,-71.1877078, 30)
		vehicle.simple_goto(point1)
		return "OK"

	finally:
		unlockV()


