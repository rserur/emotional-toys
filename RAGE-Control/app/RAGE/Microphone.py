import pyaudio, threading, time, sys, OSC
from numpy import *

class MicrophoneMonitor (threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
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

class MicrophoneBullets (threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.mm = MicrophoneMonitor()
		self.mm.start()
		self.charging = False
		self.bullets = 0
	
	def run(self):
		while True:
			if self.mm.dB >= 4:
				if (self.charging == False):
					self.sT = time.clock()
				self.cT = time.clock() - self.sT
				if (self.cT > 1):
					self.bullets += 1
					self.sT += 1
#				print self.bullets
				self.charging = True
			else:
				if (self.charging == True):
					self.charging = False

if __name__=='__main__':
	mb = MicrophoneBullets()
	mb.start()

"""				
freq = 440.
rate = 44100
duration = 1.
amp = 0.0000000000000000001
l = rate / freq
samples = rate * duration
w = zeros(samples)
for i in range(int(samples)):
	w[i] = amp * sin((i/freq)*2.*pi)

chunk = 1024
channels = 1
format = pyaudio.paFloat32

p = pyaudio.PyAudio()
stream = p.open(
    format = format,
    channels = channels,
    rate = rate,
    input = True)

i0 = 0.1

while True:
	try:
		raw = stream.read(chunk)
		samps = fromstring(raw, dtype=float32)
		newmin = min(samps)
		i = average(samps**2)
		if i < i0:
			i0 = i
		print average(samps**2), 10*log10(i/(10*i0))
	except IOError:
		print "Frame down!"

"""
"""
stream = p.open(
			format = format, 
			channels=channels, 
			rate = rate, 
			input = False, 
			output = True, 
			frames_per_buffer=chunk)
for i in range(samples / chunk):
	start = i * chunk
	end = start + chunk
	stream.write(w[start:end])
stream.stop_stream()
stream.close()
p.terminate()
"""