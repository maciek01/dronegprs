#!/usr/bin/env python

import Queue
import json
import time
import datetime
import sys, traceback
import threading

from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

import pilot


commandQueue = Queue.Queue()

thread = None

isArmed = False

def none(data):
	print "NONE"

def takeoff(data):
	global isArmed
	
	arm(data, block=True)
	print "TAKEOFF"
	if not pilot.vehicle.armed:
		print "NOT ARMED!!"
		return	
		
	pilot.vehicle.simple_takeoff(50) # Take off to target altitude

	# Check that vehicle has reached takeoff altitude
	#while True:
	#	print " Altitude: ", pilot.vehicle.location.global_relative_frame.alt 
	#	if pilot.vehicle.location.global_relative_frame.alt >= 50 * 0.95: 
	#		print " Reached target altitude"
	#		break
	#	time.sleep(1)
	
	print " tookoff"

def land(data):
	global isArmed
	
	print "LAND"
	if not pilot.vehicle.armed:
		print "NOT ARMED!!"
		return
		
	pilot.vehicle.mode = VehicleMode("LAND")
	print " landing"

def rtl(data):
	global isArmed
	
	print "RTL"
	if not pilot.vehicle.armed:
		print "NOT ARMED!!"
		return

def arm(data, block=False):
	global isArmed
	
	print "ARM"
	
	while not pilot.vehicle.is_armable:
		print " Waiting for vehicle to initialise..."
		time.sleep(1)

	pilot.vehicle.mode    = VehicleMode("GUIDED")
	pilot.vehicle.armed   = True
	
	if not block:
		return

	while not pilot.vehicle.armed:
		print " Waiting for arming..."
		time.sleep(1)	
	isArmed = True
	print " armed"
	

def disarm(data):
	global isArmed
	
	print "DISARM"
		
	pilot.vehicle.armed   = False

	print " disarming"

def position(data):
	global isArmed
	
	print "POSITION"
	if not pilot.vehicle.armed:
		print "NOT ARMED!!"
		return
		
		
def goto(data):

	print "GOTO"
	point1 = LocationGlobalRelative(42.5231211,-71.1877078, 30)
	vehicle.simple_goto(point1)


actions = {
	None : none,
	"" : none,
	"NONE" : none,
	"ARM" : arm,
	"DISARM" : disarm,
	"POSITION" : position,
	"TAKEOFF" : takeoff,
	"LAND" : land,
	"RTL" : rtl,
	"GOTO" : goto
}


def processCommands():

        global commandQueue

        while True:
                try:
			action = commandQueue.get()
			actions[action['command']['name']](action)

                except Exception as inst:
                        noop = None
                        traceback.print_exc()


def processorinit():
        global thread
        thread = threading.Thread(target=processCommands)
        thread.daemon = True
        thread.start()


