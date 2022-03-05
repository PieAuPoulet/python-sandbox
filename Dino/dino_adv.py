# import the pygame module, so you can use it
import pygame

from random import randint
import random
import numpy as np

class PointCounter:

	def __init__(self, sizeX, lvlmgr):
		self.counter = 0
		self.high = 0
		self.INCREMENT = 0.67
		self.font = pygame.font.SysFont("Gill Sans", 36)
		self.sizeX = sizeX
		self.lvlmgr = lvlmgr

	def Update(self, deltaT):
		self.counter += deltaT * self.INCREMENT
		if self.counter > self.high:
			self.high = self.counter
	def Display(self, screen):		
		text = self.font.render(str(int(self.counter)), True, (0, 0, 0))
		screen.blit(text, (self.sizeX - text.get_width() - 20,20)) 
		if self.high > 0:
			text2 = self.font.render("HI " + str(int(self.high)), True, (0, 0, 0))
			screen.blit(text2, (self.sizeX - text2.get_width() - 20,20 +  text.get_height()))
		text3 = self.font.render("LVL " + str(int(self.lvlmgr.rocGenerator.currentLvl)), True, (0, 0, 0))
		screen.blit(text3, (self.sizeX - text3.get_width() - 20,20 +  text.get_height() +  text2.get_height())) 

class Player:

	def __init__(self, x, y, floor):
		self.mx = x
		self.my = y
		self.img = pygame.image.load("dino2.png")
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

	def IsFlickeringFrame(self):
		if self.untouchable == True:
			self.currUntouchableFrames += 1
			if self.currUntouchableFrames > self.untouchableFrames:
				self.untouchable = False
				self.currUntouchableFrames = 0
				return False
			self.currFlickerFrames += 1
			if self.currFlickerFrames > self.flickerOnOffFrames[self.flickerOnOffIndex]:
				self.currFlickerFrames = 0
				self.flickerOnOffIndex = (self.flickerOnOffIndex+1)%2
			return (self.flickerOnOffIndex == 0)
		else:
			return False


	def Display(self, screen):
		if self.IsFlickeringFrame() == False:
			screen.blit(self.img, (self.mx,self.my))
		if self.displayHitBox == True:
			pygame.draw.rect(screen, (255,0,0), self.GetHitbox())	

	def Move(self, x, y):
		self.mx = x
		self.my = y

	def Jump(self):
		if self.jumping == False:
			self.jumping = True
			self.V0 = self.JumpV0
			self.T = 0
			self.jumpReleased = False
		else:
			#print(self.V0)
			if self.jumpReleased == False and self.V0 < self.JumpV1:
				#print(self.V0)
				self.V0 += 1


	def Update(self, deltaT):
		if self.jumping == True:
			self.T += deltaT
			self.my = self.floor - self.V0 * self.T + 0.5 * self.G * self.T * self.T
			if self.my >= self.floor:
				self.jumping = False
				self.my = self.floor

	def DisplayHP(self, screen):
		for i in range(self.PV): 
			screen.blit(self.q, ( 20 + i * 40, 20))

	def Hit(self):
		if self.untouchable == True:
			return False
		self.PV -= 1
		if(self.PV <= 0):
			return True
		self.untouchable = True
		return False

	def GetHitbox(self):
		return pygame.Rect(20*3,5*3,11*3,25*3).move(self.mx, self.my)
		

class DecoObject:

	def __init__(self, img, x, y, speed):
		self.x = x
		self.y = y
		self.speed = speed
		self.img = img
		self.displayHitBox = False

	def Update(self, deltaT):
		self.x -= deltaT * self.speed

	def Display(self, screen):
		screen.blit(self.img, (self.x,self.y))
		if self.displayHitBox == True:
			pygame.draw.rect(screen, (0,255,0), self.GetHitbox())	

	def GetHitbox(self):
		return self.img.get_rect().move(self.x, self.y)

