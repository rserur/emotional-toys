import threading, OSC, datetime

colors = ['Blue', 'Green']

class HXMReceiver:

	def __init__(self, minDevices=1):
		addr = '127.0.0.1', 9000
		self.s = OSC.OSCServer(addr)
		self.s.addMsgHandler("/HXM", self.HXM_handler)
		self.devices = []
		for d in range(minDevices):
			self.devices.append(HXMWidget())
		self.devices[0].HR = 70

	def HXM_handler(self, addr, tags, data, source):
		device = data.pop(0)
		if (len(self.devices) < (device + 1)):
			self.devices.append(HXMWidget())
		self.devices[device].set_stats(*data)
	
	def run(self):
		self.st = threading.Thread( target = self.s.serve_forever )
		self.st.start()
		
	def close(self):
		self.s.close()
		self.st.join()
		print "Done..."

class HXMWidget:

	def __init__ (self):
		self.HR = 0.
		self.HRV = 0.
		self.stress = 0.
		self.color = 'White'
		self.hrHistory = []
		self.avgHR = 0
		self.minHR = 0
		self.maxHR = 0
		self.threshold = 0.
		self.underThreshold = 0.

	def set_stats(self, HR, HRV, stress, color='White'):
		self.HR = HR
		self.HRV = HRV
		self.stress = stress
		self.color = color
		log = {'Timestamp': str(datetime.datetime.now()), 'HR':self.HR, 'UnderThreshold': self.HR <= self.threshold }
		self.hrHistory.append(log)

	def calculate_stats(self):
		if self.hrHistory:
			HRs = [item['HR'] for item in self.hrHistory]
			self.avgHR, self.minHR, self.maxHR = (sum(HRs)/len(HRs)), min(HRs), max(HRs)
			self.underThreshold = float(sum(item['UnderThreshold'] == True for item in self.hrHistory))/len(self.hrHistory)*100

	def log(self):
		out = "Player,Threshold,Time Under Threshold,Min HR,Max HR, Average HR\n"
		out += "{0},{1},{2:.0f}%,{3},{4},{5}\n".format(self.color, self.threshold, self.underThreshold, self.minHR, self.maxHR, round(self.avgHR,1))
		out += "Player,Time,HR,Under Threshold?\n"	
		for item in self.hrHistory:
			out += "{0},{1},{2},{3}\n".format(self.color, item['Timestamp'], item['HR'], item['UnderThreshold'])
		return out