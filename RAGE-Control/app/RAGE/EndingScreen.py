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

	def __init__(self, screen, thresholdScores=[0,0], players=[]):
		print "reached endingscreen init"
		all = pygame.sprite.RenderUpdates()
		self._screen = screen
		self._players = players
		self.background = Sprite.Sprite(all, screen, imageFile='background.png', size=(1432,803), x=numpy.array([0.,0.]))
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
		# self._BackFont = pygame.font.Font(self._headerFont, 28)
		print "setting positions"
		self._TitlePos = (100, 100)
		self._SubtitlePos = (100, 200)
		self._PlayerOnePos = (100, 300)
		self._PlayerOneThresholdPos = (100, 360)
		self._PlayerOneScorePos = (100, 390)
		self._PlayerOneAsteroidsHitPos = (130, 420)
		self._PlayerOneFriendsHitPos = (130, 450)
		self._PlayerOneBossesHitPos = (130, 480)
		self._PlayerOneHitsTakenPos = (130, 510)
		# self._BackButtonPos = (790, 5)
		# self.hoverBackButton = False
		self._UnselectedColor = white
		self._SelectedColor = yellow
		# self._BackButton = self._BackFont.render('Menu', True, self._UnselectedColor)
		self._Title = self._TitleFont.render('Game Over',True,self._UnselectedColor)
		self._Subtitle = self._SubtitleFont.render('Final Score: {}'.format(self._players.totalScore()),True,self._UnselectedColor)
		self._PlayerOne = self._PlayerFont.render('Player 1',True,self._UnselectedColor)
		self._PlayerOneScore = self._SmallerFont.render('Score: {}'.format(players[0].score),True,self._UnselectedColor)
		self._PlayerOneThreshold = self._SmallerFont.render("Time Below HR: {0:.0f}%".format(thresholdScores[0]/self._players.maxThresholdScore * 100),True,self._UnselectedColor)
		self._PlayerOneAsteroidsHit = self._SmallerFont.render("Asteroids Hit: {}".format(self._players[0].asteroidsHit),True,self._UnselectedColor)
		self._PlayerOneFriendsHit = self._SmallerFont.render("Friends Hit: {}".format(self._players[0].friendsHit),True,self._UnselectedColor)
		self._PlayerOneBossesHit = self._SmallerFont.render("Bosses Hit: {}".format(self._players[0].bossesHit),True,self._UnselectedColor)
		self._PlayerOneHitsTaken = self._SmallerFont.render("Hits Taken: {}".format(self._players[0].hitsTaken),True,self._UnselectedColor)

		if len(self._players.players) > 1:
			self._PlayerTwoPos = (400, 300)
			self._PlayerTwoThresholdPos = (400, 360)
			self._PlayerTwoScorePos = (400, 390)
			self._PlayerTwoAsteroidsHitPos = (430, 420)
			self._PlayerTwoFriendsHitPos = (430, 450)
			self._PlayerTwoBossesHitPos = (430, 480)
			self._PlayerTwoHitsTakenPos = (430, 510)
			self._PlayerTwo = self._PlayerFont.render('Player 2',True,self._UnselectedColor)
			self._PlayerTwoScore = self._SmallerFont.render('Score: {}'.format(players[1].score),True,self._UnselectedColor)
			self._PlayerTwoThreshold = self._SmallerFont.render("Time Below HR: {0:.0f}%".format(thresholdScores[1]/self._players.maxThresholdScore * 100),True,self._UnselectedColor)
			self._PlayerTwoAsteroidsHit = self._SmallerFont.render("Asteroids Hit: {}".format(self._players[1].asteroidsHit),True,self._UnselectedColor)
			self._PlayerTwoFriendsHit = self._SmallerFont.render("Friends Hit: {}".format(self._players[1].friendsHit),True,self._UnselectedColor)
			self._PlayerTwoBossesHit = self._SmallerFont.render("Bosses Hit: {}".format(self._players[0].bossesHit),True,self._UnselectedColor)
			self._PlayerTwoHitsTaken = self._SmallerFont.render("Hits Taken: {}".format(self._players[1].hitsTaken),True,self._UnselectedColor)
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
		self._screen.blit(self._PlayerOneScore, self._PlayerOneScorePos)
		self._screen.blit(self._PlayerOneThreshold, self._PlayerOneThresholdPos)		
		self._screen.blit(self._PlayerOneAsteroidsHit, self._PlayerOneAsteroidsHitPos)
		self._screen.blit(self._PlayerOneFriendsHit, self._PlayerOneFriendsHitPos)
		self._screen.blit(self._PlayerOneBossesHit, self._PlayerOneBossesHitPos)
		self._screen.blit(self._PlayerOneHitsTaken, self._PlayerOneHitsTakenPos)

		if len(self._players.players) > 1:
			self._screen.blit(self._PlayerTwo, self._PlayerTwoPos)
			self._screen.blit(self._PlayerTwoScore, self._PlayerTwoScorePos)
			self._screen.blit(self._PlayerTwoThreshold, self._PlayerTwoThresholdPos)
			self._screen.blit(self._PlayerTwoAsteroidsHit, self._PlayerTwoAsteroidsHitPos)
			self._screen.blit(self._PlayerTwoFriendsHit, self._PlayerTwoFriendsHitPos)
			self._screen.blit(self._PlayerTwoBossesHit, self._PlayerTwoBossesHitPos)
			self._screen.blit(self._PlayerTwoHitsTaken, self._PlayerTwoHitsTakenPos)

	def BackButtonHover(self):
		self.hoverBackButton = True

	def BackButtonLeave(self):
		self.hoverBackButton = False
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