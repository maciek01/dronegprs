#!/usr/bin/env python

import Queue
import json
import time
import datetime
import sys, traceback
import threading

commandQueue = Queue.Queue()

thread = None

def none(data):
	print "NONE"

def takeoff(data):
	print "TAKEOFF"

def land(data):
	print "LAND"

def rtl(data):
	print "RTL"


commands = {
	None : none,
	"" : none,
	"NONE" : none,
	"TAKEOFF" : takeoff,
	"LAND" : land,
	"RTL" : rtl
}


def processCommands():

        global commandQueue

        while True:
                try:
			command = commandQueue.get()
			commands[command['name']](command)

                except Exception as inst:
                        noop = None
                        traceback.print_exc()


def processorinit():
        global thread
        thread = threading.Thread(target=processCommands)
        thread.daemon = True
        thread.start()


