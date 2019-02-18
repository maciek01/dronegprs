#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback
import gps, pilot, modem
import command_processor
import argparse


globalData = None


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
		"gpsAltRel" : pilot.vehicle.location.global_relative_frame.alt if pilot.vehicle.location.global_relative_frame != None else None,

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

		"airSpeed" : pilot.vehicle.airspeed,
		"heading" : pilot.vehicle.heading,
		"baroAlt" : pilot.vehicle.rangefinder.distance if pilot.vehicle.rangefinder != None else 0,
		"sonarAlt" : pilot.vehicle.rangefinder.distance if pilot.vehicle.rangefinder != None else 0,
		"lidarAlt" : pilot.vehicle.rangefinder.distance if pilot.vehicle.rangefinder != None else 0,
		"status" : pilot.vehicle.system_status.state,
		"mode" : pilot.vehicle.mode.name,
		"armed" : pilot.vehicle.armed,

		#5 sec reporting
		"gpsNumSats" : pilot.vehicle.gps_0.satellites_visible,
		"gpsLock" : pilot.vehicle.gps_0.fix_type,
		"gpsHError" : pilot.vehicle.gps_0.eph,
		"gpsVError" : pilot.vehicle.gps_0.epv,

		#"gps2NumSats" : pilot.vehicle.gps_1.satellites_visible if pilot.vehicle.gps_1 != None else None,
		#"gps2Lock" : pilot.vehicle.gps_1.fix_type if pilot.vehicle.gps_1 != None else None,
		#"gps2HError" : pilot.vehicle.gps_1.eph if pilot.vehicle.gps_1 != None else None,
		#"gps2VError" : pilot.vehicle.gps_1.epv if pilot.vehicle.gps_1 != None else None,

		"currVolts" : pilot.vehicle.battery.voltage,
		"currVoltsLevel" : pilot.vehicle.battery.level,
		"currA" : pilot.vehicle.battery.current,
		"currTotmAh" : pilot.curr_tot,
		"voltages" : pilot.voltages,

		"modemstatus" : modem.MODEMSTATUS,
		"modemsignal" : modem.MODEMSIGNAL,

		"message" : pilot.statusMessage,
		"messageSev" : pilot.statusSev,

		#30 s reporting
		"unitCallbackPort" : "8080"
		}

	return data

if __name__ == '__main__':

	print "STARTING MAIN MODULE"

	unitID = "drone1"
	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	defHost                    = "http://home.kolesnik.org:8000"
	content = None
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--connect", default=defHost)
	args = parser.parse_args()

	url = args.connect + "/uavserver/v1/heartbeat"

	headers = {'Content-Type': content_type_header}

	#initialize gps
	# disabled as now this port is connected to FC
	#gps.gpsinit("/dev/serial0", 38400)

	#initialize modem monitor
	firstModem = modem.findModem([
		"/dev/ttyUSB0",
		"/dev/ttyUSB1",
		"/dev/ttyUSB2",
		"/dev/ttyUSB3",
		"/dev/ttyUSB4",
		"/dev/ttyUSB5",
		"/dev/ttyUSB6"], 38400)
	if firstModem != "":
		print("Monitoring modem " + firstModem)
		modem.modeminit(firstModem, 57600, 5, True)

	print "STARTING PILOT MODULE"
	#initialize pilot
	pilot.pilotinit("udp:localhost:14550", 57600)
	#pilot.pilotinit("udpbcast:192.168.2.255:14550", 57600)
	#pilot.pilotinit("udpin:0.0.0.0:14550", 57600)
	#pilot.pilotinit("/dev/pts/2", 57600)


	print "STARTING COMMAND PROCESSOR MODULE"
	#initialize command queue
	command_processor.processorinit()

	#wait for vehicel connection
	while pilot.vehicle == None:
		time.sleep(1)

	# Get Vehicle Home location - will be `None` until first set by autopilot
	while pilot.vehicle.home_location == None:
		cmds = pilot.vehicle.commands
		cmds.download()
		cmds.wait_ready()
		if pilot.vehicle.home_location == None:
			print " Waiting for home location ..."
			time.sleep(1)
			try:
				data = reportPilotData()
				globalData = data
				modem.pilotData = data
				if data != None:
					http.request( url, 'POST', json.dumps(data), headers=headers)
				else:
					continue
			except Exception as inst:
				noop = None
				#comment out the following if runnign as daemon
				traceback.print_exc()
				continue


	# We have a home location.
	print "\n Home location: %s" % pilot.vehicle.home_location

	print "STARTING COMMAND LOOP"
	while True:
		try:
			time.sleep(1)
			#data = reportGPSData()
			data = reportPilotData()
			globalData = data
			modem.pilotData = data
			if data != None:
				response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
			else:
				continue
		except Exception as inst:
			noop = None
			#comment out the following if runnign as daemon
			traceback.print_exc()
			continue

		try:
			if content != None:
				actions = json.loads(content)
				print "COMMANDS:" + content
				if actions != None and actions['data'] != None and actions['data']['actionRequests'] != None:
					print "actionRequests: " + json.dumps(actions['data']['actionRequests'])
					for i in actions['data']['actionRequests']:
						command_processor.commandQueue.put(i)

		except Exception as inst:
			noop = None
			traceback.print_exc()

