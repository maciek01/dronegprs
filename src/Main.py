#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback
import gps, pilot, modem
import command_processor
import argparse
import ConfigParser


def reportGPSData():
	global unitID
	global gpsPort

	if gpsPort == "":
		return None

	data = {
		"unitId" : unitID,
		"stateTimestampMS" : gps.current_milli_time(),
		"gpsLatLon" : gps.GPSLAT + " / " + gps.GPSLON,
		"gpsLat" : gps.GPSLATNORM,
		"gpsLon" : gps.GPSLONNORM,
		"gpsTime" : gps.GPSTIME,
		"gpsStatus" : gps.GPSSTATUS,
		"gpsLastStatusMS" : gps.GPSLASTSTATUSMS,
		"unitCallbackPort" : "8080",
                "modemstatus" : modem.MODEMSTATUS,
                "modemsignal" : modem.MODEMSIGNAL

	}

	return data

def reportPilotData():
	global unitID
	global mavlinkPort

	if pilot.vehicle == None or mavlinkPort == "":
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

def mergeData(pilotData, gpsData):

	if pilotData == None:
		return gpsData
	if gpsData == None:
		return pilotData

	pilotData["gpsLatLon"] = gpsData["gpsLatLon"]
	pilotData["gpsTime"] = gpsData["gpsTime"]
	pilotData["gpsStatus"] = gpsData["gpsStatus"]

	return pilotData



if __name__ == '__main__':

	print "STARTING MAIN MODULE"

	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	content = None

	#parse args	

	parser = argparse.ArgumentParser()
	parser.add_argument("--config", default="/home/pi/main.cfg")
	args = parser.parse_args()

	cfg = args.config

	#read config

	config = ConfigParser.ConfigParser()
	config.readfp(open(cfg, 'r'))

	#read cfg params
	mavlinkPort = config.get('main', 'mavlinkPort')
	mavlinkBaud = config.get('main', 'mavlinkBaud')
	gpsPort = config.get('main', 'gpsPort')
	gpsBaud = config.get('main', 'gpsBaud')
	modemPort = config.get('main', 'modemPort')
	modemBaud = config.get('main', 'modemBaud')
	modems = config.get('main', 'modems')
	host = config.get('main', 'host')
	uri = config.get('main', 'uri')
	unitID = config.get('main', 'unitID')

	#apply cfg defaults

	unitID = unitID if unitID != "" else "drone1"
	uri = uri if uri != "" else "/uavserver/v1/heartbeat"
	host = host if host != "" else "http://home.kolesnik.org:8000"
	url = host + uri


	print "CONFIGURATION:"
	print " unitID:", unitID
	print " url:", url
	print " mavlinkPort:", mavlinkPort
	print " mavlinkBaud:", mavlinkBaud
	print " gpsPort:", gpsPort
	print " gpsBaud:", gpsBaud
	print " modemPort:", modemPort
	print " modemBaud:", modemBaud
	print " modems:", modems


	headers = {'Content-Type': content_type_header}

	#initialize modem monitor
	if modemPort == "" and modems != "":
		print("LOOK FOR AVAILABLE MODEMS ...")
		modemList = modems.split(',')
		firstModem = modem.findModem(modemList, int(modemBaud))
	else:
		firstModem = modemPort
	if firstModem != "":
		print("STARTING MODEM MODULE AT " + firstModem)
		modem.modeminit(firstModem, int(modemBaud), 5, True)

	#initialize pilot
	if mavlinkPort != "":
		print "STARTING PILOT MODULE AT " + mavlinkPort
		pilot.pilotinit(mavlinkPort, int(mavlinkBaud))

	#initialize gps
	if gpsPort != "":
		print "STARTING GPS MODULE AT " + gpsPort
		gps.gpsinit(gpsPort, int(gpsBaud))

	print "STARTING COMMAND PROCESSOR MODULE"
	#initialize command queue
	command_processor.processorinit()

	#wait for vehicel connection
	while pilot.vehicle == None and mavlinkPort != "":
		time.sleep(1)

	# Get Vehicle Home location - will be `None` until first set by autopilot
	while pilot.vehicle != None and pilot.vehicle.home_location == None:
		cmds = pilot.vehicle.commands
		cmds.download()
		cmds.wait_ready(timeout=600)
		if pilot.vehicle.home_location == None:
			print " Waiting for home location ..."
			time.sleep(1)
			try:
				gpsData = reportGPSData()
				data = reportPilotData()
				data = mergeData(data, gpsData)
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

	if pilot.vehicle != None:
		# We have a home location.
		print "\n Home location: %s" % pilot.vehicle.home_location

	print "STARTING COMMAND LOOP"
	while True:
		try:
			time.sleep(1)
			gpsData = reportGPSData()
			data = reportPilotData()
			data = mergeData(data, gpsData)
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
			if content != None and content != "":
				actions = json.loads(content)
				print "COMMANDS:" + content
				if actions != None and actions['data'] != None and actions['data']['actionRequests'] != None:
					print "actionRequests: " + json.dumps(actions['data']['actionRequests'])
					for i in actions['data']['actionRequests']:
						command_processor.commandQueue.put(i)

		except Exception as inst:
			noop = None
			traceback.print_exc()

