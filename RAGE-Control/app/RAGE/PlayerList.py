import Player, SuperPlayer, pygame, time, datetime, os
from HXMReceiver import *
from IPython import embed

t = datetime.datetime.fromtimestamp(time.time())
d = t.strftime('%Y-%m-%d')
_logDir = os.path.join(os.path.expanduser('~'),'Documents','CALMS-gameplay-logs/{0}/'.format(d))

class PlayerList:
	
	def __init__ (self, containers, screen, players=1, thresholds=(70,70), sound_on=True):
		self._screen = screen
		self._containers = containers
		self._soundOn = sound_on
		self.difficulty = 1.
		self.superPlayerActive = False
		self.hxm = HXMReceiver(minDevices=players)
		self.hxm.run()
		self.players = []
		self.stressedPlayers = []
		self.totalScore()
		for p in range(players):
			self.players.append(Player.Player(containers, screen, self.hxm.devices[p], thresholds[p], self, p, sound_on))
			self.hxm.devices[p].threshold = thresholds[p]
		self.outfile = _logDir + t.strftime('%Y-%m-%d %H.%M.%S') + '.csv'
		f = open(self.outfile, 'w')
		f.write('Start time: {0}, Players: {1}\n'.format(time.time(), players))
		f.close()

	def totalScore(self):
		total = 0
		for player in self.players:
			total += player.score
		return total

	def activateSuperPlayer(self, x):
		self.superPlayerActive = True
		self.players.append(SuperPlayer.SuperPlayer(self._containers, self._screen, self, self._soundOn, x=x))

	def deactivateSuperPlayer(self):
		self.superPlayerActive = False
		self.players.pop()

	def __getitem__(self, key):
		return self.players[key]

	def setDifficulty(self, difficulty):
		self._difficulty = difficulty

	def decel(self, player):
		self.players[player].decel()

	def accel(self, player):
		if len(self.players) > player:
			if player == 2:
				self.players[player].superAccel(self.players[0]._moving * self._difficulty)
			else:
				self.players[player].accel(self._difficulty)
	
	def fire(self, player):
		self.players[player].fire()
		if self.superPlayerActive:
			self.players[2].fire()
	
	def move(self):
		for player in self.players:
			player.move()
			if (len(self.stressedPlayers) > 0):
					player.startCountdown()
			else:
					player.stopCountdown()
	
	def draw(self):
			for index, player in enumerate(self.players):
				if (player.isSuperPlayer and self.superPlayerActive):
					player.draw()
				elif ((not player.isSuperPlayer) and (self.superPlayerActive)):
					player.drawHr(index)
				elif ((not player.isSuperPlayer) and (not self.superPlayerActive)):
					player.draw()
			
	def playerBullets(self):
		bullets = []
		for player in players:
			bullets.append(player.bullets)
		return bullets

	def tellEveryoneImStressed(self, player):
		if player not in self.stressedPlayers:
			self.stressedPlayers.append(player)

	def tellEveryoneImBetter(self, player):
		if player in self.stressedPlayers:
			self.stressedPlayers.remove(player)

	def __del__ (self):
		self.hxm.close()

	def close (self):
		f = open(self.outfile, 'a')
		f.write('End time: {0}, Score: {1}\n'.format(time.time(), self.totalScore()))
		for index, player in enumerate(self.players):
			self.hxm.devices[index].calculate_stats()
			f.write(self.hxm.devices[index].log())
		f.close()
		self.__del__()

