import threading
import lightblue
from numpy import *
from struct import *

class HXMDevice (threading.Thread):
	
	def __init__ (self, address, delegate=None):
		self.address = address
		self.socket = lightblue.socket()
		self.socket.connect((self.address, 1))
		self._delegate = delegate
		self._deltas = zeros(60)
		self.HRV = -1
		self._lhrts = 0	# last heart rate time stamp
		self._chrts = 0	# current heart rate time stamp
		self._gooddata = False
		self._i = 0
		threading.Thread.__init__(self)
		
	def validateData(d):
		if (len(d)==59):
			return 1
		return 0
	
	def run (self):		
		while True:
#			self.HRV += 1
			self._d = self.socket.recv(60)
#			if validateData(_d):
#				self.HR, = struct.unpack('B', d[11])
#				self._chrts, = struct.unpack('H', d[13]+d[14])
#				self._deltas[i] = self._chrts - self._lhrts
#				if (self._deltas[i] < 0):
#					self._deltas[i] += 65536
#				self._lhrts = self._chrts
#				_i = (_i + 1) % 60
#				if (_i==59):
#					_gooddata = True # Make sure that we have good data before reporting variance
#				if _gooddata:
#					self.HRV = var(_deltas)