#!/usr/bin/env python

import time, json
import command_processor


command_processor.processorinit()

command_processor.commandQueue.put(json.loads('{"command":{"name" : "RTL"}}'))
command_processor.commandQueue.put(json.loads('{"command":{"name" : "LAND"}}'))
command_processor.commandQueue.put(json.loads('{"command":{"name" : "TAKEOFF"}}'))
command_processor.commandQueue.put(json.loads('[{"command":{"name" : "TAKEOFF"}}]')[0])

time.sleep(1)


