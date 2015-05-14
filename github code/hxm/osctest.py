import OSC, time

def handler(addr, tags, data, source):
	print data

if __name__ == '__main__':
	print "OSC Tester!"
	addr = '127.0.0.1', 9000
	s = OSC.OSCServer(addr)
	s.addMsgHandler("/HXM", handler)
	while True:
		time.sleep(1)
	