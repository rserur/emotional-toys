import pygame, numpy, sys, os, random, time, math
from pygame.locals import *
from Sprite import *

#gameFont = pygame.font.match_font('Century Gothic,Arial')

white = (255,255,255,255)
black = (0,0,0)
teal = (0,180,214)
red = (254, 65, 3)
sizeX = 200
sizeY = 90
superZonePos = numpy.array([300.,460.])
if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
_defaultFont = os.path.join(_mainDir, 'fonts', 'questrial.ttf')
_headerFont = os.path.join(_mainDir, 'fonts', 'fugaz.ttf')

class SuperZone (Sprite):

	def __init__ (self, containers, screen):
		Sprite.__init__(self, containers, screen, imageFile='super_zone.png', size=(sizeX,sizeY), wobble=0.)
		self._x = superZonePos
		self._header = pygame.font.Font(_headerFont, 20)
		self._details = pygame.font.Font(_defaultFont, 14)
		self._details.set_bold(True) 
		self._zoneHeaderPos = (self._x[0] + 45, self._x[1] - 20)
		self._headerTextColor = teal
		self._flashTime = 0
		self._zoneHeader = self._header.render('SuperZone!',True,self._headerTextColor)

	def setFlashTime(self, flashTime=None):
		self._flashTime = flashTime
	
	def draw(self):
		if (self._flashTime > 0):
			Sprite.draw(self)
			self._screen.blit(self._zoneHeader, self._zoneHeaderPos)
			self._flashTime -= 1