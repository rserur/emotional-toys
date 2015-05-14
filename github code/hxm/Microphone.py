import pyaudio, threading, time, sys, OSC
from numpy import *

class MicrophoneMonitor:

	def __init__(self):
		self.p = pyaudio.PyAudio()
		channels = 1
		format = pyaudio.paFloat32
		rate = 44100
		self.stream = self.p.open(
			format = format,
			channels = channels,
			rate = rate,
			input = True)
		self.i0 = 0.1 # original min power
		self.chunk = 1024
		self.dB = 0

	def read(self):
		raw = self.stream.read(self.chunk)
		samps = fromstring(raw, dtype=float32)
		i = average(samps**2)
		if i < self.i0:
			self.i0 = i
		self.rawVol = average(samps**2)
		self.dB = 10*log10(i/(10*self.i0))
	
	"""
	def run(self):
		while True:
			try:
				raw = self.stream.read(self.chunk)
				samps = fromstring(raw, dtype=float32)
				i = average(samps**2)
				if i < self.i0:
					self.i0 = i
				self.rawVol = average(samps**2)
				self.dB = 10*log10(i/(10*self.i0))
				#print self.rawVol, self.dB
			except IOError:
				pass
	"""