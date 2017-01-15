#!/usr/bin/env python

import Queue
import json
import time
import datetime
import sys, traceback
import threading

import pilot


commandQueue = Queue.Queue()

thread = None

########################## ACTION HANDLERS #####################################

def none(data):
	print "NONE"

def takeoff(data):
	return pilot.takeoff(data)

def land(data):
	return pilot.land(data)

def rtl(data):
	return pilot.rtl(data)	

def arm(data):
	return pilot.arm(data)	

def disarm(data):
	return pilot.disarm(data)	

def position(data):
	return pilot.position(data)	
		
def goto(data):
	return pilot.goto(data)

######################### ACTIONS ##############################################

actions = {
	None : none,
	"" : none,
	"NONE" : none,
	"ARM" : arm,
	"DISARM" : disarm,
	"TAKEOFF" : takeoff,
	"LAND" : land,
	"POSITION" : position,
	"RTL" : rtl,
	"GOTO" : goto
}

################################# MAIN THREAD ##################################
def processCommands():

        global commandQueue

        while True:
                try:
			action = commandQueue.get()
			result = actions[action['command']['name']](action)

                except Exception as inst:
                        noop = None
                        traceback.print_exc()

################################ INIT ##########################################

def processorinit():
        global thread
        thread = threading.Thread(target=processCommands)
        thread.daemon = True
        thread.start()


