import pygame, numpy, sys, os, time
from pygame.locals import *
from Sprite import *
from PlayerGun import *
from math import pi
from HXMReceiver import *
from Sounds import *
from HXMReceiver import *

if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
sizeX = 50
sizeY = 50
difficulty = -1
maxBullets = 5
black = (0,0,0)
red = (255,0,0)
white = (255,255,255,255)
yellow = (254, 250, 15)
green = (0,255,0)
blue = (0,0,255)
maxCountdownTime = 5
_defaultFont = os.path.join(_mainDir, 'fonts', 'sourcecodepro.ttf')
_headerFont = os.path.join(_mainDir, 'fonts', 'fugaz.ttf')

class Player (Sprite):
	
	def __init__ (self, containers, screen, hxm=None, threshold=70, playerList=None, playerNum = 0, sound_on=True):
		Sprite.__init__(self, containers, screen, imageFile='goodguy2.png', size=(sizeX,sizeY), wobble=0.)
		self._x = numpy.array([0., float(self._bounds[1])-60])
		self._v = numpy.array([0.,0.])
		self._bulletOffset = numpy.array([float(sizeX)/2., 0.])
		self.playerNum = playerNum
		self.bulletGroup = pygame.sprite.Group()
		self.bullets = []
		self.score = 0
		self.thresholdScore = 0
		self.hxm = hxm
		self.fontSmall = pygame.font.SysFont(_defaultFont, 18)
		self.fontLarge = pygame.font.SysFont(_defaultFont, 40, bold=True)
		self.hrTextLabel = self.fontSmall.render('HR',True,white)
		self.countdownMode = False
		self.countdownOver = False
		self.countdownClockOutline = pygame.Surface((7,52))
		self.countdownClockSurface = pygame.Surface((5,50))
		self.colorSurface = pygame.Surface((50, 4))
		self.color = white
		self.countdownClockSurface.fill(white)
		self.countdownTime = 0
		self.countdownStartTime = 0.
		self.threshold = threshold
		self.stressed = False
		self.playerList = playerList
		self.sound_on = sound_on
		self.isSuperPlayer = False

	def accel (self, a):
		self._a = numpy.array(a)*5
	
	def fire (self, stress=0):
		if (len(self.bullets) < maxBullets):
			if (not self.countdownOver):
				self.bullets.append(PlayerShot(
									self._x + self._bulletOffset, 
									(self._containers, self.bulletGroup), 
									self._screen, self.sound_on, 
									angle=-(pi/180.)*self._wobbleAngle, 
									stress=self.hxm.HR-self.threshold))
			else:
				self.bullets.append(PlayerShot(
								   self._x + self._bulletOffset, 
								   (self._containers, self.bulletGroup), 
								   self._screen, self.sound_on,
								   angle=-(pi/180.)*self._wobbleAngle, 
								   stress=1))
		
	def draw (self):
		Sprite.draw(self)
		hrTextLabelPos = self._x + numpy.array([60.,0.])
		hrTextPos = self._x + numpy.array([60.,14.])
		self.hrText = self.fontLarge.render(("%.0f"%round(self.hxm.HR,0)),True,white)
		self._screen.blit(self.hrTextLabel, (hrTextPos[0], hrTextLabelPos[1]))
		self._screen.blit(self.hrText, (hrTextPos[0], hrTextPos[1]))
		for bullet in self.bullets:
			bullet.draw()
		self.drawCountdownTimer()
		self.drawColor()

	def drawHr (self, index):
		hrTextLabelPos = numpy.array([60.,560.])
		if index == 0:
			hrTextPos = numpy.array([200.,570.])
		else:
			hrTextPos = numpy.array([670.,570.])
		self.hrText = self.fontLarge.render(("%.0f"%round(self.hxm.HR,0)),True,white)
		self._screen.blit(self.hrTextLabel, (hrTextPos[0], hrTextLabelPos[1]))
		self._screen.blit(self.hrText, (hrTextPos[0], hrTextPos[1]))
		self.drawColor(hrTextPos[0])

	def move (self):
		Sprite.move(self)
		for bullet in self.bullets:
			if (bullet._x[1] < 0) or (bullet._x[1] > bullet._bounds[1]):
				self.bullets.remove(bullet)
				bullet.kill()
			else:
				bullet.move()
		if (self.hxm.HR-self.threshold) > 0:
			self.playerList.tellEveryoneImStressed(self)
			self.stressed = True
			self._wobble = self.hxm.stress/7.
			if self._wobble > 1.:
				self._wobble = 1.
		elif (self.countdownOver):
			self._wobble = 1
		else:
			self._wobble = 0
			self._wobbleAngle = 0
		if (self.stressed) and ((self.hxm.HR-self.threshold) < 0):
			self.playerList.tellEveryoneImBetter(self)
			self.stressed = False

	def wipeThresholdScore(self):
		self.thresholdScore = 0
	
	def changeThresholdScore(self, increment):
		self.thresholdScore += increment
	
	def changeScore(self, increment):
		self.score += increment
	
	def startCountdown(self):
		if (not self.countdownMode) and (not self.stressed):
			self.countdownMode = True
			self.countdownStartTime = time.clock()
			
	def stopCountdown(self):
		self.countdownMode = False
		self.countdownClockSurface.fill(white)
		self.countdownOver = False
	
	def drawCountdownTimer(self):
		endHeight = 50
		if (self.countdownMode):
			countdownPct = ((time.clock() - self.countdownStartTime) / maxCountdownTime)
			if countdownPct > 1:
				countdownPct = 1
				self.countdownOver = True
			pygame.draw.rect(self.countdownClockSurface, red, (0,endHeight*(1-countdownPct),5,endHeight))
			self._screen.blit(self.countdownClockSurface, (self._x[0]-25, self._x[1]))

	def drawColor(self, hrTextPosX=None):
		if self.hxm.color == 'Blue':
			self.color = blue
		elif self.hxm.color == 'Green':
			self.color = green
		else:
			self.color = yellow
		self.colorSurface.fill(self.color)
		if (hrTextPosX is not None):
			self._screen.blit(self.colorSurface, (hrTextPosX, 590.))
		else:
			self._screen.blit(self.colorSurface, (self._x[0], self._x[1]+sizeY))
