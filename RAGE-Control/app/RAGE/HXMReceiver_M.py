import threading, OSC, time

class HXMReceiver_M ():

	def __init__ (self):
		self.charging = False
		self.bullets = 0
		addr = '127.0.0.1', 9000
		self.s = OSC.OSCServer(addr)
		self.s.addMsgHandler("/Mic", self.Mic_handler)
		self.stress = 0
	
	def Mic_handler(self, addr, tags, data, source):
		self.dB = data[0]
		self.vol = data[1]
		if self.dB >= 4:
			if (self.charging == False):
				self.sT = time.clock()
			self.cT = time.clock() - self.sT
			if (self.cT > 1):
				self.bullets += 1
				self.sT += 1
			self.charging = True
		else:
			self.charging = False
	
	def run(self):
		self.st = threading.Thread( target = self.s.serve_forever )
		self.st.start()
		
	def close(self):
		self.s.close()
		self.st.join()
		print "Done..."