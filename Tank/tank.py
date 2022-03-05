# import the pygame module, so you can use it
import pygame

from random import randint
import random
import numpy as np

class PointCounter:

	def __init__(self, sizeX, lvl):
		self.counter = 0
		self.high = 0
		self.INCREMENT = 0.67
		self.font = pygame.font.SysFont("Gill Sans", 36)
		self.sizeX = sizeX
		self.lvl = lvl

	#def Update(self, deltaT):
		#self.counter += deltaT * self.INCREMENT
		#if self.counter > self.high:
		#	self.high = self.counter
	def Display(self, screen):		
		text = self.font.render(str(int(len(self.lvl.ennemies))), True, (0, 0, 0))
		screen.blit(text, (self.sizeX - text.get_width() - 20,20)) 
		#if self.high > 0:
		#	text2 = self.font.render("HI " + str(int(self.high)), True, (0, 0, 0))
		#	screen.blit(text2, (self.sizeX - text2.get_width() - 20,20 +  text.get_height()))

class Player:

	def __init__(self, x, y, floor):
		self.mx = x
		self.my = y
		self.img = pygame.image.load("tank.png")
		self.img = pygame.transform.scale(self.img, (3*42, 3*35))
		self.floor = floor
		self.epsilon = 10
		self.jumping = False
		self.V0 = 0
		self.T = 0
		self.G = 20  # Graviatation constant 9.86
		self.JumpV0 = 50 # Vitesse initiale de saut 40
		self.JumpV1 = 90 # Vitesse initiale de saut 70
		self.PV_img = pygame.image.load("heart.png")
		self.MaxPV = 3
		self.PV = self.MaxPV
		self.die = False
		self.q = pygame.image.load("heart.png")
		self.jumpReleased = True
		self.untouchable = False
		self.untouchableFrames = 50
		self.currUntouchableFrames = 0
		self.flickerOnOffFrames = [10,12]
		self.flickerOnOffIndex = 0
		self.currFlickerFrames = 0
		self.displayHitBox = False

	def Display(self, screen):
		screen.blit(self.img, (self.mx,self.my))	

	def Move(self, direction):
		if direction == "right":
			self.mx = self.mx + self.epsilon
		if direction == "left":
			self.mx = self.mx - self.epsilon


	def GetHitbox(self):
		return pygame.Rect(20*3,5*3,11*3,25*3).move(self.mx, self.my)
		

class Ennemy:

	def __init__(self, img, x, y, minX, maxX, minY, maxY, mu, sigma, speedMu, speedSigma):
		self.x = x
		self.y = y
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		self.img = img
		self.displayHitBox = False
		self.mx = 0
		self.my = 0
		self.currentDt = 0
		self.lastChangeDirTime = 0
		self.mu = mu
		self.sigma = sigma
		self.speedMu = speedMu
		self.speedSigma = speedSigma

	def Update(self, deltaT):
		self.x += self.mx * deltaT
		self.y += self.my * deltaT
		if self.x < self.minX:
			self.x = self.minX
		if self.y < self.minY:
			self.y = self.minY
		if self.x > self.maxX:
			self.x = self.maxX
		if self.y > self.maxY:
			self.y = self.maxY
		dt = pygame.time.get_ticks() - self.lastChangeDirTime
		if(dt < self.currentDt):
			return
		self.currentDt = np.random.normal(self.mu, self.sigma)
		self.mx = np.random.normal(self.speedMu, self.speedSigma)
		self.my = np.random.normal(self.speedMu, self.speedSigma)
		self.lastChangeDirTime = pygame.time.get_ticks()
		

	def Display(self, screen):
		screen.blit(self.img, (self.x,self.y))
		if self.displayHitBox == True:
			pygame.draw.rect(screen, (0,255,0), self.GetHitbox())	

	def GetHitbox(self):
		return self.img.get_rect().move(self.x, self.y)

class EnnemyGenerator:

	def __init__(self, img, minX, maxX, minY, maxY, speedMu, speedSigma, minDeltaMs, popMu, popSigma, moveMu, moveSigma):
		self.img = img
		self.minX = minX
		self.maxX = maxX
		self.minY = minY
		self.maxY = maxY
		self.speedMu = speedMu
		self.speedSigma = speedSigma
		self.minDeltaMs = minDeltaMs
		self.popMu = popMu
		self.popSigma = popSigma
		self.moveMu = moveMu
		self.moveSigma = moveSigma
		self.currentDt = 0
		self.lastGenTime = 0
		

	def Next(self):
		dt = pygame.time.get_ticks() - self.lastGenTime
		if(self.minDeltaMs > 0 and dt < self.minDeltaMs):
			return None
		if(dt < self.currentDt):
			return None
		x = randint(self.minX, self.maxX)
		y = randint(self.minY, self.maxY)
		self.currentDt = np.random.normal(self.popMu, self.popSigma)
		self.lastGenTime = pygame.time.get_ticks()
		return Ennemy(self.img, x, y, self.minX, self.maxX, self.minY, self.maxY, self.moveMu, random.uniform(0.01,self.moveSigma), self.speedMu, random.uniform(0.01,self.speedSigma))

class LevelManager:

	def __init__(self, screenSizeX):
		self.ennemies = []
		self.ennemyGen = EnnemyGenerator(pygame.image.load("spider.png"), 0, screenSizeX-100, 10, 400, 0, 0.2, 0, 5000, 4000, 150, 150 )
		

	def Update(self, deltaT):
		r = self.ennemyGen.Next()
		if r is not None:
			self.ennemies.append(r)
		for o in self.ennemies:
			o.Update(deltaT)


	def Display(self, screen):
		for o in self.ennemies:
			o.Display(screen)

	#def IsColliding(self, player):
	#	for o in self.obstacles:
	#		if(o.GetHitbox().colliderect(player.GetHitbox())):
	#			self.obstacles.remove(o)
	#			return True
	#	return False
 
# define a main function
def main():

	#CONSTANTS
	FLOOR_Y = 470
	START_X = 100
	SCREEN_SIZE_X = 800
	SCREEN_SIZE_Y = 600

	 
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	#logo = pygame.image.load("logo32x32.png")
	#pygame.display.set_icon(logo)
	pygame.display.set_caption("tank adventure")
	 
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((SCREEN_SIZE_X,SCREEN_SIZE_Y))
	#screen.fill((100,120,155))

																							#PV = pygame.image.load("heart.png")
	bgd_image = pygame.image.load("fond.jpg")
	tank = Player(START_X,FLOOR_Y,FLOOR_Y)
	clock = pygame.time.Clock()
	lvl = LevelManager(SCREEN_SIZE_X)
	counter = PointCounter(SCREEN_SIZE_X,lvl)
	
	

	gameover = False
	gameoverfont = pygame.font.SysFont("arial", 72)

	 
	# define a variable to control the main loop
	running = True
	 
	# main loop
	while running:

		dt = clock.tick(60) # Max FPS = 60 and get elapsed time since last frame in ms

		screen.blit(bgd_image, (0,0))
		
		keys = pygame.key.get_pressed() 
		if keys[pygame.K_LEFT]:
			tank.Move("left")
		if keys[pygame.K_RIGHT]:
			tank.Move("right")

		# event handling, gets all event from the eventqueue
		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False           

		#counter.Update(dt)
		lvl.Update(dt)

		lvl.Display(screen)
		tank.Display(screen)
		counter.Display(screen)	

		
		pygame.display.flip()

	 
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
#if __name__=="__main__":
	# call the main function
main()


