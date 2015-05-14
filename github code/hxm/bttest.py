def validateData(d):
	if (len(d)==59):
		return 1
	return 0

import lightblue, struct
devices = lightblue.finddevices()
for device in devices:
	addr, name, class_of_device = device

print name
# services = lightblue.findservices(addr)
# print services
s = lightblue.socket()
s.connect((addr, 1))
s.setblocking(0)
while 1==1:
	try:
		d=s.recv(60)
		if (validateData(d)):
			hr, = struct.unpack('B', d[11])
			print "HR: " + str(hr)
			hrts, = struct.unpack('H', d[13]+d[14])
			print "HR time stamp: " + str(hrts)
	except KeyboardInterrupt:
		print 'All done'
		break
	except:
		pass
