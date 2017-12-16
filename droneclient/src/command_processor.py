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
	
def pause(data):
	return pilot.pause(data)
	
def resume(data):
	return pilot.resume(data)
	
def loiter(data):
	return pilot.loiter(data)
	
def manual(data):
	return pilot.manual(data)
		
def goto(data):
	return pilot.goto(data)

def alt(data):
	return pilot.alt(data)
	
def speed(data):
	return pilot.speed(data)	

def decAlt1(data):
	return pilot.decAlt1(data)
	
def decAlt10(data):
	return pilot.decAlt10(data)
	
def incAlt10(data):
	return pilot.incAlt10(data)
	
def incAlt1(data):
	return pilot.incAlt1(data)
	
def decSpeed1(data):
	return pilot.decSpeed1(data)
	
def decSpeed10(data):
	return pilot.decSpeed10(data)
	
def incSpeed10(data):
	return pilot.incSpeed10(data)
	
def incSpeed1(data):
	return pilot.incSpeed1(data)

def setHome(data):
	return pilot.setHome(data)

def reHome(data):
	return pilot.reHome(data)

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
	"PAUSE" : pause,
	"RESUME" : resume,
	"MANUAL" : manual,
	"LOITER" : loiter,
	"RTL" : rtl,
	"REHOME" : reHome,
	"SETHOME" : setHome,
	"GOTO" : goto,
	"ALT" : alt,
	"SPEED" : speed,
	"DECALT1" : decAlt1,
	"DECALT10" : decAlt10,
	"INCALT10" : incAlt10,
	"INCALT1" : incAlt1,
	"DECSPEED1" : decSpeed1,
	"DECSPEED10" : decSpeed10,
	"INCSPEED10" : incSpeed10,
	"INCSPEED1" : incSpeed1
}

################################# MAIN THREAD ##################################
def processCommands():

        global commandQueue
        global actions

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


