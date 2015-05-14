import pygame, sys, serial, random, time, os
from pygame.locals import *

A_BUTTON = 1
B_BUTTON = 2
START_BUTTON = 9
SELECT_BUTTON = 8
UP_DOWN_AXIS = 4
UP_VALUE = -1
DOWN_VALUE = 1
LEFT_RIGHT_AXIS = 3
LEFT_DIRECTION = -0.5
RIGHT_DIRECTION = 0.5

white = (255,255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors = {'White': white, 'Black': black, 'Red': red, 'Blue': blue, 'Green': green}


def loop():
	threshold1 = 150
	threshold2 = 150
	sers = getSerialPorts()
	print "Available Serial Interfaces:\n\t", sers
	gamepads = []
	for i in range(pygame.joystick.get_count()):
		gamepads.append(pygame.joystick.Joystick(i))
		pygame.joystick.Joystick(i).init()
	print "Available Gamepads:\n\t", gamepads
	hr1 = 0.0
	hr2 = 0.0
	screen = pygame.display.get_surface()
	looping = True
	player1DrivingForward = False
	player1DrivingBackward = False
	player1TurningLeft = False
	player1TurningRight = False
	player2DrivingForward = False
	player2DrivingBackward = False
	player2TurningLeft = False
	player2TurningRight = False
	dontSpam1 = False
	dontSpam1Time = time.clock()
	dontSpam2 = False
	dontSpam2Time = time.clock()
	while looping:
		#get HR
		hr1Color = 'Blue'
		hr2Color = 'Green'
		
		events = pygame.event.get()
		for event in events:
			#print event
			if event.type == QUIT:
				for ser in sers:
					ser.write(chr(0)+'\n')
					ser.close()
				sys.exit(0)
			elif (event.type == KEYDOWN) and (event.key == K_ESCAPE):
				for ser in sers:
					ser.write(chr(0)+'\n')
					ser.close()
				sys.exit(0)
			elif (event.type == KEYDOWN) and (event.key == K_z):
				threshold1 -= 1	
			elif (event.type == KEYDOWN) and (event.key == K_x):
				threshold1 += 1
			elif (event.type == KEYDOWN) and (event.key == K_n):
				threshold2 -= 1
			elif (event.type == KEYDOWN) and (event.key == K_m):
				threshold2 += 1
			elif (event.type == KEYDOWN):
			    if (event.key == 276):
			        # left arrow key
			        player2TurningLeft = True
			    elif (event.key == 273):
			        # up arrow key
			        player2DrivingForward = True
			    elif (event.key == 274):
			        # down arrow key
			        player2DrivingBackward = True
			    elif (event.key == 275):
			        # right arrow key
			        player2TurningRight = True
			    elif (event.key == K_a):
			        # left arrow key
			        player1TurningLeft = True
			    elif (event.key == K_w):
			        # up arrow key
			        player1DrivingForward = True
			    elif (event.key == K_s):
			        # down arrow key
			        player1DrivingBackward = True
			    elif (event.key == K_d):
			        # right arrow key
			        player1TurningRight = True
			elif (event.type == KEYUP):
			    if (event.key == 276):
			        # left arrow key
			        player2TurningLeft = False
			    elif (event.key == 273):
			        # up arrow key
			        player2DrivingForward = False
			    elif (event.key == 274):
			        # down arrow key
			        player2DrivingBackward = False
			    elif (event.key == 275):
			        # right arrow key
			        player2TurningRight = False
			    elif (event.key == K_a):
			        # left arrow key
			        player1TurningLeft = False
			    elif (event.key == K_w):
			        # up arrow key
			        player1DrivingForward = False
			    elif (event.key == K_s):
			        # down arrow key
			        player1DrivingBackward = False
			    elif (event.key == K_d):
			        # right arrow key
			        player1TurningRight = False
			elif (event.type == JOYBUTTONDOWN):
				if (event.button == A_BUTTON) and (event.joy == 0):
					player1DrivingForward = True
				if (event.button == B_BUTTON) and (event.joy == 0):
					player1DrivingBackward = True
				if (event.button == A_BUTTON) and (event.joy == 1):
					player2DrivingForward = True
				if (event.button == B_BUTTON) and (event.joy == 1):
					player2DrivingBackward = True
			elif (event.type == JOYBUTTONUP):
				if (event.button == A_BUTTON) and (event.joy == 0):
					player1DrivingForward = False
				elif (event.button == B_BUTTON) and (event.joy == 0):
					player1DrivingBackward = False
				elif (event.button == A_BUTTON) and (event.joy == 1):
					player2DrivingForward = False
				elif (event.button == B_BUTTON) and (event.joy == 1):
					player2DrivingBackward = False
			elif (event.type == JOYAXISMOTION):
				if (event.axis == LEFT_RIGHT_AXIS) and (event.value < LEFT_DIRECTION) and (event.joy == 0):
					player1TurningLeft = True
				elif (event.axis == LEFT_RIGHT_AXIS) and (event.value > RIGHT_DIRECTION) and (event.joy == 0):
					player1TurningRight = True
				elif (event.axis == LEFT_RIGHT_AXIS) and (event.joy == 0):
					player1TurningLeft = False
					player1TurningRight = False
				elif (event.axis == LEFT_RIGHT_AXIS) and (event.value < LEFT_DIRECTION) and (event.joy == 1):
					player2TurningLeft = True
				elif (event.axis == LEFT_RIGHT_AXIS) and (event.value > RIGHT_DIRECTION) and (event.joy == 1):
					player2TurningRight = True
				elif (event.axis == LEFT_RIGHT_AXIS) and (event.joy == 1):
					player2TurningLeft = False
					player2TurningRight = False

		# print player1DrivingForward, player1DrivingBackward, player1TurningLeft, player1TurningRight
		out1 = (chr(0)+'\n')
		p1ButtonBressed = True
		if player1DrivingForward and not player1TurningLeft and not player1TurningRight and (hr1 <= threshold1):
			out1 = chr(1)+'\n'
		elif player1DrivingForward and player1TurningLeft and (hr1 <= threshold1):
			out1 = chr(8)+'\n'
		elif player1DrivingForward and player1TurningRight and (hr1 <= threshold1):
			out1 = chr(2)+'\n'
		elif player1DrivingBackward and not player1TurningLeft and not player1TurningRight and (hr1 <= threshold1):
			out1 = chr(5)+'\n'
		elif player1DrivingBackward and player1TurningLeft and (hr1 <= threshold1):
			out1 = chr(6)+'\n'
		elif player1DrivingBackward and player1TurningRight and (hr1 <= threshold1):
			out1 = chr(4)+'\n'
		elif player1TurningLeft and (hr1 <= threshold1):
			out1 = chr(7)+'\n'
		elif player1TurningRight and (hr1 <= threshold1):
			out1 = chr(3)+'\n'
		if (hr1 > threshold1):
			out1 = chr(random.randint(0,8))+'\n'
		elif not player1DrivingForward and not player1DrivingBackward and not player1TurningLeft and not player1TurningRight:
			out1 = chr(0)+'\n'
			p1ButtonBressed = False
		if not dontSpam1:
			sers[0].write(out1)
			if (sers[0].inWaiting() > 0) :
			    hr1 = float( ord( sers[0].read() ) )
			    #print hr1
			    sers[0].flushInput()
			#print "heart rate 1 ",hr1
			dontSpam1 = True
			dontSpam1Time = time.clock()
		elif time.clock() - dontSpam1Time:
			dontSpam1 = False

		out2 = (chr(0)+'\n')
		p2ButtonBressed = True
		if player2DrivingForward and not player2TurningLeft and not player2TurningRight and (hr2 <= threshold2):
			out2 = chr(1)+'\n'
		elif player2DrivingForward and player2TurningLeft and (hr2 <= threshold2):
			out2 = chr(8)+'\n'
		elif player2DrivingForward and player2TurningRight and (hr2 <= threshold2):
			out2 = chr(2)+'\n'
		elif player2DrivingBackward and not player2TurningLeft and not player2TurningRight and (hr2 <= threshold2):
			out2 = chr(5)+'\n'
		elif player2DrivingBackward and player2TurningLeft and (hr2 <= threshold2):
			out2 = chr(6)+'\n'
		elif player2DrivingBackward and player2TurningRight and (hr2 <= threshold2):
			out2 = chr(4)+'\n'
		elif player2TurningLeft and (hr2 <= threshold2):
			out2 = chr(7)+'\n'
		elif player2TurningRight and (hr2 <= threshold2):
			out2 = chr(3)+'\n'
		if (hr2 > threshold2):
			out2 = chr(random.randint(0,8))+'\n'
		elif not player2DrivingForward and not player2DrivingBackward and not player2TurningLeft and not player2TurningRight:
			out2 = chr(0)+'\n'
			p2ButtonBressed = False
		if not dontSpam2 and (len(sers) > 1):
			sers[1].write(out2)
			if (sers[1].inWaiting() > 0) :
			    hr2 = float( ord( sers[1].read() ) )
			if (sers[1].inWaiting() > 1) :
			    sers[1].flushInput()
			#print "heart rate 2 ", hr2
			dontSpam2 = True
			dontSpam2Time = time.clock()
		elif time.clock() - dontSpam2Time:
			dontSpam2 = False
		
		drawBackground(screen)
		drawHR(screen, hr1, hr2, colors[hr1Color], colors[hr2Color])
		drawThresh(screen, threshold1, threshold2)
		drawButtonIndicator(screen, p1ButtonBressed, p2ButtonBressed)
		pygame.display.flip()

def drawHR(screen, hr1, hr2, hr1Color=black, hr2Color=black):
	hrFont = pygame.font.Font(None, 500)
	playerNameFont = pygame.font.Font(None, 100)
	
	#player 1 HR Display
	#hr1Color = black
	hr1Display = hrFont.render(("%.0f"%round(hr1,0)), True, hr1Color)
	player1Display = playerNameFont.render("Player 1 HR", True, black)
	screen.blit(hr1Display, ((screen.get_size()[0]/4.)-hr1Display.get_size()[0]/2.,150))
	screen.blit(player1Display, ((screen.get_size()[0]/4.)-player1Display.get_size()[0]/2.,25))

	#player 2 HR Display
	#hr2Color = black
	hr2Display = hrFont.render(("%.0f"%round(hr2,0)), True, hr2Color)
	player2Display = playerNameFont.render("Player 2 HR", True, black)
	screen.blit(hr2Display, ((3*screen.get_size()[0]/4.)-hr2Display.get_size()[0]/2.,150))
	screen.blit(player2Display, ((3 * screen.get_size()[0]/4.)-player2Display.get_size()[0]/2.,25))

def drawThresh(screen, hr1, hr2):
	hrFont = pygame.font.Font(None, 200)
	playerNameFont = pygame.font.Font(None, 50)
	
	#player 1 HR Display
	hr1Color = black
	hr1Display = hrFont.render(("%.0f"%round(hr1,0)), True, hr1Color)
	player1Display = playerNameFont.render("Threshold HR:", True, black)
	screen.blit(hr1Display, ((screen.get_size()[0]/4.)-hr1Display.get_size()[0]/2.,550))
	screen.blit(player1Display, ((screen.get_size()[0]/4.)-player1Display.get_size()[0]/2.,500))
	
	#player 2 HR Display
	hr2Color = black
	hr2Display = hrFont.render(("%.0f"%round(hr2,0)), True, hr2Color)
	player2Display = playerNameFont.render("Threshold HR:", True, black)
	screen.blit(hr2Display, ((3*screen.get_size()[0]/4.)-hr2Display.get_size()[0]/2.,550))
	screen.blit(player2Display, ((3 * screen.get_size()[0]/4.)-player2Display.get_size()[0]/2.,500))

def drawButtonIndicator(screen, p1, p2):
	if p1:
		pygame.draw.circle(screen, black, (screen.get_size()[0]/4-5, 675), 5)
	if p2:
		pygame.draw.circle(screen, black, (3 * screen.get_size()[0]/4-5, 675), 5)

def drawBackground(screen):
	bg = pygame.Surface(screen.get_size())
	bg = bg.convert()
	bg.fill(white)
	screen.blit(bg, (0,0))
	
def getSerialPorts():
	serialports = []
	"""
	try:
		ser = serial.Serial('/dev/tty.usbmodem641', 115200)
		serialports.append(ser)
	except:
		pass
	try:
		ser = serial.Serial('/dev/tty.usbmodem411', 115200)
		serialports.append(ser)
	except:
		pass
	"""
	for dirname, dirnnames, filenames in os.walk('/dev'):
		for filename in filenames:
			if 'tty' in filename and 'usbmodem' in filename:
				devAddr = dirname + '/' + filename
				ser = serial.Serial(devAddr, 115200)
				serialports.append(ser)
				
	return serialports
	

if __name__ == '__main__':
	#print getSerialPorts()
	pygame.init()
	full_screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN| pygame.DOUBLEBUF | pygame.HWSURFACE)
	loop()
	
	

