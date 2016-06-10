import pygame, numpy, sys, os, random, time, math
from Sprite import *

#gameFont = pygame.font.match_font('Century Gothic,Arial')

white = (255,255,255,255)
black = (0,0,0)
teal = (0,180,214, 100)
red = (254, 65, 3)
if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
_defaultFont = os.path.join(_mainDir, 'fonts', 'questrial.ttf')
_headerFont = os.path.join(_mainDir, 'fonts', 'fugaz.ttf')
class HUD:

	def __init__ (self, containers, screen):
		self._screen = screen
		self._header = pygame.font.Font(_headerFont, 20)
		self._details = pygame.font.Font(_defaultFont, 52)
		self._flashDetails = pygame.font.Font(_headerFont, 22)
		self._BackFont = pygame.font.Font(_headerFont, 28)
		self._details.set_bold(True) 
		self._scoreHeaderPos = (5, 5)
		self._remainingHeaderPos = (580, 5)
		self._scorePos = (5, 30)
		self._flashPos = (100, 5)
		self._hrHeaderPos = (0, 100)
		self._hrPos = (0, 120)
		self._headerTextColor = white
		self._goodTextColor = teal
		self._badTextColor = red
		self._BackButtonPos = (790, 5)
		self._BackButton = self._BackFont.render('Menu', True, self._headerTextColor)
		self._scoreHeader = self._header.render('Score:',True,self._headerTextColor)
		self._hrHeader = self._header.render('Heart Rate:',True,self._headerTextColor)
		self.flash = ''
		self.flashTime = 0
		self.score = '0'
		self.hr = '0'
		self.hoverBackButton = False
		self._scoreText = self._details.render(self.score,True,self._headerTextColor)
		self._hrText = self._details.render(self.hr,True,self._headerTextColor)
		self._flashText = self._flashDetails.render(self.flash,True,self._goodTextColor)
		self.clock = Clock( screen)
		self._remainingHeader = self._header.render('Time Left: ' + self.clock.timeFormatted(), True, self._headerTextColor)
		self.heartMeterOne = HeartMeter(containers, screen, 'P1', numpy.array([5., 555.]))
		self.heartMeterTwo = HeartMeter(containers, screen, 'P2', numpy.array([710., 555.]))

	def updateHeartMeter(self, player):
		if player.playerNum == 0:
			self.heartMeterOne.blockCount = player.thresholdScore/100
		else:
			self.heartMeterTwo.blockCount = player.thresholdScore/100
	
	def setMessages(self, score=None, hr=None, flash=None, flashType=None):
		if (score is not None):
			self.score = score
			self._scoreText = self._details.render(self.score,True,self._headerTextColor)
		if (hr is not None):
			self.hr = hr
			self._hrText = self._details.render(self.hr,True,self._headerTextColor)
		if (flash is not None):
			self.flash = flash
			self.flashTime = 20
			if (flashType is 'good'):
				self._flashText = self._flashDetails.render(self.flash,True,self._goodTextColor)
			elif (flashType is 'bad'):
				self._flashText = self._flashDetails.render(self.flash,True,self._badTextColor)

	def draw(self,players_len):
		self._screen.blit(self._scoreHeader, self._scoreHeaderPos)
		self._screen.blit(self._header.render('Time Left: ' + self.clock.timeFormatted(), True, self._headerTextColor), self._remainingHeaderPos)
		self._screen.blit(self._scoreText, self._scorePos)
		self._screen.blit(self._BackButton, self._BackButtonPos)
		if (self.flashTime > 0):
			self._screen.blit(self._flashText, self._flashPos)
			self.flashTime -= 1
		self.heartMeterOne.draw()
		if players_len >= 2:
			self.heartMeterTwo.draw()
		# self._screen.blit(self._hrHeader, self._hrHeaderPos)
		# self._screen.blit(self._hrText, self._hrPos)

	def BackButtonHover(self):
		self.hoverBackButton = True

	def BackButtonLeave(self):
		self.hoverBackButton = False

class HeartMeter (Sprite):

	def __init__ (self, containers, screen, player, x, blockCount=0):
		Sprite.__init__(self, containers, screen, imageFile='heart-meter-bg.png', size=(180,46), wobble=0.)
		self._hrDetails = pygame.font.Font(_headerFont, 17)
		self._playerTextPos = (x[0] + 20, x[1] + 10)
		self._player = player
		self.blockCount = blockCount
		self._x = x
		self._player = self._hrDetails.render(self._player, True, white)

	def draw(self):
		pygame.draw.rect(self._screen, teal, (self._x[0] + 10, self._x[1] + 10, 162, 25), 2)
		for block in range(self.blockCount):
			blockX = self._x[0] + 56 + (block * 16)
			pygame.draw.rect(self._screen, teal, (blockX, self._x[1] + 13, 13, 19), 0)
		Sprite.draw(self)
		self._screen.blit(self._player, self._playerTextPos)

class Clock:

	def __init__(self, screen, duration=3.):
		self._surface = pygame.Surface((50,50))
		self._surface.set_colorkey(black)
		self.duration = duration * 60.
		self.startTime = time.clock()
		self._screen = screen

	def time(self):
		return self.duration - (time.clock() - self.startTime)
		
	def timeFormatted(self):
		return time.strftime("%-M:%S", time.localtime(int(self.time())))
