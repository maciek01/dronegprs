#!/usr/bin/env python

import subprocess

stream_cmd = None


def init(cmd):
        global stream_cmd

	stream_cmd = cmd


def toggleVid(data):

        global stream_cmd


	process = subprocess.Popen(stream_cmd, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print process.returncode

	return None




