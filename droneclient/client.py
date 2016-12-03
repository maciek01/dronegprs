#!/usr/bin/env python

import httplib2
import json
import time
import datetime
import sys, traceback

if __name__ == '__main__':

	unitID = "drone1"
	httplib2.debuglevel     = 0
	http                    = httplib2.Http()
	content_type_header     = "application/json"
	host                    = "http://home.kolesnik.org:9090"

	url = host + "/heartbeat"

	headers = {'Content-Type': content_type_header}

	while True:
		try:
			time.sleep(1)
			data = {
				"unitId" : unitID,
				"stateTimestampMS" : time.time() * 1000,
				"gpsLatLong" : "2832.1834,N,08101.0536,W",
				"unitCallbackPort" : "8080"
			}

			response, content = http.request( url,
				'POST',
				json.dumps(data),
				headers=headers)
			#print (response)
			#print (content)
		except Exception as inst:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			#traceback.print_exc()
			#print repr(traceback.format_exception(exc_type, exc_value,
			#					  exc_traceback))
			#print traceback.format_exception(exc_type, exc_value,
			#					  exc_traceback)

