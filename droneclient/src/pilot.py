#!/usr/bin/env python

import sys, traceback
import threading
import time, datetime, json
#import pilot

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
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
		releaseSticks()
		
		#cancel resume
		savedLat = None
		savedLon = None		
		
		i = 0
		while not vehicle.armed and i < 30:
			print " Waiting for arming..."
			time.sleep(1)	
			i = i + 1
			
		if not vehicle.armed:
			vehicle.armed   = False
			print " failed to arm"
			return "ERROR"
		else:
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
		releaseSticks()
		
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
			
		vehicle.simple_takeoff(int(aTargetAltitude)) # Take off to target altitude
		#vehicle._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
		#				  0, 0, 0, 0, 0, 0, 0, int(aTargetAltitude))
		releaseSticks()

		#cancel resume
		savedLat = None
		savedLon = None		
		
		print " took off"			
			

		return "OK"
	finally:
		unlockV()

def land(data):

	global vehicle
	global requestedLat
	global requestedLon
	global savedLat
	global savedLon
	
	lockV()
	try:
		print "LAND"
		#if not vehicle.armed:
			#print " NOT ARMED"
			#return "ERROR: NOT ARMED"
			
		vehicle.mode = VehicleMode("LAND")
		releaseSticks()
		
		#vehicle._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_LAND,
		#				  0, 0, 0, 0, 0, 0, 0, altitude)

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
			
		centerSticks()
		vehicle.mode = VehicleMode("POSHOLD")
		
		#save last goto
		savedLat = requestedLat
		savedLon = requestedLon
		requestedLat = None
		requestedLon = None
		
			
		return "OK"

	finally:
		unlockV()
		

def loiter(data):

	global vehicle
	global requestedLat
	global requestedLon
	global savedLat
	global savedLon 
	
	lockV()
	try:
		print "LOITER"
			
		centerSticks()
		vehicle.mode = VehicleMode("LOITER")
		
		#save last goto
		savedLat = requestedLat
		savedLon = requestedLon
		requestedLat = None
		requestedLon = None
		
			
		return "OK"

	finally:
		unlockV()		

def pause(data):

	global vehicle
	global operatingAlt
	global operatingSpeed
	global requestedLat
	global requestedLon
	global savedLat
	global savedLon 
	
	lockV()
	try:
		print "PAUSE"
			
		if not vehicle.armed:
			print " NOT ARMED"
			return "ERROR: NOT ARMED"
		
		
		if vehicle.location.global_frame != None:		
			vehicle.mode = VehicleMode("GUIDED")
			releaseSticks()
			#save last goto
			savedLat = requestedLat
			savedLon = requestedLon
			#stop here
			requestedLat = vehicle.location.global_frame.lat
			requestedLon = vehicle.location.global_frame.lon
			point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), int(operatingAlt))
			vehicle.simple_goto(point1, int(operatingSpeed))
	

			
		
			
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
			vehicle.mode = VehicleMode("GUIDED")
			point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), int(operatingAlt))
			vehicle.simple_goto(point1, int(operatingSpeed))
			savedLat = None
			savedLon = None
			releaseSticks()
		
			
		return "OK"

	finally:
		unlockV()

#release channel overrides
def manual(data):

	global vehicle
	
	lockV()
	try:
		print "MANUAL"
		vehicle.mode = VehicleMode("POSHOLD")
		releaseSticks()
		return "OK"

	finally:
		unlockV()

def reHome(data):
	global vehicle
	
	lockV()
	try:
		print "REHOME"
		vehicle.home_location=vehicle.location.global_frame
		return "OK"

	finally:
		unlockV()
		
def rtl(data):

	global vehicle
	global requestedLat
	global requestedLon
	global savedLat
	global savedLon	   
	
	lockV()
	try:
		print "RTL"
		#if not vehicle.armed:
			#print " NOT ARMED"
			#return "ERROR: NOT ARMED"

		vehicle.mode = VehicleMode("RTL")
		releaseSticks()

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
		
		point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), int(operatingAlt))
		vehicle.simple_goto(point1, int(operatingSpeed))
		releaseSticks()

		#cancel resume
		savedLat = None
		savedLon = None

		print " going to "
		return "OK"

	finally:
		unlockV()

def setHome(data):
	global vehicle
	lockV()
	try:
		print "SETHOME"
		
		parameters = data['command']['parameters']
		
		for i in parameters:
			if i['name'] == "lat":
				lat = i['value']
			if i['name'] == "lon":
				lon = i['value']
		
		point1 = LocationGlobal(float(lat), float(lon), vehicle.home_location.alt)
		if vehicle.home_location != None:
			vehicle.home_location=point1

		return "OK"

	finally:
		unlockV()

		
def alt(data):

	global vehicle
	global operatingAlt
	global requestedLat
	global requestedLon
	global operatingSpeed
	
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
					point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), int(operatingAlt))
					vehicle.simple_goto(point1, int(operatingSpeed))
		
		print " operating alt is now " + operatingAlt
		return "OK"

	finally:
		unlockV()
		
def altAdjust(delta):

	global vehicle
	global operatingAlt
	global requestedLat
	global requestedLon
	global operatingSpeed
	
	lockV()
	try:
		operatingAlt = str(max(int(operatingAlt) + delta, 0))
		
		
		if requestedLat != None and requestedLon != None:
			#wont work in LOITER mode
			vehicle.mode = VehicleMode("GUIDED")
			point1 = LocationGlobalRelative(float(requestedLat), float(requestedLon), int(operatingAlt))
			vehicle.simple_goto(point1, int(operatingSpeed))
		
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
				vehicle.groundspeed = int(operatingSpeed)
		
		print " operating speed is now " + operatingSpeed
		return "OK"

	finally:
		unlockV()
		
def speedAdjust(delta):
	global vehicle
	global operatingSpeed
	
	lockV()
	try:
		operatingSpeed = str(max(min(int(operatingSpeed) + delta, 15), 1))
		vehicle.groundspeed = int(operatingSpeed)
		
		print " operating speed is now " + operatingSpeed
		
		return "OK"

	finally:
		unlockV()

def decAlt1(data):
	print "DECALT1"
	return altAdjust(-1)
	
def decAlt10(data):
	print "DECALT10"
	return altAdjust(-10)
	
def incAlt10(data):
	print "INCALT10"
	return altAdjust(10)
	
def incAlt1(data):
	print "INCALT1"
	return altAdjust(1)
	
def decSpeed1(data):
	print "DECSPEED1"
	return speedAdjust(-1)
	
def decSpeed10(data):
	print "DECSPEED10"
	return speedAdjust(-10)
	
def incSpeed10(data):
	print "INCSPEED10"
	return speedAdjust(10)
	
def incSpeed1(data):
	print "INCSPEED1"
	return speedAdjust(1)


#override channels - center 
def centerSticks():
	global vehicle
	vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500}
	
#remove channel overrides
def releaseSticks():
	global vehicle
	vehicle.channels.overrides = {}
	


