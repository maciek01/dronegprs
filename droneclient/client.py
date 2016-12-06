#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback
import gps

if __name__ == '__main__':

	unitID = "drone1"
	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	host                    = "http://home.kolesnik.org:9090"

	url = host + "/heartbeat"

	headers = {'Content-Type': content_type_header}

	gps.gpsinit("/dev/ttyAMA0", 38400)

	while True:
		try:
			time.sleep(1)
			data = {
				"unitId" : unitID,
				"stateTimestampMS" : time.time() * 1000,
				"gpsLatLong" : gps.GPSLAT + " / " + gps.GPSLON,
				"gpsTime" : gps.GPSTIME,
				"unitCallbackPort" : "8080"
			}

			response, content = http.request( url,
				'POST',
				json.dumps(data),
				headers=headers)
		except Exception as inst:
			#traceback.print_exc()

