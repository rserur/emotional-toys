import threading, OSC

class HXMReceiver:

	#receiver needs to handle more than one device...
	
	def HXM_handler(self, addr, tags, data, source):
		self.HR=data[1]
		self.HRV=data[2]
		print data
	
	def __init__(self):
		addr = '127.0.0.1', 9000
		self.s = OSC.OSCServer(addr)
		self.s.addMsgHandler("/HXM", self.HXM_handler)
		self.HR = 0
		self.HRV = 0
	
	def run(self):
		self.st = threading.Thread( target = self.s.serve_forever )
		self.st.start()
		
	def close(self):
		self.s.close()
		self.st.join()
		print "Done..."

if __name__ == '__main__':
	hxm = HXMReceiver()
	hxm.run()