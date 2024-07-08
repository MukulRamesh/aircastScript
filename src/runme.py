# THIS FILE SHOULD NOT BE USED / ACCESSED

# DEPRECIATED: Now using gui.py to render an interface.

import sys
import datetime

class Logger(object):
	def __init__(self):
		self.terminal = sys.stdout
		self.log = open("log.txt", "a")

	def write(self, message):
		now = datetime.datetime.now()
		timedMessage = str(now) + " : " + message
		if (message != '\n'):
			self.log.write(timedMessage + '\n')  
		self.terminal.write(message)

stdOut = sys.stdout
sys.stdout = Logger()

import unzip
import cleanup

sys.stdout = stdOut

