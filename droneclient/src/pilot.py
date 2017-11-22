#!/usr/bin/env python

import sys, traceback
import threading
import time, datetime, json
#import pilot

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

current_milli_time = lambda: int(time.time() * 1000)



operatingAlt = 20
operatingSpeed = 10
requestedLat = None
requestedLon = None
savedLat = None
savedLon = None

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

		#this doesnt work with pixracer - is_armable stays false
		#while not vehicle.is_armable:
		#	print " Waiting for vehicle to initialise..."
		#	time.sleep(1)
	
		vehicle.mode    = VehicleMode("GUIDED") #pix racer never changes mode to GUIDED
		vehicle.armed   = True
		
		#cancel resume
		savedLat = None
		savedLon = None		
		
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
		
		#cancel resume
		savedLat = None
		savedLon = None		
	
		print " disarming"
		return "OK"	
		
	finally:
		unlockV()


def takeoff(data):

        global vehicle

	lockV()
	try:
	
		aTargetAltitude = operatingAlt

		#request and wait for the arm thread to be armed	
		arm(data)

		print "TAKEOFF"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
			
		vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500}
		
		vehicle.simple_takeoff(float(aTargetAltitude)) # Take off to target altitude
		
		#vehicle._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                #                                  0, 0, 0, 0, 0, 0, 0, float(aTargetAltitude))

		#cancel resume
		savedLat = None
		savedLon = None		
		
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
			
		vehicle.channels.overrides = {}
		
		vehicle.mode = VehicleMode("LAND") #on pixracer this mode is not recognized
		
		#vehicle._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_LAND,
                #                                  0, 0, 0, 0, 0, 0, 0, altitude)

		#cancel last goto		
		savedLat = None
		savedLon = None                
                requestedLat = None
                requestedLon = None
		
		print " landing"
	
		return "OK"

	finally:
		unlockV()

def position(data):

        global vehicle
	global requestedLat
        global requestedLon
        global savedLat
        global savedLon 
        
	lockV()
	try:
		print "POSITION"
			
		vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500}
		vehicle.mode = VehicleMode("LOITER")
		
		#save last goto
		savedLat = requestedLat
		savedLon = requestedLon
		requestedLat = None
		requestedLon = None
		
			
		return "OK"

	finally:
		unlockV()

def resume(data):

        global vehicle
	global requestedLat
        global requestedLon
        global savedLat
        global savedLon 
        
	lockV()
	try:
		print "RESUME"

		if savedLat != None and savedLon != None:
			requestedLat = savedLat
			requestedLon = savedLon
			vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500}
			vehicle.mode = VehicleMode("GUIDED")
			point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), float(operatingAlt))
			vehicle.simple_goto(point1, float(operatingSpeed))
			savedLat = None
			savedLon = None
		
			
		return "OK"

	finally:
		unlockV()

		
def rtl(data):

        global vehicle
        global requestedLat
        global requestedLon        
        
	lockV()
	try:
		print "RTL"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"

		vehicle.channels.overrides = {}
		
                vehicle.mode = VehicleMode("RTL")

		#cancel last goto
		savedLat = None
		savedLon = None                
                requestedLat = None
                requestedLon = None
                
                print " returning home"


		return "OK"

	finally:
		unlockV()
		
		
def goto(data):

        global vehicle
        global operatingAlt
        global requestedLat
        global requestedLon
        
	lockV()
	try:
		print "GOTO"
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
		
		vehicle.mode = VehicleMode("GUIDED")
		
		parameters = data['command']['parameters']
		
		for i in parameters:
			if i['name'] == "lat":
				lat = i['value']
				requestedLat = lat
			if i['name'] == "lon":
				lon = i['value']
				requestedLon = lon
		
		point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), float(operatingAlt))
		vehicle.simple_goto(point1, float(operatingSpeed))

		#cancel resume
		savedLat = None
		savedLon = None

		print " going to "
		return "OK"

	finally:
		unlockV()

		
def alt(data):

        global vehicle
        global operatingAlt
        global requestedLat
        global requestedLon
        
	lockV()
	try:
		print "ALT"
		
		parameters = data['command']['parameters']
		
		for i in parameters:
			if i['name'] == "alt":
				operatingAlt = i['value']
				if requestedLat != None and requestedLon != None:
					#wont work in LOITER mode
					vehicle.mode = VehicleMode("GUIDED")
					point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), float(operatingAlt))
					vehicle.simple_goto(point1, float(operatingSpeed))
		
		print " operating alt is now " + operatingAlt
		return "OK"

	finally:
		unlockV()
		
def speed(data):

        global vehicle
	global operatingSpeed
        
	lockV()
	try:
		print "SPEED"
		
		parameters = data['command']['parameters']
		
		for i in parameters:
			if i['name'] == "speed":
				vehicle.mode = VehicleMode("GUIDED")
				operatingSpeed = i['value']
				vehicle.groundspeed = float(operatingSpeed)
		
		print " operating speed is now " + operatingSpeed
		return "OK"

	finally:
		unlockV()





