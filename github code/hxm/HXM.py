# HXM Class
# Jason Kahn (c) 2011
# Searches for an arbitrary number of HXM devices
#	and starts an OSC server to post HR and HRV data
#	Data:
#		\HXM\DeviceCount\<value>		Number of devices
#		\HXM\<Device X>\HR\<value>		HR on Device X
#		\HXM\<Device X>\HRV\<value>		HRV on Device X


USING_COLORS = True

import lightblue, re, struct, OSC, random, time, datetime, Microphone, os, threading, Queue, multiprocessing, sys
from numpy import *

DeviceColors = {'HXM003891':'Blue', 'HXM009982': 'Green'}

def _z(a, x):
	"""compute z-score for x for population a"""
	s = std(a)
	u = mean(a)
	dfm = x - u
	nsd = dfm / s
	return nsd

class _HRVTracker:

	def __init__(self):
		self._lastHRTS = 0
		self.insertPoint = 0
		self.deltas = zeros(60)
		self.HRV = 0.0
		self.timeStart = time.time()
		self._calibrating = True
		self._initPeriod = 60
		self._HRVPopulation = []
		self._HRPopulation = []
		
	def addTimeStamp(self, ts):
		try:
			delta = ts - self._lastHRTS
			if (delta == 0):
				return
			self._lastHRTS = ts
			if (delta < 0):
				delta += 65536
			self.deltas[self.insertPoint] = delta
			self.insertPoint += 1
			self.insertPoint = self.insertPoint % 60
			self.HRV = self.deltas.var()
			return
		except:
			return
	
	def mHRHRV (self, timeStamps, dataPoints=15):
		print "decoding..."
		data = zeros(dataPoints)
		deltas = zeros(dataPoints-1)
		for i in range(dataPoints):
			data[i], = struct.unpack('H', timeStamps[i*2]+timeStamps[i*2+1])
			if (i >= 1):
				deltas[i-1]=data[i-1]-data[i]
				if (deltas[i-1] < 0): 
					deltas[i-1] += 65536
		hr = 1./(average(deltas)/60000.)
		hrv = deltas.var()
		if (self._calibrating):
			self._HRPopulation.append(hr)
			self._HRVPopulation.append(hrv)
			if ((time.time() - self.timeStart) > self._initPeriod):
				self._calibrating = False
		stress = (1.0 * _z(self._HRPopulation, hr)) + (0.0 * _z(self._HRVPopulation, hrv))
		# print data, deltas
		print "decoded"
		return hr, hrv, stress
	
	def mHRHRV2 (self, timeStamps, deviceNum, queue = None, dataPoints=15, responder=None, color=None):
		data = zeros(dataPoints)
		deltas = zeros(dataPoints-1)
		for i in range(dataPoints):
			data[i], = struct.unpack('H', timeStamps[i*2]+timeStamps[i*2+1])	# unpack bytes and translate into number
			if (i >= 1):														# calculate deltas if not first element
				deltas[i-1]=data[i-1]-data[i]
				if (deltas[i-1] < 0): 
					deltas[i-1] += 65536
		if (average(deltas) > 0):
			hr = 1./(average(deltas)/60000.)	# get heart rate in bpm
		else:
			hr = 0
		hrv = deltas.var()
		if (self._calibrating):				# not used -- 
			self._HRPopulation.append(hr)
			self._HRVPopulation.append(hrv)
			if ((time.time() - self.timeStart) > self._initPeriod):
				self._calibrating = False
		stress = (0.9 * _z(self._HRPopulation, hr)) + (0.1 * _z(self._HRVPopulation, hrv))	# not based on anything
		if USING_COLORS:
			q_items=(deviceNum,hr,hrv,stress,color)
		else:
			q_items=(deviceNum,hr,hrv,stress)
		queue.put(q_items)
		#print deviceNum, hr
		if responder is not None:
			#print deviceNum, hr
			responder.set_heart_rate(deviceNum, hr)
		print "/HXM/" + str(deviceNum) + "/HR/" + str(hr)
		#print "/HXM/" + str(deviceNum) + "/HRV/" + str(hrv)
		#print "/HXM/" + str(deviceNum) + "/Stress/" + str(stress)
	

