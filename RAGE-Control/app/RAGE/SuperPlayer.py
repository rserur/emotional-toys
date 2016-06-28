import pygame, numpy, sys, os, time
from pygame.locals import *
from Sprite import *
from PlayerGun import *
from math import pi
import Explosion
from Sounds import *

if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
sizeX = 100
sizeY = 55
difficulty = -1
maxBullets = 100
black = (0,0,0)
red = (255,0,0)
white = (255,255,255,255)
yellow = (254, 250, 15)
green = (0,255,0)
blue = (0,0,255)
maxCountdownTime = 5
_defaultFont = os.path.join(_mainDir, 'fonts', 'sourcecodepro.ttf')
_headerFont = os.path.join(_mainDir, 'fonts', 'fugaz.ttf')

class SuperPlayer (Sprite):
	
	def __init__ (self, containers, screen, PlayerList=None, sound_on=True, x=0.):
		Sprite.__init__(self, containers, screen, imageFile='superplayer.png', size=(sizeX,sizeY), wobble=0.)
		self._x = numpy.array([x + 60., 460.])
		self._v = numpy.array([0.,0.])
		self._bulletOffset = numpy.array([float(sizeX)/2., 0.])
		self.explosionList = []
		self.bulletGroup = pygame.sprite.Group()
		self.bullets = []
		self.score = 0
		self.fontSmall = pygame.font.SysFont(_defaultFont, 18)
		self.fontLarge = pygame.font.SysFont(_defaultFont, 40, bold=True)
		self.PlayerList = PlayerList
		self.sound_on = sound_on
		self.isSuperPlayer = True
		self.stressed = False
		self.countdownMode = False
		self.countdownOver = False
		self.countdownClockOutline = pygame.Surface((7,52))
		self.countdownClockSurface = pygame.Surface((5,50))
		self.color = white
		self.countdownClockSurface.fill(white)
		self.countdownTime = 0
		self.countdownStartTime = 0.
		self.asteroidsHit = 0
		self.friendsHit = 0
		self.bossesHit = 0
		self.hitsTaken = 0

	def decel(self):
		self._v = numpy.array([.5, .0])
			
	def superAccel (self, accel_modifier):
		self._a = numpy.array([accel_modifier, .0])*5
	
	def fire (self, stress=0):
		if (len(self.bullets) < maxBullets):
			if (not self.countdownOver):
				for player in self.PlayerList.stressedPlayers:
					stress += player.hxm.HR-player.threshold
				self.bullets.append(PlayerShot(
									self._x + self._bulletOffset, 
									(self._containers, self.bulletGroup), 
									self._screen, self.sound_on, 
									angle=-(pi/180.)*self._wobbleAngle, 
									stress=stress))
			else:
				self.bullets.append(PlayerShot(
								   self._x + self._bulletOffset, 
								   (self._containers, self.bulletGroup), 
								   self._screen, self.sound_on,
								   angle=-(pi/180.)*self._wobbleAngle, 
								   stress=1))
		
	def draw (self):
		Sprite.draw(self)
		for bullet in self.bullets:
			bullet.draw()
		for explosion in self.explosionList:
			explosion.draw()
		self.drawCountdownTimer()

	def entrance (self):
		if self.sound_on:
			Sounds().SuperPlayer()
		centerX, centerY = self.getCenter()
		self.explosionList.append(Explosion.Explosion(self._containers, self._screen, numpy.array([centerX, centerY]), explosionType='superplayer'))
	
	def move (self):
		Sprite.move(self)
		for bullet in self.bullets:
			if (bullet._x[1] < 0) or (bullet._x[1] > bullet._bounds[1]):
				self.bullets.remove(bullet)
				bullet.kill()
			else:
				bullet.move()
		for explosion in self.explosionList:
			if (explosion.expired()):
				self.explosionList.remove(explosion)
			else:
				explosion.move()
		if len(self.PlayerList.stressedPlayers) > 0:
			self.stressed = True
			self._wobble = 0
			if self._wobble > 1.:
				self._wobble = 1.
		elif (self.countdownOver):
			self._wobble = 1
		else:
			self._wobble = 0
			self._wobbleAngle = 0
		if len(self.PlayerList.stressedPlayers) == 0:
			self.stressed = False
			
	def changeScore(self, increment):
		self.score += increment

	def startCountdown(self):
		if not self.countdownMode:
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
