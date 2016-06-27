#!/usr/bin/env python2.7

import pygame, sys, time, random
from pygame.locals import *
import RAGE.PlayerList, RAGE.Player, RAGE.Background, RAGE.Villians, RAGE.Bosses, RAGE.Friends, RAGE.HUD, RAGE.IntroScreen, RAGE.TutorialScreen, RAGE.Sounds, RAGE.SuperZone, RAGE.EndingScreen
from numpy import array


WIDTH =  900 #1080 # 720  # 1024 screen size effects gameplay dramatically-- too big = too easy; not enough enemy density
HEIGHT =  600 #607 # 405 # 800
SCREENRECT     = Rect(0, 0, WIDTH, 550)

GAME_LENGTH = 180 # seconds
USE_DIFFICULTY = 1 # set to 0 to not reverse directions at 1 min remain
THRESHOLD_GOAL = 1400

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


def mouseInput(events):
  for event in events:
    if event.type == MOUSEMOTION:
      mousepos = pygame.mouse.get_pos()
      return {'MOUSEMOVE': mousepos}
    if event.type == MOUSEBUTTONDOWN:
      if (pygame.mouse.get_pressed()[0] == 1):
        return {'MOUSEPRESS': pygame.mouse.get_pressed()[0]}
    if event.type == QUIT: 
      sys.exit(0)
  return False

def input(events, players, shooting=True):

  for event in events:
    if event.type in (KEYUP, KEYDOWN):
      keystate = pygame.key.get_pressed()
      players[0]._moving = int(keystate[K_RIGHT]-keystate[K_LEFT])
      players[1]._moving = int(keystate[K_d]-keystate[K_a])
      if shooting:
        if (keystate[K_SPACE] or keystate[K_UP]):
          players.fire(0)
        if keystate[K_w]:
          players.fire(1)
      if keystate[K_ESCAPE]:
        players.close()
        sys.exit(0)
      players.accel(0)
      players.accel(1)
    elif (event.type == JOYBUTTONDOWN and shooting):
      if (event.button == A_BUTTON) or (event.button == B_BUTTON):
        players.fire(event.joy)
    elif (event.type == JOYAXISMOTION) and (event.axis == LEFT_RIGHT_AXIS):
        players[event.joy]._moving = int(event.value)
        players.accel(event.joy)
    elif event.type == QUIT:
      players.close()
      sys.exit(0)

  if players.superPlayerActive:
    if (players[0]._moving == players[1]._moving):
      if ((int(players[0]._moving) == 0) or (int(players[1]._moving) == 0)):
        players.decel(2)
      else:
        players.accel(2)

  return mouseInput(events)
    
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
            # boss.deadFriends += 1
            # if(boss.deadFriends == boss.maxKills):
            #   bosses.explode(boss)
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
          bullets1.remove(bullet)
          bullet.kill()
          break
      except:
        pass
    for bullet in bullets2:
      try:
        bulletSize = array(bullet.getSize())
        bossSize = array(boss.getSize())
        if detectHit(bullet._x, bulletSize, boss._x, bossSize):
          p2hit = True
          bullets2.remove(bullet)
          bullet.kill()
          break
      except:
        pass
    if (p1hit and p2hit):
      bosses.explode(boss)
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
  
def superZoning(players, superzone):  
  superZoneSize = array(superzone.getSize())
  superZoners = 0
  for player in players:
    playerSize = array(player.getSize())
    if detectHit(player._x, playerSize, superzone._x, superZoneSize):
      superZoners +=1
  if superZoners == 2:
    return 1
  else:
    return 0

