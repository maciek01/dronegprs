#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback
import gps
import command_processor

if __name__ == '__main__':

	unitID = "drone1"
	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	host                    = "http://home.kolesnik.org:9090"

	url = host + "/heartbeat"

	headers = {'Content-Type': content_type_header}

	#initialize gps
	# disabled as now this port is connected to FC
	#gps.gpsinit("/dev/ttyAMA0", 38400)

	#initialize command queue
	command_processor.processorinit()


	while True:
		try:
			time.sleep(1)
			data = {
				"unitId" : unitID,
				"stateTimestampMS" : gps.current_milli_time(),
				"gpsLatLong" : gps.GPSLAT + " / " + gps.GPSLON,
				"gpsTime" : gps.GPSTIME,
				"gpsStatus" : gps.GPSSTATUS,
				"gpsLastStatusMS" : gps.GPSLASTSTATUSMS,
				"unitCallbackPort" : "8080"
			}

			response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
		except Exception as inst:
			noop = None
			#traceback.print_exc()
			continue

		try:
			if content != None:
				commands = json.loads(content)
				for i in commands:
					command_processor.commandQueue.put(i)

		except Exception as inst:
			noop = None
			traceback.print_exc()

