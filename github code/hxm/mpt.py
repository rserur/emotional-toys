import multiprocessing
import threading
import time

class multi(multiprocessing.Process):

	def __init__ (self):
		self.thing = 0
		multiprocessing.Process.__init__(self)
		
	def run (self):
		while (True):
			self.thing += 1
			
class t (threading.Thread):
	
	def __init__ ( self ):
		self.thing = 0
		threading.Thread.__init__(self)
	
	def run(self):
		while (True):
			self.thing += 1
			
if __name__ == "__main__":
	p = t()
	p.start()
	print p.thing
	time.sleep(2)
	print p.thing
	p.terminate()
	