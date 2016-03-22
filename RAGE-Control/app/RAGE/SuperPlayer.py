import pygame, numpy, sys, os, time
from pygame.locals import *
from Sprite import *
from PlayerGun import *
from math import pi
from HXMReceiver import *
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
			
	def accel (self, a):
		self._a = numpy.array(a)*5
	
	def fire (self, stress=0):
		if (len(self.bullets) < maxBullets):
			self.bullets.append(PlayerShot(
									self._x + self._bulletOffset, 
									(self._containers, self.bulletGroup), 
									self._screen, self.sound_on, 
									angle=-(pi/180.)*self._wobbleAngle, 
									stress=0))
		
	def draw (self):
		Sprite.draw(self)
		for bullet in self.bullets:
			bullet.draw()
		for explosion in self.explosionList:
			explosion.draw()

	def entrance (self):
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
			
	def changeScore(self, increment):
		self.score += increment