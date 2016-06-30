import pygame, Sprite, numpy, random, os, time, datetime
from git import Repo

maxParticles = 150
particleSpeed = 15
alphaDecay = 0.025
black = (0,0,0)
yellow = (254, 250, 15)
white = (255,255,255)
if 'RESOURCEPATH' in os.environ:
	_mainDir = os.environ['RESOURCEPATH']
else:
	_mainDir = os.path.split(os.path.abspath(__file__))[0]
	REPO = Repo('../../')
_SoundImage = 'art/sound.png'
_MuteImage = 'art/sound_mute.png'
_SoundSize = (100,100)
_MuteSize = (100,100)
t = datetime.datetime.fromtimestamp(time.time())
d = t.strftime('%Y-%m-%d')
_logDir = os.path.join(os.path.expanduser('~'),'Documents','CALMS-gameplay-logs/{0}/'.format(d))
if not os.path.exists(_logDir):
	os.makedirs(_logDir)

class EndingScreen:

	def __init__(self, screen, players=[]):
		print "reached endingscreen init"
		all = pygame.sprite.RenderUpdates()
		self._screen = screen
		self._players = players
		self.background = Sprite.Sprite(all, screen, imageFile='background2.png', size=(1432,803), x=numpy.array([0.,0.]))
		self.titleParticles = Particles(all, screen, numpy.array([100.,100.]))
		print "setting fonts"
		self._defaultFont = os.path.join(_mainDir, 'fonts', 'questrial.ttf')#os.path.join(_mainDir, 'fonts', 'freesansbold.ttf')
		self._headerFont = os.path.join(_mainDir, 'fonts', 'fugaz.ttf')#os.path.join(_mainDir, 'fonts', 'freesansbold.ttf')
		self._PlayerFont = pygame.font.Font(self._headerFont, 30)#pygame.font.Font(os.path.join(_mainDir, 'fonts', 'Helvetica.dfont'), 30, bold=True)
		self._PlayerFont.set_underline(1)
		self._SubtitleFont = pygame.font.Font(self._headerFont, 42)#pygame.font.SysFont(os.path.join(_mainDir, 'fonts', 'Helvetica.dfont'), 42, bold=True)
		self._SmallerFont = pygame.font.Font(self._defaultFont, 24)#pygame.font.SysFont(os.path.join(_mainDir, 'fonts', 'Baskerville.ttc'), 16)
		self._LargerFont = pygame.font.Font(self._defaultFont, 60)#pygame.font.SysFont(os.path.join(_mainDir, 'fonts', 'Helvetica.dfont'), 60, bold=True)
		self._TitleFont = pygame.font.Font(self._headerFont, 68)
		print "setting positions"
		self._TitlePos = (100, 20)
		self._SubtitlePos = (100, 120)
		self._PlayerOnePos = (100, 180)
		self._PlayerTwoPos = (500, 180)
		self._StatStartXs = [100, 500]
		self._StatStartY = 200
		self._Title = self._TitleFont.render('Game Over',True,white)
		self._Subtitle = self._SubtitleFont.render('Final Score: {}'.format(self._players.totalScore()),True,white)
		self._PlayerOne = self._PlayerFont.render('Player 1',True,white)
		self._PlayerTwo = self._PlayerFont.render('Player 2',True,white)
		self._PlayerStats = {}
		for index, player in enumerate(self._players):
			if not player.isSuperPlayer:
				self._PlayerStats[index] = [  
					"Time Below HR: {0:.0f}%".format(player.hxm.underThreshold),
					"Times Threshold Crossed: {}".format(player.thresholdCrosses),
					"Threshold HR: {}".format(player.threshold),
					"Average HR: {0:.0f}".format(player.hxm.avgHR),
					"Min HR: {0:.0f}".format(player.hxm.minHR),
					"Max HR: {0:.0f}".format(player.hxm.maxHR),
					"Score: {}".format(player.score),
					"Asteroids Hit: {}".format(player.asteroidsHit),
					"Friends Hit: {}".format(player.friendsHit),
					"Bosses Hit: {}".format(players[0].bossesHit),
					"Hits Taken: {}".format(player.hitsTaken) 
				]			
		print "leaving endingscreen init"
		
	def draw(self):
		#print self._screen.get_size()
		self.background.draw()
		self.titleParticles.move()
		self.titleParticles.draw()
		# self._screen.blit(self._BackButton, self._BackButtonPos)
		self._screen.blit(self._Title, self._TitlePos)
		self._screen.blit(self._Subtitle, self._SubtitlePos)
		self._screen.blit(self._PlayerOne, self._PlayerOnePos)
		self._screen.blit(self._PlayerTwo, self._PlayerTwoPos)
		for p in xrange(len(self._players.players)):
			if p is not 2:
				for index, stat in enumerate(self._PlayerStats[p],1):
					if (index > 6):
						self._screen.blit(self._SmallerFont.render(stat,True,white), (self._StatStartXs[p] + 30, self._StatStartY + 30 * index))			
					else:
						self._screen.blit(self._SmallerFont.render(stat,True,white), (self._StatStartXs[p], self._StatStartY + 30 * index))			

class Particles:

	def __init__ (self, containers, screen, center):
		self._particles = []
		self._containers = containers
		self._screen = screen
		self._center = center
	
	def addParticle(self):
		self._particles.append(Particle(self._center.copy(), self._containers, self._screen))
	
	def move(self):
		if (len(self._particles) < maxParticles):
			self.addParticle()
		for particle in self._particles:
			if particle.alpha <= 0:
				self._particles.remove(particle)
			else:
				particle.move()
	
	def draw (self):
		for particle in self._particles:
			particle.draw()

class Particle (Sprite.Sprite):

	def __init__ (self, loc, containers, screen, alpha=1.):
		v0 = numpy.array([random.uniform(-0.25,0.25), random.uniform(-0.25,0.25)])
		v1 = v0 * particleSpeed
		Sprite.Sprite.__init__(self, containers, screen, imageFile='star.png', size=(20,20), x=loc, v=v1)
		self.alpha = alpha
		# self._surface.set_colorkey((255,255,255))
		self.kill()	# particle don't get to be in any group
	
	def move (self):
		Sprite.Sprite.move(self)
		self._surface.set_alpha(255.*self.alpha)
		self.alpha -= alphaDecay