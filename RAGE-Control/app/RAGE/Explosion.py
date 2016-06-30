import pygame, numpy, sys, os
from pygame.locals import *
from Sprite import *
from math import sin, cos
from random import uniform
import time

maxParticles = 50
alphaDecay = 0.03
particleSpeed = 5.
explosionLifetime = .5

class Explosion:

	def __init__ (self, containers, screen, x, imageFile='explosion.png', explosionType='normal'):
		self._containers = containers
		self._screen = screen
		self._particles = []
		self._x = x
		self.timeStart = time.time()
		self._explosionType = explosionType
		if (self._explosionType is 'boss'):
			self._imageFile = 'explosion2.png'
		elif (self._explosionType is 'superplayer'):
			self._imageFile = 'spark.png'
		else:
			self._imageFile = imageFile
	
	def addParticle (self):
		if (len(self._particles) < maxParticles):
			while (len(self._particles) < maxParticles):
				self._particles.append(_ExplosionParticle(self._x.copy(), self._containers, self._screen, imageFile=self._imageFile, explosionType=self._explosionType))
	
	def timeElapsed (self):
		return time.time() - self.timeStart
	
	def expired (self):
		explosionLifetime = .5
		if self._explosionType is 'superplayer':
			explosionLifetime = 2
		if (self.timeElapsed() >= explosionLifetime):
			return True
		return False
	
	def move (self):
		self.addParticle()
		for particle in self._particles:
			if particle.alpha <= 0:
				self._particles.remove(particle)
			else:
				particle.move()
	
	def draw (self):
		for particle in self._particles:
			particle.draw()

class _ExplosionParticle (Sprite):

	def __init__ (self, loc, containers, screen, alpha=1., imageFile='explosion.png', explosionType='normal'):
		v0 = numpy.array([random.uniform(-1,1), random.uniform(-1,1)])
		v1 = v0 * particleSpeed
		x0 = numpy.array([random.uniform(-30,30), random.uniform(-30,30)])
		loc += x0
		if (explosionType is 'boss'):
			self._imageFile = 'explosion2.png'
			Sprite.__init__(self, containers, screen, imageFile=imageFile, size=(50,50), x=loc, v=v1)
		elif (explosionType is 'superplayer'):
			self._imageFile = 'spark.png'
			Sprite.__init__(self, containers, screen, imageFile=imageFile, size=(200,138), x=numpy.array([loc[0]-100,loc[1]-100]), v=(v1 * 2))
		else:
			self._imageFile = imageFile
			Sprite.__init__(self, containers, screen, imageFile=imageFile, size=(15,15), x=loc, v=v1)
		self._a = numpy.array([0.,0.2])
		self.alpha = alpha
		# self._surface.set_colorkey((255,255,255))
		self.kill()	# particles don't get to be in any group

	def move (self):
		Sprite.move(self)
		self._surface.set_alpha(255.*self.alpha)
		self.alpha -= alphaDecay