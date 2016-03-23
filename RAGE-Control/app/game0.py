#!/usr/bin/env python2.7

import pygame, sys, time, os, random
from pygame.locals import *
import RAGE.PlayerList, RAGE.Player, RAGE.Background, RAGE.Villians, RAGE.Bosses, RAGE.Friends, RAGE.HUD, RAGE.IntroScreen, RAGE.TutorialScreen, RAGE.Sounds, RAGE.SuperZone
from numpy import array


WIDTH =  900 #1080 # 720  # 1024 screen size effects gameplay dramatically-- too big = too easy; not enough enemy density
HEIGHT =  600 #607 # 405 # 800
SCREENRECT     = Rect(0, 0, WIDTH, 550)

GAME_LENGTH = 180 # seconds
USE_DIFFICULTY = 1 # set to 0 to not reverse directions at 1 min remain

A_BUTTON = 1
B_BUTTON = 2
START_BUTTON = 9
SELECT_BUTTON = 8
UP_DOWN_AXIS = 4
UP_VALUE = -1
DOWN_VALUE = 1
LEFT_RIGHT_AXIS = 3
LEFT_DIRECTION = -0.5
RIGHT_DIRECTION = 0.5

def introInput(events):
	for event in events: 
		#print event
		if event.type == MOUSEMOTION:
			mousepos = pygame.mouse.get_pos()
			return {'MOUSEMOVE': mousepos}
		if event.type == MOUSEBUTTONDOWN:
			if (pygame.mouse.get_pressed()[0] == 1):
				return {'MOUSEPRESS': pygame.mouse.get_pressed()[0]}
		if event.type == QUIT: 
			sys.exit(0)
	return False

def input(hud, events, players, difficulty=None, shooting=True, tutorial=False): 

	accel_modifier = 1.
	if (difficulty == 1):
		accel_modifier = -1.
	for event in events: 
		if event.type == QUIT: 
			players.close()
			sys.exit(0) 
		elif (event.type == KEYDOWN) and (event.key == K_ESCAPE):
			players.close()
			sys.exit(0)
		# elif (event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
		# 	r = hud._BackButton.get_rect()
		# 	m = pygame.mouse.get_pos()
		# 	if detectHit(hud._BackButtonPos, r.bottomright, m, (0,0,)):
		# 		players.close()
		# 		return True
		elif event.type == KEYDOWN:
			keystate = pygame.key.get_pressed()
			a0 = float(keystate[K_RIGHT]-keystate[K_LEFT])
			a1 = float(keystate[K_d]-keystate[K_a])
			if (keystate[K_SPACE] or keystate[K_UP]) and shooting:
				players.fire(0)
				players.fire(2)
			if keystate[K_w] and shooting:
				players.fire(1)
				players.fire(2)
			players.accel(0, [a0 * accel_modifier, 0.])
			players.accel(1, [a1 * accel_modifier, 0.])
			players.accel(2, [(a0 + a1) * accel_modifier, 0.])
		elif (event.type == JOYBUTTONDOWN and shooting):
			if (event.button == A_BUTTON) and (event.joy == 0):
				players.fire(0)
				players.fire(2)
			if (event.button == B_BUTTON) and (event.joy == 0):
				players.fire(0)
				players.fire(2)
			if (event.button == A_BUTTON) and (event.joy == 1):
				players.fire(1)
				players.fire(2)
			if (event.button == B_BUTTON) and (event.joy == 1):
				players.fire(1)
				players.fire(2)
		elif (event.type == JOYAXISMOTION):
			a0 = float(0)
			a1 = float(0)
			if (event.axis == LEFT_RIGHT_AXIS) and (event.joy == 0):
				a0 = event.value
			elif (event.axis == LEFT_RIGHT_AXIS) and (event.joy == 1):
				a1 = event.value
			players.accel(0, [a0 * accel_modifier, 0.])
			players.accel(1, [a1 * accel_modifier, 0.])
			players.accel(2, [(a0 + a1) * accel_modifier, 0.])
		return introInput(events)
		#else: 
		#	print event
		 
