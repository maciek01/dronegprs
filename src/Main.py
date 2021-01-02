#!/usr/bin/env python

import httplib2, requests
import json
import time
import datetime
import socket
import sys, traceback
import gps, pilot, modem, video_manager
import command_processor
import argparse
import ConfigParser
import dbmanager
import logger

HOST = "home.kolesnik.org"

#HTTP FAILSAFE SUPPORT
fs_http_triggered = False

#heartbeat sucess ts for FAILSAFE
good_heartbeat = None
#good_heartbeat = pilot.current_milli_time()

#1 minute before triggerting http FS
#FS_TRESHOLD = 6000
FS_TRESHOLD = 60000

#request timeout
#HTTP_TIMEOUT = 0.000005
HTTP_TIMEOUT = 5

def subst(str, net = False):
	global HOST
	ipAddress = HOST
	if net:
		try:
			ipAddress = socket.gethostbyname(HOST)
		except Exception:
			ipAddress = HOST

	if str != None:
		str = str.replace("${HOSTNAME}", HOST)
		if net:
			str = str.replace("${HOSTIP}", ipAddress)

	return str

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

		"videostat" : "ON" if video_manager.process != None else "OFF",

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

def sendHeartbeat(log, unitID, http, url, headers):

	content = None
	global good_heartbeat

	try:
		gpsData = reportGPSData()
		data = reportPilotData()
		data = mergeData(data, gpsData)
		modem.pilotData = data
		if data != None:
			log.info("sending heartbeat")
			try:
				response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
				#response = requests.post(url, json = data, headers = headers, timeout = HTTP_TIMEOUT)
				#content = response.content
				#response.close()
				log.info("heartbeat sent")
				good_heartbeat = pilot.current_milli_time()
			except Exception as inst:
				log.error("http timeout")
				#traceback.print_exc()
		else:
			log.info("nothing to send")
			data = {
				#1s reporting
				"unitId" : unitID,
				"videostat" : "ON" if video_manager.process != None else "OFF",

				"modemstatus" : modem.MODEMSTATUS,
				"modemsignal" : modem.MODEMSIGNAL,

				#30 s reporting
				"unitCallbackPort" : "8080"
			}
			log.info("sending heartbeat")
			try:
				response, content = http.request( url, 'POST', json.dumps(data), headers=headers)
				#response = requests.post(url, json = data, headers = headers, timeout = HTTP_TIMEOUT)
				#content = response.content
				#response.close()
				log.info("heartbeat sent")
				good_heartbeat = pilot.current_milli_time()
			except Exception as inst:
				log.error("http timeout")
				#traceback.print_exc()


	except Exception as inst:
		noop = None
		#comment out the following if runnign as daemon
		traceback.print_exc()
		return

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


if __name__ == '__main__':

	log = logger.setup_custom_logger('main')

	log.info("STARTING MAIN MODULE")

	httplib2.debuglevel     = 0
	http                    = httplib2.Http(timeout=HTTP_TIMEOUT)
	content_type_header     = "application/json"

	#parse args	

	parser = argparse.ArgumentParser()
	parser.add_argument("--config", default="/home/pi/main.cfg")
	args = parser.parse_args()

	cfg = args.config

	#read config

	config = ConfigParser.ConfigParser()
	config.readfp(open(cfg, 'r'))

	#read cfg params
	HOST = config.get('main', 'HOSTNAME')
        HOST = HOST if HOST != "" else "home.kolesnik.org"
	mavlinkPort = subst(config.get('main', 'mavlinkPort'))
	mavlinkBaud = subst(config.get('main', 'mavlinkBaud'))
	gpsPort = subst(config.get('main', 'gpsPort'))
	gpsBaud = subst(config.get('main', 'gpsBaud'))
	modemPort = subst(config.get('main', 'modemPort'))
	modemBaud = subst(config.get('main', 'modemBaud'))
	modems = subst(config.get('main', 'modems'))
	host = subst(config.get('main', 'host'))
	uri = subst(config.get('main', 'uri'))
	dbfile = subst(config.get('main', 'dbfile'))
	unitID = subst(config.get('main', 'unitID'))
	FS_TRESHOLD = int(config.get('main', 'FS_TRESHOLD'))
	videoStreamCmd = subst(config.get('main', 'videoStreamCmd'))

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
	log.info(" FS_TRESHOLD:" + str(FS_TRESHOLD))
	log.info(" videoStreamCmd:" + videoStreamCmd)


	headers = {"Content-Type": content_type_header}

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

	#net context available
        videoStreamCmd = subst(config.get('main', 'videoStreamCmd'), net=True)


	#initialize pilot
	if mavlinkPort != "":
		log.info("STARTING PILOT MODULE AT " + mavlinkPort)
		pilot.pilotinit(mavlinkPort, int(mavlinkBaud))

	#initialize gps
	if gpsPort != "":
		log.info("STARTING GPS MODULE AT " + gpsPort)
		gps.gpsinit(gpsPort, int(gpsBaud))

	#initialize video streaming
	video_manager.init(videoStreamCmd)

	log.info("STARTING COMMAND PROCESSOR MODULE")
	#initialize command queue
	command_processor.processorinit()

	#wait for vehicleconnection
	while pilot.vehicle == None and mavlinkPort != "":
		log.info(" Waiting for vehicle connection ...")
		time.sleep(1)
		sendHeartbeat(log, unitID, http, url, headers)
		if good_heartbeat != None:
			if pilot.current_milli_time() - good_heartbeat > FS_TRESHOLD:
				log.info("FAILSAFE - noncritical")

	# Get Vehicle Home location - will be 'None' until first set by autopilot
	while pilot.vehicle != None and pilot.vehicle.home_location == None:
		try:
			cmds = pilot.vehicle.commands
			cmds.download()
			cmds.wait_ready(timeout=15)
			time.sleep(1)
			if pilot.vehicle.home_location == None:
				log.info(" Waiting for home location ...")
				sendHeartbeat(log, unitID, http, url, headers)
				if good_heartbeat != None:
					if pilot.current_milli_time() - good_heartbeat > FS_TRESHOLD:
						log.info("FAILSAFE - noncritical")
		except Exception as inst:
			traceback.print_exc()

	if pilot.vehicle != None:
		# We have a home location.
		log.info("\n Home location: %s" % pilot.vehicle.home_location)

	log.info("STARTING COMMAND LOOP")
	while True:
		time.sleep(1)
		sendHeartbeat(log, unitID, http, url, headers)
		if good_heartbeat != None:
			if pilot.current_milli_time() - good_heartbeat > FS_TRESHOLD:
				log.error("FAILSAFE condition")
				if not fs_http_triggered:
					command_processor.commandQueue.put(json.loads('{"command":{"name" : "FS_HTTP"}}'))
					log.error("HTTP FAILSAFE triggered")
					fs_http_triggered = True
			else:
				if fs_http_triggered:
					log.error("FAILSAFE cleared")
					fs_http_triggered = False



