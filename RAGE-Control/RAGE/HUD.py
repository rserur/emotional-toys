import pygame, numpy, sys, os, random, time, math

#gameFont = pygame.font.match_font('Century Gothic,Arial')

white = (255,255,255,255)
black = (0,0,0)

class HUD:

	def __init__ (self, screen):
		self._screen = screen
		self._header = pygame.font.Font(None, 20)
		self._details = pygame.font.Font(None, 90)
		self._BackFont = pygame.font.Font(None, 48)
		self._details.set_bold(True) 
		self._scoreHeaderPos = (0, 0)
		self._scorePos = (0, 20)
		self._hrHeaderPos = (0, 100)
		self._hrPos = (0, 120)
		self._headerTextColor = (0,0,0)
		self._SelectedColor = (255,0,0)
		self._BackButtonPos = (650, 0)
		self._BackButton = self._BackFont.render('Back to Menu', True, self._headerTextColor)
		self._scoreHeader = self._header.render('Score:',True,self._headerTextColor)
		self._hrHeader = self._header.render('Heart Rate:',True,self._headerTextColor)
		self.score = '0'
		self.hr = '0'
		self.hoverBackButton = False
		self._scoreText = self._details.render(self.score,True,self._headerTextColor)
		self._hrText = self._details.render(self.hr,True,self._headerTextColor)
		self.clock = Clock(screen)
	
	def setMessages(self, score=None, hr=None):
		if (score is not None):
			self.score = score
			self._scoreText = self._details.render(self.score,True,self._headerTextColor)
		if (hr is not None):
			self.hr = hr
			self._hrText = self._details.render(self.hr,True,self._headerTextColor)
	
	def draw(self):
		self._screen.blit(self._scoreHeader, self._scoreHeaderPos)
		self._screen.blit(self._scoreText, self._scorePos)
		self._screen.blit(self._BackButton, self._BackButtonPos)
		self.clock.draw()
		#self._screen.blit(self._hrHeader, self._hrHeaderPos)
		#self._screen.blit(self._hrText, self._hrPos)

	def BackButtonHover(self):
		self._BackButton = self._BackFont.render('Back to Menu',True,self._SelectedColor)
		self.hoverBackButton = True

	def BackButtonLeave(self):
		self._BackButton = self._BackFont.render('Back to Menu',True,self._headerTextColor)
		self.hoverBackButton = False


class Clock:

	def __init__(self, screen, duration=3.):
		self._surface = pygame.Surface((50,50))
		self.duration = duration * 60.
		self.startTime = time.clock()
		self._screen = screen

	def draw(self):
		self._surface.fill(white)
		seconds = self.duration - (time.clock() - self.startTime)
		minutes = seconds / 60.
		minuteHandAngle = 2 * math.pi * ((minutes % 12)/12.) # We're going to pretend a clock shows 12 minutes, not 12 hours
		secondHandAngle = 2 * math.pi * ((seconds % 60) / 60)
		minHandLen = 10
		secHandLen = 25
		minHandCoord = (math.sin(minuteHandAngle) * minHandLen + 25, -math.cos(minuteHandAngle) * minHandLen + 25)
		secHandCoord = (math.sin(secondHandAngle) * secHandLen + 25, -math.cos(secondHandAngle) * secHandLen + 25)
		pygame.draw.aaline(self._surface, black, (25,25), minHandCoord)
		pygame.draw.aaline(self._surface, black, (25,25), secHandCoord)
		pygame.draw.circle(self._surface, black, (25,25), secHandLen, 2)
		self._screen.blit(self._surface, (600, 10))

	def time(self):
		return self.duration - (time.clock() - self.startTime)
		