def detectHit(box1Pos, box1Size, box2Pos, box2Size):
	if ((box1Pos[0] <= box2Pos[0] + box2Size[0]) and 
		(box1Pos[0] + box1Size[0] >= box2Pos[0]) and
		(box1Pos[1] <= box2Pos[1] + box2Size[1]) and
		(box1Pos[1] + box1Size[1] >= box2Pos[1])):
		return True
	return False

def checkBullet(bullet, boss):
	bulletPos = bullet._x
	bulletSize = bullet.getSize()
	bossPos = boss._x
	bossSize = boss.getSize()
	if ((bulletPos[1] + bulletSize[1]) > (bossSize[1]*.75 + bossPos[1])):
		return True
	return False

def detectFVCollisions(friends, villians):
	deadFriends = 0
	for friend in friends.friendList:
		for villian in villians.villianList:
			try:
				friendSize = array(friend.getSize())
				villianSize = array(villian.getSize())
				if detectHit(friend._x, friendSize, villian._x, villianSize):
					friend._wobble += 0.7
					if friend._wobble >= 1:
						friends.explode(friend)
						deadFriends += 1
					villians.explode(villian)
			except:
				pass
	return deadFriends

def detectFBCollisions(friends, bosses):
	deadFriends = 0
	for friend in friends.friendList:
		for boss in bosses.bossList:
			try:
				friendSize = array(friend.getSize())
				bossSize = array(boss.getSize())
				if detectHit(friend._x, friendSize, boss._x, bossSize):
					friend._wobble += 0.7
					if friend._wobble >= 1:
						friends.explode(friend)
						deadFriends += 1
						boss.deadFriends += 1
						if(boss.deadFriends == boss.maxKills):
							bosses.explode(boss)
			except:
				pass
	return deadFriends

def detectBVCollisions(bullets, villians):
	for bullet in bullets:
		for villian in villians.villianList:
			try:
				bulletSize = array(bullet.getSize())
				villianSize = array(villian.getSize())
				if detectHit(bullet._x, bulletSize, villian._x, villianSize):
					bullets.remove(bullet)
					bullet.kill()
					villians.explode(villian)
					return True
			except:
				pass

def detectBBCollisions(bullets1, bullets2, bosses):
	p1hit = False
	p2hit = False
	impact_bullets = []

	for boss in bosses.bossList:
		for bullet in bullets1:
			try:
				bulletSize = array(bullet.getSize())
				bossSize = array(boss.getSize())
				if detectHit(bullet._x, bulletSize, boss._x, bossSize):
					p1hit = True
					#if (checkBullet(bullet, boss)):
					bullets1.remove(bullet)
					bullet.kill()
					#else:
					#	impact_bullets[0] = [True, bullet]
					break
			except:
				pass
		for bullet in bullets2:
			try:
				bulletSize = array(bullet.getSize())
				bossSize = array(boss.getSize())
				if detectHit(bullet._x, bulletSize, boss._x, bossSize):
					p2hit = True
					#if (checkBullet(bullet, boss)):
					bullets2.remove(bullet)
					bullet.kill()
					#else:
					#	impact_bullets[1] = [True, bullet]
					break
			except:
				pass
		if (p1hit and p2hit):
			bosses.explode(boss)
			# if (impact_bullets[0][0]):
			# 	bullets1.remove(impact_bullets[0][1])
			# 	impact_bullets[0][1].kill()
			# if (impact_bullets[1][0]):
			# 	bullets1.remove(impact_bullets[1][1])
			# 	impact_bullets[1][1].kill()
			return True

def detectSBBCollisions(superbullets, bosses):
	superhit = False

	for boss in bosses.bossList:
		for bullet in superbullets:
			try:
				bulletSize = array(bullet.getSize())
				bossSize = array(boss.getSize())
				if detectHit(bullet._x, bulletSize, boss._x, bossSize):
					superhit = True
					bullets1.remove(bullet)
					bullet.kill()
					break
			except:
				pass
		if (superhit):
			bosses.explode(boss)
			return True

