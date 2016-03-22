import sys, pygame, os
from pygame.locals import *
import pygame.mixer
from random import choice
from datetime import datetime, timedelta

if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
_soundDir = 'Sounds'
_shotFileName = 'shot2.wav'
_cometFileName = 'comet.wav'
_explosionFileName = 'explosion.wav'
_smallExplosionFileName = 'small_explosion.wav'
_successFileName = 'success1.wav'
_superPlayerFileName = 'superplayer.wav'
_powerDownFileName = 'power-down.wav'
_entryFileNames = ['entry1.wav','entry2.wav','entry3.wav','entry4.wav']

lastStart = datetime.now() + timedelta(seconds=-3)

class Sounds:

	def __init__ (self):
		pygame.mixer.init()
		pygame.mixer.set_num_channels(32)
		self.fireSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _shotFileName))
		self.cometSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _cometFileName))
		self.explosionSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _explosionFileName))
		self.smallExplosionSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _smallExplosionFileName))
		self.successSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _successFileName))
		self.superPlayerSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _superPlayerFileName))
		self.powerDownSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _powerDownFileName))
		self.entrySounds = []
		for file in _entryFileNames:
			self.entrySounds.append(pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, file)))

	def Fire (self):
		self.fireSound.play()

	def CometStart (self):
		self.cometSound.play()

	def SuccessStart (self):
		self.successSound.play()

	def SuperPlayer (self):
		self.superPlayerSound.play()

	# def PowerDown (self):
		# if self.powerDownSound.get_num_channels() < 1:
		# 	self.powerDownSound.play()

	def VillianEntry (self):
		#print lastStart, datetime.now() - self.lastStart
		#if (datetime.now() - lastStart) > timedelta(seconds=3):
		#lastStart = datetime.now()
		#choice(self.entrySounds).play()
		return

	def Explode (self):
		self.explosionSound.play()

	def SmallExplode (self):
		self.smallExplosionSound.play()
		