class DecoObjectGenerator:

	def __init__(self, img, x, minY, maxY, minSpeed, maxSpeed, minDeltaMs, mu, sigma):
		self.img = img
		self.x = x
		self.minY = minY
		self.maxY = maxY
		self.minSpeed = minSpeed
		self.maxSpeed = maxSpeed
		self.minDeltaMs = minDeltaMs
		self.mu = mu
		self.sigma = sigma
		self.currentDt = 0
		self.lastGenTime = 0
		

	def Next(self):
		dt = pygame.time.get_ticks() - self.lastGenTime
		if(self.minDeltaMs > 0 and dt < self.minDeltaMs):
			return None
		if(dt < self.currentDt):
			return None
		y = randint(self.minY, self.maxY)
		speed = random.uniform(self.minSpeed, self.maxSpeed)
		self.currentDt = np.random.normal(self.mu, self.sigma)
		self.lastGenTime = pygame.time.get_ticks()
		return DecoObject(self.img, self.x, y, speed)


class ObstacleGenerator:

	def __init__(self, img, x, minY, maxY):
		self.img = img
		self.x = x
		self.minY = minY
		self.maxY = maxY
		self.pattern1 = [[3000],[100,2000]]
		self.pattern2 = [[1200,300,1000,200,200,1500,2000],[1000,100,200,900,2000],[600,100,2000]]
		self.pattern3 = [[1000,800,900,1000],[200,200,800,1000],[600,800,100,100,700,1000]]
		self.levels = [[10,0,0],[2,7,1],[1,3,6]]
		self.speeds = [0.35,0.45,0.55]
		self.currentLvl = 0
		self.currentIndex = 0
		self.currentPattern = self.pattern1[0]
		self.nblvlpattern = [3,12,8]
		self.currentNblvlpattern = 0
		self.NextPattern()


		self.currentDt = 3000
		self.lastGenTime = 0


	def NextPattern(self):
		sum = self.levels[self.currentLvl][0] + self.levels[self.currentLvl][1] + self.levels[self.currentLvl][2]
		dice = random.random()*sum
		#print(dice)
		if dice < self.levels[self.currentLvl][0]:
			self.currentPattern = self.pattern1[randint(0, len(self.pattern1)-1)]
		elif dice < self.levels[self.currentLvl][0] + self.levels[self.currentLvl][1]:
			self.currentPattern = self.pattern2[randint(0, len(self.pattern2)-1)]
		else:
			self.currentPattern = self.pattern3[randint(0, len(self.pattern3)-1)]
		self.currentIndex = 0
		self.currentNblvlpattern += 1
		if self.currentNblvlpattern > self.nblvlpattern[self.currentLvl]:
			if self.currentLvl < 2 :
				self.currentLvl += 1
				self.currentNblvlpattern = 0
				print(self.currentLvl)
			else:
				self.speeds[self.currentLvl] += 0.065
				print(self.speeds[self.currentLvl])
			
		
		

	def Next(self):
		dt = pygame.time.get_ticks() - self.lastGenTime
		if(dt < self.currentDt):
			return None
		y = randint(self.minY, self.maxY)
		speed = self.speeds[self.currentLvl]
		#print(self.currentPattern)
		#print(self.currentIndex)
		self.currentDt = self.currentPattern[self.currentIndex]
		#print(self.currentDt)
		self.currentIndex += 1
		if self.currentIndex >= len(self.currentPattern):
			self.NextPattern()
		self.lastGenTime = pygame.time.get_ticks()
		return DecoObject(self.img, self.x, y, speed)

class LevelManager:

	def __init__(self, screenSizeX):
		self.obstacles = []
		#self.rocGenerator = DecoObjectGenerator(pygame.transform.scale(pygame.image.load("roc.png"), (3*30, 3*20)), screenSizeX+50, 520, 520, 0.25, 0.25, 800, 1200, 1000 )
		#self.rocGenerator = DecoObjectGenerator(pygame.transform.scale(pygame.image.load("roc.png"), (3*30, 3*20)), screenSizeX+50, 520, 520, 0.25, 0.25, 0, 1800, 800 )
		self.rocGenerator = ObstacleGenerator(pygame.transform.scale(pygame.image.load("roc.png"), (3*30, 3*20)), screenSizeX+50, 520, 520 )
		

	def Update(self, deltaT):
		for o in self.obstacles:
			o.Update(deltaT)
			if(o.x < -100):
				self.obstacles.remove(o)
		r = self.rocGenerator.Next()
		if r is not None:
			self.obstacles.append(r)

	def Display(self, screen):
		for o in self.obstacles:
			o.Display(screen)

	def IsColliding(self, player):
		for o in self.obstacles:
			if(o.GetHitbox().colliderect(player.GetHitbox())):
				self.obstacles.remove(o)
				return True
		return False