def detectBFCollisions(bullets, friends):
	deadFriends = 0
	for bullet in bullets:
		for friend in friends.friendList:
			try:
				bulletSize = array(bullet.getSize())
				friendSize = array(friend.getSize())
				if detectHit(bullet._x, bulletSize, friend._x, friendSize):
					bullets.remove(bullet)
					bullet.kill()
					friend._wobble += 0.7
					if friend._wobble >= 1:
						friends.explode(friend)
						deadFriends += 1
			except:
				pass
	return deadFriends

def detectPVBCollisions(player, villians, bosses):
	villianCrashes = 0
	for villian in villians.villianList:
		playerSize = array(player.getSize())
		villianSize = array(villian.getSize())
		if detectHit(player._x, playerSize, villian._x, villianSize):
			villians.explode(villian)
			villianCrashes += 1
			if (villian._x[0] > player.getCenter()[0]):
				player._v -= array([20,0])
			else:
				player._v += array([20,0])
	for boss in bosses.bossList:
		playerSize = array(player.getSize())
		bossSize = array(boss.getSize())
		if detectHit(player._x, playerSize, boss._x, bossSize):
			bosses.explode(boss)
			villianCrashes += 1
			if (boss._x[0] > boss.getCenter()[0]):
				player._v -= array([30,0])
			else:
				player._v += array([30,0])
	if villianCrashes > 0:
		return True
	
def detectSuperZone(player, superzone):	
	superZoneSize = array(superzone.getSize())
	playerSize = array(player.getSize())
	if detectHit(player._x, playerSize, superzone._x, superZoneSize):
		if (superzone._x[0] > player.getCenter()[0]):
			return True

