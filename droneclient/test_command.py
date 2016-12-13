#!/usr/bin/env python

import time, json
import command_processor


command_processor.processorinit()

command_processor.commandQueue.put(json.loads('{"name" : "RTL"}'))
command_processor.commandQueue.put(json.loads('{"name" : "LAND"}'))
command_processor.commandQueue.put(json.loads('{"name" : "TAKEOFF"}'))
command_processor.commandQueue.put(json.loads('[{"name" : "TAKEOFF"}]')[0])

time.sleep(1)