class Background:

	def __init__(self, screenSizeX):
		self.decoObjects = []
		self.cloudsGenerator = DecoObjectGenerator(pygame.image.load("cloud.png"), screenSizeX+50, 0, 200, 0.05, 0.1, 3000, 5000, 3000 )
		self.cloudsGenerator2 = DecoObjectGenerator(pygame.image.load("cloud2.png"), screenSizeX+50, 0, 200, 0.05, 0.1, 3000, 5000, 3000 )
		self.treesGenerator = DecoObjectGenerator(pygame.image.load("tree.png"), screenSizeX+50, 410, 410, 0.08, 0.15, 0, 2000, 1000 )
		self.iceGenerator = DecoObjectGenerator(pygame.image.load("ice.png"), screenSizeX+50, 320, 350, 0.08, 0.15, 0, 500, 0 )
		

	def Update(self, deltaT):

		#Bouge tous les nuages vers la gauche
		for o in self.decoObjects:
			o.Update(deltaT)
			if(o.x < -100): # Enleve les nuages qui sont sortis de l ecran
				self.decoObjects.remove(o)
		n = self.cloudsGenerator.Next() 
		m = self.cloudsGenerator2.Next()
		t = self.treesGenerator.Next()
		t2 = self.iceGenerator.Next()


		if n is not None:
			self.decoObjects.append(n)
		if m is not None:
			self.decoObjects.append(m)
		if t is not None:
			self.decoObjects.append(t)
		#if t2 is not None:
		#	self.decoObjects.append(t2)

	def Display(self, screen):
		for o in self.decoObjects:
			o.Display(screen)


 
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
	pygame.display.set_caption("dino adventure")
	 
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((SCREEN_SIZE_X,SCREEN_SIZE_Y))
	#screen.fill((100,120,155))

																							#PV = pygame.image.load("heart.png")
	bgd_image = pygame.image.load("fond.jpg")
	dino = Player(START_X,FLOOR_Y,FLOOR_Y)
	clock = pygame.time.Clock()
	bgd = Background(SCREEN_SIZE_X)
	lvl = LevelManager(SCREEN_SIZE_X)
	counter = PointCounter(SCREEN_SIZE_X, lvl)
	

	gameover = False
	gameoverfont = pygame.font.SysFont("arial", 72)

	 
	# define a variable to control the main loop
	running = True
	 
	# main loop
	while running:

		dt = clock.tick(60) # Max FPS = 60 and get elapsed time since last frame in ms

		screen.blit(bgd_image, (0,0))
		
		keys = pygame.key.get_pressed() 
		if keys[pygame.K_SPACE]:
			dino.Jump()
		else:
			dino.jumpReleased = True

		# event handling, gets all event from the eventqueue
		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False           

			#if event.type == pygame.KEYDOWN:
			#	if event.key == pygame.K_SPACE:
			#	   dino.Jump()
			if event.type == pygame.MOUSEBUTTONUP:
				if gameover == True:
					dino.PV = dino.MaxPV
					counter.counter = 0
					lvl.rocGenerator.currentLvl = 0
					lvl.obstacles.clear()
					gameover = False


		if(gameover == True):
			dino.Update(dt/100)
			bgd.Display(screen)
			lvl.Display(screen)
			dino.Display(screen)
			dino.DisplayHP(screen)		
			counter.Display(screen)
			text = gameoverfont.render("GAME OVER", True, (255, 0, 0))
			screen.blit(text, (SCREEN_SIZE_X*0.5 - text.get_width(),SCREEN_SIZE_Y*0.5)) 
		else:
			bgd.Update(dt)
			dino.Update(dt/100)
			counter.Update(dt)
			lvl.Update(dt)

			bgd.Display(screen)
			lvl.Display(screen)
			dino.Display(screen)
			dino.DisplayHP(screen)		
			counter.Display(screen)
		
			if(lvl.IsColliding(dino)):
				if(dino.untouchable == False):
					screen.fill((128,0,0))
				if(dino.Hit()):
					gameover = True



		

		
		pygame.display.flip()

	 
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
#if __name__=="__main__":
	# call the main function
main()