def introLoop():
  screen = pygame.display.get_surface()
  background = RAGE.Background.Background(screen)
  introScreen = RAGE.IntroScreen.IntroScreen(screen)
  sound_on = True
  while True:
    action = mouseInput(pygame.event.get())
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
    
    background.draw()
    introScreen.draw()
    pygame.display.flip()

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
      action = input(pygame.event.get(), players, shooting=False)
    else:
      action = input(pygame.event.get(), players)
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
  friends = RAGE.Friends.Friends(all, screen, sound_on)
  sounds = RAGE.Sounds.Sounds()
  background = RAGE.Sprite.Sprite(all, screen, imageFile='background.png', size=(1432,803), x=array([0.,0.]))
  hud = RAGE.HUD.HUD(all, screen)
  superzone = RAGE.SuperZone.SuperZone(all, screen)
  superCrashLimit = 5
  superZoningTime = 0
  
  #start time
  startTime = time.clock()
  
  # main loop
  while ((time.clock()-startTime) < GAME_LENGTH): 
    villians.newVillian()
    friends.newFriend()
    if(len(players.players) > 1 and (time.clock()-startTime) > 0 and random.randint(1, 400) == 77):
      bosses.newBoss()

    players.setDifficulty(1.)
    players.changeMaxThresholdScore(1.)
    if (hud.clock.time() < 60):
      players.setDifficulty(-1.)
    
    action = input(pygame.event.get(), players)

    if(action):
      if ('MOUSEMOVE' in action):
        r = hud._BackButton.get_rect()
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
          player.changeScore(200)
        else:
          player.changeScore(100)
        player.asteroidsHit += 1
      deadFriends = detectBFCollisions(player.bullets, friends)
      if detectPVBCollisions(player, villians, bosses):
        player.changeScore(-100)
        player.hitsTaken += 1
        if players.superPlayerActive:
          superCrashLimit -= 1
        hud.setMessages(flash='PLAYER HIT! -100',flashType='bad')
      if (deadFriends > 0):
        player.friendsHit += 1
        hud.setMessages(flash='FRIEND HIT! -100',flashType='bad')
        player.changeScore(deadFriends * -100)
      if player.isSuperPlayer is False:
        hud.updateHeartMeter(player)
        if (player.stressed is not True):
          player.changeTotalThresholdScore(1.)
        if (player.stressed is not True) and player.thresholdScore < 700:
          player.changeThresholdScore(1)
        elif (player.stressed is True and players.superPlayerActive is False):
          player.wipeThresholdScore()         

    if(len(players.players) == 2):
      if ((players[0].thresholdScore + players[1].thresholdScore) == THRESHOLD_GOAL):
        if (sound_on and not superzone._active):
          sounds.OpenSuperZone()
        superzone._active = True
      else:
        superzone._active = False
      if(detectBBCollisions(players[0].bullets, players[1].bullets, bosses)) :
        player.changeScore(500)
        hud.setMessages(flash='METEOR DEFLECTED! +500', flashType='good')
        players[0].bossesHit += 1
        if (sound_on):
          sounds.SuccessStart()
      if superzone._active:
        if superZoning(players, superzone) == 1:
          superZoningTime += 1
        else: 
          superZoningTime = 0
        if 0 < superZoningTime < 30:
          hud.setMessages(flash='HOLD STEADY...', flashType='good')
        elif superZoningTime == 30:
          superZoningTime = 0
          players.activateSuperPlayer(superzone._x[0])
          hud.setMessages(flash='SUPERPLAYER ACTIVATED! +500', flashType='good')
          players[2].changeScore(500)
          players[2].entrance()
    if(len(players.players) > 1):
      thresholdScores = [players[0].totalThresholdScore, players[1].totalThresholdScore]
    else:
      thresholdScores = [players[0].totalThresholdScore]
    detectFVCollisions(friends, villians)
    detectFBCollisions(friends, bosses)
    hud.setMessages(score=str(players.totalScore()))

    if players.superPlayerActive:
      superzone._active = False
      if (detectSBBCollisions(players[2].bullets, bosses)):
        players[2].changeScore(500)
        players[0].bossesHit += 1
        hud.setMessages(flash='METEOR DEFLECTED! +500', flashType='good')
        if (sound_on):
          sounds.SuccessStart()
      if superCrashLimit == 0:
        players.deactivateSuperPlayer()
        if (sound_on):
          sounds.SuperPlayerSplit()
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
  endingLoop(thresholdScores, players)
    
def endingLoop(thresholdScores, players):
  screen = pygame.display.get_surface()
  background = RAGE.Background.Background(screen)
  endingScreen = RAGE.EndingScreen.EndingScreen(screen, thresholdScores=thresholdScores, players=players)

  while True:
    background.draw()
    endingScreen.draw()
    pygame.display.flip() 

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




