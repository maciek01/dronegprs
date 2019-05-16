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
import dbmanager
import logger

#this is for GPS pinger mode if enabled
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
		"gpsAlt" : gps.GPSALT,
		"gpsAltRel" : gps.GPSALT,
		"gpsSpeed" : gps.GPSSPEED,
		"heading" : gps.GPSHEADING,
		"gpsTime" : gps.GPSTIME,
		"gpsStatus" : gps.GPSSTATUS,
		"gpsNumSats" : gps.GPSNSATS,
		"gpsLock" : gps.GPSFIX,
		"gpsLastStatusMS" : gps.GPSLASTSTATUSMS,
		"unitCallbackPort" : "8080",
                "modemstatus" : modem.MODEMSTATUS,
                "modemsignal" : modem.MODEMSIGNAL

	}

	return data

#this is for mission control mode if enabled
def reportPilotData():
	global unitID
	global mavlinkPort

	if pilot.vehicle == None or mavlinkPort == "":
		return None
	
	try:
		pilot.vehicle.gps_1
		gps1 = pilot.vehicle.gps_1
	except Exception:
		gps1 = None
	
	
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

		"gps2NumSats" : gps1.satellites_visible if gps1 != None else None,
		"gps2Lock" : gps1.fix_type if gps1 != None else None,
		"gps2HError" : gps1.eph if gps1 != None else None,
		"gps2VError" : gps1.epv if gps1 != None else None,

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

#combine both sources to unified model - pilotData
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

	log = logger.setup_custom_logger('main')

	log.info("STARTING MAIN MODULE")

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
	dbfile = config.get('main', 'dbfile')
	unitID = config.get('main', 'unitID')

	#apply cfg defaults

	dbfile = dbfile if dbfile != "" else "/home/pi/uavonboard.db"
	unitID = unitID if unitID != "" else "uav0"
	uri = uri if uri != "" else "/uavserver/v1/heartbeat"
	host = host if host != "" else "http://home.kolesnik.org:8000"
	url = host + uri

	log.info("CONFIGURATION:")
	log.info(" unitID:" + unitID)
	log.info(" url:" + url)
	log.info(" mavlinkPort:" + mavlinkPort)
	log.info(" mavlinkBaud:" + mavlinkBaud)
	log.info(" gpsPort:" + gpsPort)
	log.info(" gpsBaud:" + gpsBaud)
	log.info(" modemPort:" + modemPort)
	log.info(" modemBaud:" + modemBaud)
	log.info(" modems:" + modems)
	log.info(" dbfile:" + dbfile)


	headers = {'Content-Type': content_type_header}

	#initialize database
	log.info("STARTING DATABASE " + dbfile)
	dbmanager.open(dbfile)

	#initialize modem monitor
	if modemPort == "" and modems != "":
		log.info("LOOK FOR AVAILABLE MODEMS ...")
		modemList = modems.split(',')
		firstModem = modem.findModem(modemList, int(modemBaud))
	else:
		firstModem = modemPort
	if firstModem != "":
		log.info("STARTING MODEM MODULE AT " + firstModem)
		modem.modeminit(firstModem, int(modemBaud), 5, True)

	#initialize pilot
	if mavlinkPort != "":
		log.info("STARTING PILOT MODULE AT " + mavlinkPort)
		pilot.pilotinit(mavlinkPort, int(mavlinkBaud))

	#initialize gps
	if gpsPort != "":
		log.info("STARTING GPS MODULE AT " + gpsPort)
		gps.gpsinit(gpsPort, int(gpsBaud))

	log.info("STARTING COMMAND PROCESSOR MODULE")
	#initialize command queue
	command_processor.processorinit()

	#wait for vehicel connection
	while pilot.vehicle == None and mavlinkPort != "":
		time.sleep(1)

	# Get Vehicle Home location - will be 'None' until first set by autopilot
	while pilot.vehicle != None and pilot.vehicle.home_location == None:
		cmds = pilot.vehicle.commands
		cmds.download()
		cmds.wait_ready(timeout=600)
		if pilot.vehicle.home_location == None:
			log.info(" Waiting for home location ...")
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
		log.info("\n Home location: %s" % pilot.vehicle.home_location)

	log.info("STARTING COMMAND LOOP")
	while True:
		try:
			time.sleep(1)
			gpsData = reportGPSData()
			data = reportPilotData()
			data = mergeData(data, gpsData)
			modem.pilotData = data
			if data != None:
				log.info("sending heartbeat")
				response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
				log.info("heartbeat sent")
			else:
				log.info("nothing to send")
				continue
		except Exception as inst:
			noop = None
			#comment out the following if runnign as daemon
			traceback.print_exc()
			continue

		try:
			if content != None and content != "":
				actions = json.loads(content)
				log.info("COMMANDS:" + content)
				if actions != None and actions['data'] != None and actions['data']['actionRequests'] != None:
					log.info("actionRequests: " + json.dumps(actions['data']['actionRequests']))
					for i in actions['data']['actionRequests']:
						command_processor.commandQueue.put(i)

		except Exception as inst:
			noop = None
			traceback.print_exc()

