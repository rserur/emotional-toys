import pygame, numpy, sys, os, random, HUD

class HUD_M (HUD.HUD):

	def __init__ (self, screen):
		HUD.HUD.__init__(self, screen)
		self._bulletCountHeaderPos = (1000, 0)
		self._bulletCountPos = (1000, 20)
		self._bulletCountHeader = self._header.render('Bullets:',True,self._headerTextColor)
		self.bulletCount = '0'
		self._bulletCountText = self._details.render(self.bulletCount,True,self._headerTextColor)
	
	def setMessages(self, score=None, hr=None, bullets=None):
		HUD.HUD.setMessages(self, score, hr)
		if (bullets is not None):
			self.bulletCount = bullets
			self._bulletCountText = self._details.render(self.bulletCount,True,self._headerTextColor)
	
	def draw(self):
		HUD.HUD.draw(self)
		self._screen.blit(self._bulletCountHeader, self._bulletCountHeaderPos)
		self._screen.blit(self._bulletCountText, self._bulletCountPos)