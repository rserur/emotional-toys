import pygame, numpy, sys, os
from pygame.locals import *
from Sprite import *
from random import uniform, gauss
from math import sin, cos, pi
import Explosion
from Sounds import *

class Bosses:
	
	def __init__ (self, containers, screen, sound_on=True):
		self.bossList = []
		self.explosionList = []
		self.bossGroup = pygame.sprite.Group()
		self.deadBosses = 0
		self.passedBosses = 0
		self.maxBosses = 1
		self.minBossSpeed = 1.5
		self.maxBossSpeed = 3
		self._containers = containers, self.bossGroup
		self._screen = screen
		self.sound_on = sound_on
	
	def inceaseDifficulty (self):
		self.maxBossSpeed += 0.25
	
	def newBoss (self):
		if (len(self.bossList) < self.maxBosses):
			self.bossList.append(_Boss(self._containers, self._screen, uniform(self.minBossSpeed, self.maxBossSpeed)))
		if (self.sound_on):
			Sounds().CometStart()

	def move (self):
		for boss in self.bossList:
			if (boss._x[1] > boss._bounds[1]):
				self.bossList.remove(boss)
				boss.kill()
			else:
				boss.move()
		for explosion in self.explosionList:
			if (explosion.expired()):
				self.explosionList.remove(explosion)
			else:
				explosion.move()
			
	def draw (self):
		for boss in self.bossList:
			boss.draw()
		for explosion in self.explosionList:
			explosion.draw()
			
	def explode (self, boss):
		centerX, centerY = boss.getCenter()
		self.bossList.remove(boss)
		boss.kill()
		if (self.sound_on):
			Sounds().Explode()
			Sounds().SuccessStart()
		self.explosionList.append(Explosion.Explosion(self._containers, self._screen, numpy.array([centerX, centerY])))

class _Boss (Sprite):

	def __init__ (self, containers, screen, speed):
		Sprite.__init__(self, containers, screen, imageFile='big_meteor.png', size=(150,150), wobble=0.)
		# self._surface.set_colorkey((255,255,255))
		self._x = numpy.array([uniform(0., self._bounds[0]), 0.])
		launchAngle = gauss(0, pi/4)
		launchV = numpy.array([sin(launchAngle), cos(launchAngle)]) * speed
		if launchV[1] < 0:
			launchV[1] = -launchV[1]
		self._v = launchV
		self._a = numpy.array([0.,0.])
		self.deadFriends = 0
		self.maxKills = 5



		