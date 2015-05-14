from GUI import ModalDialog, Window, Label, Button, Task, Application, Document
from HXM import *
import objc
from AppKit import NSTimer

class HXMApp(Application):

	def __init__(self):
		Application.__init__(self)
	
	def open_app(self):
		self.make_window()

	def make_document(self, fileref):
		return HXMDoc()
	
	def make_window(self):
		win = HXMWin(self, 'Heart Rate Monitor', 5)
		win.show()
	
	def kill(self):
		self._quit()
		
	def event_loop(self):
		Application.event_loop(self)


class HXMWin(Window):

	def __init__(self, responder, text, timeout=5):
		Window.__init__(self, size=(330,150))
		self.init_labels()
		self.init_buttons()
		#self.shrink_wrap(padding = (20, 20))
		self.responder = responder
		self.server_up = False
		self.hxm_server = None
		self.timer = None
		self.start_server()
		self.init_timer()
    
	def init_labels(self):
		self.server_status = Label('Server status:')
		self.server_status_result = Label('off')
		self.hxm0_hr = Label('Heart Rate 1: ')
		self.hxm0_hr_result = Label('N/A')
		self.hxm1_hr = Label('Heart Rate 2: ')
		self.hxm1_hr_result = Label('N/A')
		self.mic_db = Label('Mic volume: ')
		self.mic_db_result = Label('')
		self.place(self.server_status, left=20, top=20)
		self.place(self.server_status_result, right=150, top=20)
		self.place(self.hxm0_hr, left=20, top=40)
		self.place(self.hxm1_hr, left=20, top=60)
		self.place(self.mic_db, left=20, top=80)
		self.place(self.mic_db_result, left=100, top=80)
		self.place(self.hxm0_hr_result, right=150, top=40)
		self.place(self.hxm1_hr_result, right=150, top=60)
	
	def init_buttons(self):
		self.start_hr_server_button = Button("Start Server", action = "start_server", enabled = True)
		self.place(self.start_hr_server_button, top=self.server_status.top, left=self.server_status.right+100)
		self.close_button = Button("Close", action="die", enabled=True)
		self.place(self.close_button, top = 100, left = 100)
	
	def start_server(self):
		self.server_status_result.text = 'starting up'
		self.server_status_result.width = 200
		self.hxm_server = HXM(responder=self)
		self.hxm_server.connect()
    
	def die(self):
		if self.hxm_server is not None:
			self.hxm_server.disconnect()
		self.responder.kill()
	
	def startup_succeeded(self):
		self.server_status_result.text = 'running'
		self.server_status_result.width = 200
	
	def set_mic_dB(self, dB):
		self.mic_db_result.text = "{0}".format("%0.2f" % round(dB,2))
		self.mic_db_result.width = 100
	
	def set_heart_rate(self, device_num, hr):
		print device_num==0, hr
		if (int(device_num) == 0):
			self.hxm0_hr_result.text = "{0}".format("%0.2f" % round(hr,2))
		if (device_num == 1):
			self.hxm1_hr_result.text = "{0}".format("%0.2f" % round(hr,2))
		self.hxm0_hr_result.width = 100
		self.hxm1_hr_result.width = 100
		
	def startup_failed(self):
		self.server_status_result.text = 'statup failed'
		self.server_status_result.width = 200
	
	def init_timer(self):
		if self.timer is not None:
			self.timer.invalidate()
		sel = objc.selector(self.pollHXM,signature='v@:')
		self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(0.01,self,sel,None,True)
	
	def pollHXM(self):
		#print 'polling...'
		self.hxm_server.read_and_publish()

class HXMDoc(Document):
	
	def __init__(self):
		Document.__init__(self)

HXMApp().run()