def introLoop():
	screen = pygame.display.get_surface()
	background = RAGE.Background.Background(screen)
	introScreen = RAGE.IntroScreen.IntroScreen(screen)
	sound_on = True
	while True:
		action = introInput(pygame.event.get())
		if (action):
			if ('MOUSEMOVE' in action):
				r1 = introScreen._OnePlayer.get_rect()
				if detectHit(introScreen._OnePlayerPos, r1.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.OnePHover()
				else:
					if (introScreen.hover1P):
						introScreen.OnePLeave()
				r2 = introScreen._TwoPlayer.get_rect()
				if detectHit(introScreen._TwoPlayerPos, r2.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.TwoPHover()
				else:
					if (introScreen.hover2P):
						introScreen.TwoPLeave()
				r = introScreen.P1Up.get_rect()
				if detectHit(introScreen._1pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P1Up.highlight()
				else:
					introScreen.P1Up.unhighlight()
				r = introScreen.P1Down.get_rect()
				if detectHit(introScreen._1pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P1Down.highlight()
				else:
					introScreen.P1Down.unhighlight()
				r = introScreen.P2Up.get_rect()
				if detectHit(introScreen._2pUpArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P2Up.highlight()
				else:
					introScreen.P2Up.unhighlight()
				r = introScreen.P2Down.get_rect()
				if detectHit(introScreen._2pDownArrowPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.P2Down.highlight()
				else:
					introScreen.P2Down.unhighlight()
				r = introScreen.SoundIcon.get_rect()
				if detectHit(introScreen._SoundPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.hoverSound = True
				else:
					introScreen.hoverSound = False
				r = introScreen._Tutorial.get_rect()
				if detectHit(introScreen._TutorialPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					introScreen.TutorialHover()
				else:
					if introScreen.hoverTutorial:
						introScreen.TutorialLeave()
			if ('MOUSEPRESS' in action):
				if introScreen.hover1P:
					return 1, (introScreen.P1Threshold, introScreen.P2Threshold), sound_on
				if introScreen.hover2P:
					return 2, (introScreen.P1Threshold, introScreen.P2Threshold), sound_on
				if introScreen.hoverSound:
					sound_on = introScreen.ToggleMute(sound_on)
				if introScreen.P1Up.selected:
					introScreen.IncrementThreshold(player=1)
				if introScreen.P1Down.selected:
					introScreen.IncrementThreshold(player=1,incVal=-1)
				if introScreen.P2Up.selected:
					introScreen.IncrementThreshold(player=2)
				if introScreen.P2Down.selected:
					introScreen.IncrementThreshold(player=2,incVal=-1)
				if introScreen.hoverTutorial:
					tutorialLoop(sound_on)
		
				#print items_hit
		background.draw()
		introScreen.draw()
		pygame.display.flip()

# this function and related calls will need to be transferred over to the non-app version
def tutorialLoop(sound_on = True):
	screen = pygame.display.get_surface()
	all = pygame.sprite.RenderUpdates()
	background = RAGE.Background.Background(screen)
	tutorialScreen = RAGE.TutorialScreen.TutorialScreen(screen)
	hud = RAGE.HUD.HUD(all, screen)
	players = RAGE.PlayerList.PlayerList(all, screen, sound_on=sound_on)
	villians = RAGE.Villians.Villians(all, screen, sound_on)
	friends = RAGE.Friends.Friends(all, screen)
	bosses = RAGE.Bosses.Bosses(all, screen, sound_on)

	gamepads = []
	for i in range(pygame.joystick.get_count()):
		gamepads.append(pygame.joystick.Joystick(i))
		pygame.joystick.Joystick(i).init()

	while(tutorialScreen.step < tutorialScreen.numSteps):
		if (tutorialScreen.step < 2):
			action = input(hud, pygame.event.get(), players, shooting=False)
		else:
			action = input(hud, pygame.event.get(), players)
		# getNext(action, tutorialScreen)
		if (action):
			if ('MOUSEMOVE' in action):
				r = tutorialScreen._ButtonText.get_rect()
				if detectHit(tutorialScreen._ButtonPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					tutorialScreen.ButtonHover()
				else:
					if (tutorialScreen.hoverButton):
						tutorialScreen.ButtonLeave()
			elif ('MOUSEPRESS' in action):
				if (tutorialScreen.hoverButton):
					tutorialScreen.step += 1
		if (tutorialScreen.step > 0):
			for player in players.players:
				if (detectBVCollisions(player.bullets, villians)):
					players[0].changeScore(100)
				detectPVBCollisions(player, villians, bosses)
				deadFriends = detectBFCollisions(player.bullets, friends)
			deadFriends += detectFVCollisions(friends, villians)
			deadFriends += detectFBCollisions(friends, bosses)
			if(tutorialScreen.step > 3):
				players[0].changeScore(deadFriends * -100)
			hud.setMessages(score=str(players[0].score))
		players.move()
		background.draw()
		hud.draw(len(players.players))
		tutorialScreen.draw()
		if (tutorialScreen.step > 0):
			villians.newVillian()
			villians.move()
			villians.draw()
		if (tutorialScreen.step > 2):
			friends.newFriend()
			friends.move()
			friends.draw()
		if (tutorialScreen.step > 4):
			bosses.newBoss()
			bosses.move()
			bosses.draw()
		players.draw()
		pygame.display.flip()

	players.close()

def gameLoop(players=1, thresholds=(70, 70), sound_on=True):
	print "in game loop"
	screen = pygame.display.get_surface()
	
	#containers?
	all = pygame.sprite.RenderUpdates()
	
	#gamepads
	gamepads = []
	for i in range(pygame.joystick.get_count()):
		gamepads.append(pygame.joystick.Joystick(i))
		pygame.joystick.Joystick(i).init()

	#game resources
	players = RAGE.PlayerList.PlayerList(all, screen, players, thresholds, sound_on)
	villians = RAGE.Villians.Villians(all, screen, sound_on)
	bosses = RAGE.Bosses.Bosses(all, screen, sound_on)
	friends = RAGE.Friends.Friends(all, screen)
	sounds = RAGE.Sounds.Sounds()
	background = RAGE.Sprite.Sprite(all, screen, imageFile='background.png', size=(1432,803), x=array([0.,0.]))
	hud = RAGE.HUD.HUD(all, screen)
	superzone = RAGE.SuperZone.SuperZone(all, screen)
	superZoners = 0
	superCrashLimit = 5
	
	#start time
	startTime = time.clock()
	
	# main loop
	while ((time.clock()-startTime) < GAME_LENGTH): 
		villians.newVillian()
		friends.newFriend()
		if(len(players.players) > 1 and (time.clock()-startTime) > 0 and random.randint(1, 500) == 77):
			bosses.newBoss()
		
		difficulty = 0
		if (hud.clock.time() < 60):
			difficulty = 1
		
		action = input(hud, pygame.event.get(), players, difficulty * USE_DIFFICULTY)
		if(action):
			if ('MOUSEMOVE' in action):
				r = hud._BackButton.get_rect()
				m = pygame.mouse.get_pos()
				if detectHit(hud._BackButtonPos, r.bottomright, action['MOUSEMOVE'], (0,0)):
					hud.BackButtonHover()
				else:
					if (hud.hoverBackButton):
						hud.BackButtonLeave()
			elif ('MOUSEPRESS' in action):
				if hud.hoverBackButton:
					players.close()
					return True
		
		for player in players.players:
			if (detectBVCollisions(player.bullets, villians)):
				if players.superPlayerActive:
					players[0].changeScore(200)
				else:
					players[0].changeScore(100)
				#hud.setMessages(score=str(player.score))
			deadFriends = detectBFCollisions(player.bullets, friends)
			if detectPVBCollisions(player, villians, bosses):
				players[0].changeScore(-100)
				if players.superPlayerActive:
					superCrashLimit -= 1
				hud.setMessages(flash='PLAYER HIT! -100',flashType='bad')
			if (deadFriends > 0):
				hud.setMessages(flash='FRIEND HIT! -100',flashType='bad')
			if player.isSuperPlayer is False:
				hud.updateHeartMeter(player)
				if (player.stressed is not True) and player.thresholdScore < 1000:
					player.changeThresholdScore(1)
				elif (player.stressed is True):
					player.wipeThresholdScore()					
					# sounds.PowerDown()

		if(len(players.players) == 2):
			if ((players[0].thresholdScore + players[1].thresholdScore) >= 2000):
				superzone._active = True
			else:
				superzone._active = False
			if(detectBBCollisions(players[0].bullets, players[1].bullets, bosses)) :
				players[0].changeScore(500)
				hud.setMessages(flash='METEOR DEFLECTED! +500', flashType='good')
				if (sound_on):
					sounds.SuccessStart()
			if superzone._active:
				if (detectSuperZone(player, superzone)):
						superZoners += 1
				if (superZoners == 2 and (not players.superPlayerActive)):
					superZoners = 0
					players.activateSuperPlayer(superzone._x[0])
					hud.setMessages(flash='SUPERPLAYER ACTIVATED! +500', flashType='good')
					players[0].changeScore(500)
					players[2].entrance()
		detectFVCollisions(friends, villians)
		detectFBCollisions(friends, bosses)
		players[0].changeScore(deadFriends * -100)
		hud.setMessages(score=str(players[0].score))

		if players.superPlayerActive:
			superzone._active = False
			if (detectSBBCollisions(players[2].bullets, bosses)):
				players[0].changeScore(500)
				hud.setMessages(flash='METEOR DEFLECTED! +500', flashType='good')
				if (sound_on):
					sounds.SuccessStart()
			if superCrashLimit == 0:
				players.deactivateSuperPlayer()
				hud.setMessages(flash='TOO MANY HITS! SUPERPLAYER DEACTIVATED', flashType='bad')
				superCrashLimit = 5
				players[0].wipeThresholdScore()					
				players[1].wipeThresholdScore()					
			
		players.move()
		friends.move()
		villians.move()
		bosses.move()
		background.draw()
		friends.draw()
		villians.draw()
		bosses.draw()
		players.draw()
		superzone.draw()
		hud.draw(len(players.players))
		pygame.display.flip()

	players.close()
		
def startGame():
	players, thresholds, sound_on = introLoop()
	return gameLoop(players, thresholds, sound_on)

if __name__ == '__main__':
	pygame.init()
	window = pygame.display.set_mode((WIDTH, HEIGHT)) 
	pygame.display.set_caption('CALMS: The Game')
	screen = pygame.display.get_surface()
	status = startGame()
	while(status == True):
		status = startGame()