class HXM():

	def __init__(self, responder=None):
		#multiprocessing.Process.__init__(self)
		self.OSCClient = OSC.OSCClient()
		self.OSCAddr = '127.0.0.1', 9000
		self.q = Queue.Queue()
		self.responder = responder
		self.use_mic = False
		self.connected = False
		self.mic = None
		self.addr_name = {}
	
	def _validateData(self, data):
		# add more robust data validation at some point
		if (len(data)==59):
			return 1
		return 0	
	
	def connect(self):
		try:
			addrList = []
			self.sockets = []
			self._HRV = []
			devices = lightblue.finddevices()
			for device in devices:
				addr, name, class_of_device = device
				print device
				self.addr_name[addr] = name
				if (re.match('HXM', name)):
					addrList.append(addr)
			i = 0
			for addr in addrList:
				s = lightblue.socket()
				s.connect((addr, 1))
				s.setblocking(1)		# set to 0 for in-game use
				self.sockets.append(s)
				t = _HRVTracker()
				self._HRV.append(t)
				i += 1
			self._deviceCount = i
			print "Added " + str(i) + " devices"
			if self.responder is not None:
				self.responder.startup_succeeded()
			self.connected = True
		except:
			print "Unable to add devices"
			self._deviceCount = 0
			if self.responder is not None:
				self.responder.startup_failed()
	
	def connect_hxm(self):
		self.connect()
	
	def connect_mic(self):
		self.use_mic = True
		self.mic = Microphone.MicrophoneMonitor()
	
	def disconnect(self):
		self._deviceCount = 0
		for socket in self.sockets:
			socket.close()
	
	def read_and_publish(self, output_file = None):
		i=0
		threads = []
		mic = self.mic
		if self.use_mic:					
			mic.read()
			bundle = OSC.OSCBundle()
			bundle.setAddress("/Mic")
			bundle.append((mic.dB, mic.rawVol))
			try:
				self.OSCClient.send(bundle)
			except:

				pass
			if self.responder is not None:
				self.responder.set_mic_dB(mic.dB)
		for socket in self.sockets:
			socket.setblocking(0)
			if self.use_mic:
				socket.setblocking(0)	# so we don't wait for a HXM read before using the mic
			try:
				incomming = socket.recv(60)
				#print "got data:", len(incomming), incomming
				if (self._validateData(incomming)):
					msgs = []
					d0 = incomming[13:43]
					# remove color info if problems
					t = threading.Thread(target=self._HRV[i].mHRHRV2, args=(d0, i, self.q, 15, self.responder, DeviceColors[self.addr_name[socket.getpeername()[0]]]))
					t.start()
					threads.append(t)
					
					while (not self.q.empty()):
						bundle = OSC.OSCBundle()
						bundle.setAddress("/HXM")
						q_data = self.q.get()
						bundle.append(q_data)
						try:
							self.OSCClient.send(bundle)
							if (output_file is not None):
								f = open(output_file, 'a')
								f.write('{0},{1},{2},{3}\n'.format(q_data[0], time.time(), q_data[1], q_data[2]))
								f.close()
						except:
							pass						
			except KeyboardInterrupt:
				print "Keyboard interrupt..."
				raise NameError("User Interrupt")
			except:
				pass
			i += 1
			for t0 in threads:
				t0.join()
	
	def run(self, logging=True, microphone=False):
		
		connected_osc = False
		self.mic = None
		if (self._deviceCount<1):
			print "No connected devices -- forcing microphone mode"
			self.connect_mic()
			#return
		
		outfile = None
		if logging:
			startTime = time.time()
			t = datetime.datetime.fromtimestamp(time.time())
			outfile = './Logs/Log ' + t.strftime('%Y-%m-%d %H.%M.%S') + '.csv'
			f = open(outfile, 'w')
			f.write('"Device","Time","HR","HRV15"\n')
			f.close()
		
		if microphone:
			self.mic = Microphone.MicrophoneMonitor()
		
		while 1:
			try:
				if not connected_osc:
					try:
						self.OSCClient.connect(self.OSCAddr)
						connected_osc = True
					except:
						print "There's no one to talk to... I'll keep trying"
				else:
					self.read_and_publish(outfile)

					
			except IOError:
				print "mic frame down!"
				pass
			except KeyboardInterrupt:
				print "User ended the loop"
				if logging:
					f.close()
				break
			#except NameError:
			#	print "User ended the loop"
			#	if logging:
			#		f.close()
			#	break
			#except:
			#	print "something weird happened"
			#	pass


		
		
		
		

	