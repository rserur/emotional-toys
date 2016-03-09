import pygame, numpy, sys, os
from pygame.locals import *
from Sprite import *
from random import uniform, gauss
from math import sin, cos, pi
import Explosion

# for tomorrow -- keep working on Friends
# friends should travel horizantally, and blow up on contact with an enemy
# player tries to clear a path for them across the screen?

class Friends:
	
	def __init__ (self, containers, screen):
		self.friendList = []
		self.explosionList = []
		self.friendGroup = pygame.sprite.Group()
		self.deadFriends = 0
		self.passedFriends = 0
		self.maxFriends = 3
		self.minFriendSpeed = 5.
		self.maxFriendSpeed = 15.
		self.recovery = 0.01
		self._containers = containers, self.friendGroup
		self._screen = screen
	
	def inceaseDifficulty (self):
		self.maxFriends += 1
		self.maxFriendSpeed += 0.5
	
	def newFriend (self):
		if (len(self.friendList) < self.maxFriends):
			self.friendList.append(_Friend(self._containers, self._screen, uniform(self.minFriendSpeed, self.maxFriends)))
	
	def move (self):
		for friend in self.friendList:
			if (friend._x[0] > friend._bounds[0]):
				self.friendList.remove(friend)
				friend.kill()
			else:
				friend.move()
				if friend._wobble > 0:
					friend._wobble -= self.recovery
		for explosion in self.explosionList:
			if (explosion.expired()):
				self.explosionList.remove(explosion)
			else:
				explosion.move()
			
	def draw (self):
		for friend in self.friendList:
			friend.draw()
		for explosion in self.explosionList:
			explosion.draw()
			
	def explode (self, friend):
		centerX, centerY = friend.getCenter()
		self.friendList.remove(friend)
		friend.kill()
		self.explosionList.append(Explosion.Explosion(self._containers, self._screen, numpy.array([centerX, centerY]), imageFile='star.png'))

class _Friend (Sprite):

	def __init__ (self, containers, screen, speed):
		Sprite.__init__(self, 
						containers, 
						screen, 
						imageFile='friend.png', 
						size=(80,45), 
						wobble=0., 
						aether=numpy.array([0.,0.]), 
						accelDecay=numpy.array([0.,0.]))
		s = self._surface
		s = pygame.transform.flip(s, True, False)
		self._surface = s
		# self._surface.set_colorkey((0,0,0))
		self._x = numpy.array([0., gauss(self._bounds[1]/2., self._bounds[1]/8.)])
		launchAngle = gauss(pi/4., pi/16.)
		launchV = numpy.array([cos(launchAngle), -sin(launchAngle)]) * speed
		if launchV[0] < 0:
			launchV[0] = -launchV[0]
		self._v = launchV
		self._a = numpy.array([0.,0.01])
		