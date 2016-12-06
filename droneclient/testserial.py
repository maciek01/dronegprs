#!/usr/bin/env python

import sys, traceback
import serial

if __name__ == '__main__':


	serialport = serial.Serial("/dev/ttyAMA0", baudrate=38400, timeout=None)

	while True:
		try:
			if serialport.inWaiting() > 0:
				command = serialport.read(serialport.inWaiting() or 1)
				print str(command),
		except Exception as inst:
                        traceback.print_exc()
