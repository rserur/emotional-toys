import pygame, numpy, sys, os
from pygame.locals import *
from Sprite import *
from random import uniform, gauss
from math import sin, cos, pi
import Explosion
from Sounds import *

class Villians:
	
	def __init__ (self, containers, screen, sound_on=True):
		self.villianList = []
		self.explosionList = []
		self.villianGroup = pygame.sprite.Group()
		self.deadVillians = 0
		self.passedVillians = 0
		self.maxVillians = 5
		self.minVillianSpeed = 1.5
		self.maxVillianSpeed = 3.
		self._containers = containers, self.villianGroup
		self._screen = screen
		self.sound_on = sound_on
	
	def inceaseDifficulty (self):
		self.maxVillians += 1
		self.maxVillianSpeed += 0.5
	
	def newVillian (self):
		if (len(self.villianList) < self.maxVillians):
			self.villianList.append(_Villian(self._containers, self._screen, uniform(self.minVillianSpeed, self.maxVillianSpeed)))
		#Sounds().VillianEntry()

	def move (self):
		for villian in self.villianList:
			if (villian._x[1] > villian._bounds[1]):
				self.villianList.remove(villian)
				villian.kill()
			else:
				villian.move()
		for explosion in self.explosionList:
			if (explosion.expired()):
				self.explosionList.remove(explosion)
			else:
				explosion.move()
			
	def draw (self):
		for villian in self.villianList:
			villian.draw()
		for explosion in self.explosionList:
			explosion.draw()
			
	def explode (self, villian):
		centerX, centerY = villian.getCenter()
		self.villianList.remove(villian)
		villian.kill()
		if (self.sound_on):
			Sounds().Explode()
		self.explosionList.append(Explosion.Explosion(self._containers, self._screen, numpy.array([centerX, centerY])))

class _Villian (Sprite):

	def __init__ (self, containers, screen, speed):
		Sprite.__init__(self, containers, screen, imageFile='meteor.png', size=(50,50), wobble=0.)
		# self._surface.set_colorkey((255,255,255))
		self._x = numpy.array([uniform(0., self._bounds[0]), 0.])
		launchAngle = gauss(0, pi/4)
		launchV = numpy.array([sin(launchAngle), cos(launchAngle)]) * speed
		if launchV[1] < 0:
			launchV[1] = -launchV[1]
		self._v = launchV
		self._a = numpy.array([0.,0.])