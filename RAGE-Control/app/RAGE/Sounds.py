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
_shotFileName = 'shot.wav'
_cometFileName = 'comet.wav'
_explosionFileName = 'explosion.wav'
_smallExplosionFileName = 'small_explosion.wav'
_successFileName = 'success1.wav'
_superPlayerFileName = 'superplayer.wav'
_powerDownFileName = 'power-down.wav'
_openSuperZoneFileName = 'open-superzone.wav'
_superPlayerSplitFileName = 'player-split.wav'

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
		self.openSuperZoneSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _openSuperZoneFileName))
		self.superPlayerSplitSound = pygame.mixer.Sound(os.path.join(_mainDir, _soundDir, _superPlayerSplitFileName))

	def Fire (self):
		self.fireSound.play()

	def CometStart (self):
		self.cometSound.play()

	def SuccessStart (self):
		self.successSound.play()

	def SuperPlayer (self):
		self.superPlayerSound.play()

	def PowerDown (self):
		self.powerDownSound.play()

	def OpenSuperZone (self):
		self.openSuperZoneSound.play()

	def Explode (self):
		self.explosionSound.play()

	def SmallExplode (self):
		self.smallExplosionSound.play()
		
	def SuperPlayerSplit (self):
		self.superPlayerSplitSound.play()