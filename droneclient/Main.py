#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback
import gps, pilot
import command_processor
import argparse


def reportGPSData():
	global unitID

	data = {
		"unitId" : unitID,
		"stateTimestampMS" : gps.current_milli_time(),
		"gpsLatLong" : gps.GPSLAT + " / " + gps.GPSLON,
		"gpsTime" : gps.GPSTIME,
		"gpsStatus" : gps.GPSSTATUS,
		"gpsLastStatusMS" : gps.GPSLASTSTATUSMS,
		"unitCallbackPort" : "8080"
	}

	return data

def reportPilotData():
	global unitID

	if pilot.vehicle == None:
		return None

	data = {
		#1s reporting
		"unitId" : unitID,

		"stateTimestampMS" : pilot.current_milli_time(),
		"gpsLatLon" : "",
		"gpsLat" : pilot.vehicle.location.global_frame.lat if pilot.vehicle.location.global_frame != None else None,
		"gpsLon" : pilot.vehicle.location.global_frame.lon if pilot.vehicle.location.global_frame != None else None,
		"gpsAlt" : pilot.vehicle.location.global_frame.alt if pilot.vehicle.location.global_frame != None else None,

		"homeLatLon" : "",
		"homeLat" : pilot.vehicle.home_location.lat if pilot.vehicle.home_location != None else None,
		"homeLon" : pilot.vehicle.home_location.lon if pilot.vehicle.home_location != None else None,
		"homeAlt" : pilot.vehicle.home_location.alt if pilot.vehicle.home_location != None else None,
		
		"operatingAlt" : pilot.operatingAlt,
		"operatingSpeed" : pilot.operatingSpeed,

		"gpsSpeed" : pilot.vehicle.groundspeed,
		"gpsTime" : "none",
		"gpsStatus" : "none",
		"gpsLastStatusMS" : pilot.current_milli_time() - pilot.vehicle.last_heartbeat,

		"airSpeed" : 0,
		"heading" : pilot.vehicle.heading,
		"baroAlt" : 0,
		"sonarAlt" : 0,
		"status" : pilot.vehicle.system_status.state,

		#5 sec reporting
		"gpsNumSats" : pilot.vehicle.gps_0.satellites_visible,
		"gpsLock" : pilot.vehicle.gps_0.fix_type,
		"gpsHError" : pilot.vehicle.gps_0.eph,
		"gpsVError" : pilot.vehicle.gps_0.epv,

		"currVolts" : pilot.vehicle.battery.voltage,
		"currVoltsLevel" : pilot.vehicle.battery.level,
		"currMah" : pilot.vehicle.battery.current,

		#30 s reporting
                "unitCallbackPort" : "8080"
        }

        return data

if __name__ == '__main__':

	unitID = "drone1"
	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	defHost                    = "http://home.kolesnik.org:9090"
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--connect", default=defHost)
	args = parser.parse_args()

	url = args.connect + "/heartbeat"

	headers = {'Content-Type': content_type_header}

	#initialize gps
	# disabled as now this port is connected to FC
	#gps.gpsinit("/dev/ttyAMA0", 38400)

	#initialize pilot
	pilot.pilotinit("udp:localhost:14550", 115200)


	#initialize command queue
	command_processor.processorinit()

	while True:
		try:
			time.sleep(1)
			#data = reportGPSData()
			data = reportPilotData()
			if data != None:
				response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
			else:
				continue
		except Exception as inst:
			noop = None
			#comment out the following if runnign as daemon
			#traceback.print_exc()
			continue

		try:
			if content != None:
				actions = json.loads(content)
				if actions != None:
					for i in actions:
						command_processor.commandQueue.put(i)

		except Exception as inst:
			noop = None
			traceback.print_exc()

