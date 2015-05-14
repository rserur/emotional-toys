#!/usr/bin/env python

import pygame, sys
from pygame.locals import *
import RAGE.Player_M, RAGE.Background, RAGE.Villians, RAGE.Friends, RAGE.HUD_M
from numpy import array
import game0

def input(events, player):
	for event in events: 
		if event.type == QUIT: 
			sys.exit(0) 
		elif (event.type == KEYDOWN) and (event.key == K_ESCAPE):
			sys.exit(0)
		elif event.type == KEYDOWN:
			keystate = pygame.key.get_pressed()
			a0 = float(keystate[K_RIGHT]-keystate[K_LEFT])
			a1 = float(keystate[K_d]-keystate[K_a])
			if keystate[K_SPACE] or keystate[K_UP]:
				player.fire()
			player.accel([a0, 0.])
			#players.accel(1, [a1, 0.])


def gameLoop():
	#containers?
	all = pygame.sprite.RenderUpdates()

	#game resources
	player = RAGE.Player_M.Player_M(all, screen)
	villians = RAGE.Villians.Villians(all, screen)
	friends = RAGE.Friends.Friends(all, screen)
	background = RAGE.Background.Background(screen)
	hud = RAGE.HUD_M.HUD_M(screen)
	
	#main loop
	while True: 
		villians.newVillian()
		friends.newFriend()
		
		#hud.setMessages(hr=str(player.hxm.HR))
		hud.setMessages(bullets=str(player.hxm.bullets))
		# print player.hxm.HR
		
		input(pygame.event.get(), player)
		
		if (game0.detectBVCollisions(player.bullets, villians)):
			player.changeScore(100)
			hud.setMessages(score=str(player.score))
		game0.detectBFCollisions(player.bullets, friends)
		game0.detectPVCollisions(player, villians)
		game0.detectFVCollisions(friends, villians)
		
		player.move()
		friends.move()
		villians.move()
		background.draw()
		hud.draw()
		villians.draw()
		friends.draw()
		player.draw()
		pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	window = pygame.display.set_mode((game0.WIDTH, game0.HEIGHT)) 
	pygame.display.set_caption('RAGE-M')
	screen = pygame.display.get_surface()
	gameLoop() 