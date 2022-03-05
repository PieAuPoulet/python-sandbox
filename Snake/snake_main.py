# import the pygame module, so you can use it
import pygame
from random import randint
import random

class Snake:
	def __init__(self, color, x, y, radius, minX, minY, maxX, maxY, image):
		self.color = color
		self.x = x
		self.y = y
		self.radius = radius
		self.direction = "RIGHT"
		self.minX = minX
		self.minY = minY
		self.maxX = maxX
		self.maxY = maxY
		self.balls = []
		self.currentBallNumber = 0
		self.OrigImage = image
		self.OrigImage.set_colorkey((255,255,255))
		self.image = image

	def UpdateNumber(self, number):
		self.number = number

	def UpdateMove(self):
		if self.direction == "UP":
			self.UpdateUp()
		if self.direction == "DOWN":
			self.UpdateDown()
		if self.direction == "LEFT":
			self.UpdateLeft()
		if self.direction == "RIGHT":
			self.UpdateRight()
		for b in self.balls:
			if b.x == self.x and b.y == self.y:
				return True
		return False

	def Roll(self):
		if len(self.balls) > 1:			
			n = len(self.balls)-1
			for i in range(0, n):
				k = n-i
				self.balls[k].x = self.balls[k-1].x
				self.balls[k].y = self.balls[k-1].y
		if len(self.balls) > 0:	
			self.balls[0].x = self.x
			self.balls[0].y = self.y

	def TakeBall(self, b):
		if b.number == self.currentBallNumber + 1:
			self.balls.append(b)
			self.currentBallNumber = self.currentBallNumber + 1
			print("Nb balls",len(self.balls))
			return True
		else:
			return False

	def UpdateUp(self):
		self.Roll()
		if self.y == self.minY:
			updated = self.UpdateDirection("RIGHT")
			if updated == True:
				self.UpdateRight()
		else:
			self.y = self.y - self.radius * 2

	def UpdateDown(self):
		self.Roll()
		if self.y == self.maxY:
			updated = self.UpdateDirection("LEFT")
			if updated == True:
				self.UpdateLeft()
		else:
			self.y = self.y + self.radius * 2

	def UpdateLeft(self):
		self.Roll()
		if self.x == self.minX:
			updated = self.UpdateDirection("UP")
			if updated == True:
				self.UpdateUp()
		else:
			self.x = self.x - self.radius * 2

	def UpdateRight(self):
		self.Roll()
		if self.x == self.maxX:
			updated = self.UpdateDirection("DOWN")
			if updated == True:
				self.UpdateDown()
		else:
			self.x = self.x + self.radius * 2

	def UpdateDirection(self, direction):
		if direction == "DOWN":
			if self.direction == "UP":
				return False
			self.image = pygame.transform.rotate(self.OrigImage, -90)
		if direction == "LEFT":
			if self.direction == "RIGHT":
				return False
			self.image = pygame.transform.flip(self.OrigImage, True, False)
		if direction == "UP":
			if self.direction == "DOWN":
				return False
			self.image = pygame.transform.rotate(self.OrigImage, 90)
		if direction == "RIGHT":
			if self.direction == "LEFT":
				return False
			self.image = self.OrigImage
		self.direction = direction
		return True

	def Display(self, screen):
		for o in self.balls:
			o.Display(screen)
		#pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
		#pygame.draw.rect(screen, self.color, (self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2))

		screen.blit(self.image, (self.x-self.radius, self.y-self.radius))
		

class Ball:

	def __init__(self, color, x, y, radius):
		self.color = color
		self.x = x
		self.y = y
		self.radius = radius
		self.font = pygame.font.SysFont("Gill Sans", 24)
		self.number = -1

	def UpdateNumber(self, number):
		self.number = number

	
	def UpdateUp(self):
		self.y = self.y - self.radius * 2

	def UpdateDown(self):
		self.y = self.y + self.radius * 2

	def UpdateLeft(self):
		self.x = self.x - self.radius * 2

	def UpdateRight(self):
		self.x = self.x + self.radius * 2

	def Display(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
		if self.number >= 0:
			text = self.font.render(str(self.number), True, (0, 0, 0))
			kx = int(self.radius / 1.7)
			ky = int(self.radius / 1.5)
			screen.blit(text, (self.x-kx,self.y-ky))


# define a main function
def main():
	 
	#CONSTANTS
	SCREEN_SIZE_X = 800
	SCREEN_SIZE_Y = 600
	pygame.init()
	pygame.display.set_caption("Snake")
	screen = pygame.display.set_mode((SCREEN_SIZE_X,SCREEN_SIZE_Y))

	ballRadius = 20

	balls = []
	ballDiamater = ballRadius * 2
	nbColumns = int(SCREEN_SIZE_X / ballDiamater)
	nbRows = int(SCREEN_SIZE_Y / ballDiamater)
	for i in range(1, nbColumns):
		for j in range(1, nbRows):
			balls.append(Ball(pygame.Color(randint(50,255), randint(50,255), randint(50,255)), i*ballDiamater, j*ballDiamater, ballRadius))
	 
	running = True

	background = pygame.image.load("Wallpapers\harry1.jpg")
	snakeHeadImage = pygame.image.load("snakeHead.png")

	selectedBalls = []
	nbBalls = 50
	for i in range(nbBalls):
		if len(balls) != 0:
			#print(len(balls))
			rindex = randint(0,len(balls)-1)
			#print(rindex)
			b = balls.pop(rindex)
			b.UpdateNumber(i+1)
			selectedBalls.append(b)

	snakeHead = Snake(pygame.Color(255, 255, 255), ballDiamater, ballDiamater, ballRadius, ballDiamater, ballDiamater, SCREEN_SIZE_X-ballDiamater, SCREEN_SIZE_Y-ballDiamater, snakeHeadImage)

	
	MOVEEVENT = pygame.USEREVENT+1
	t = 250 #ms
	pygame.time.set_timer(MOVEEVENT, t)

	gameover = False

	# main loop
	while running:

		screen.fill((0,0,0))
		screen.blit(background, (0,75))

		if gameover == True:
			for event in pygame.event.get():
				# only do something if the event is of type QUIT
				if event.type == pygame.QUIT:
					# change the value to False, to exit the main loop
					running = False
				#if event.type == pygame.KEYUP:
				#	if event.key == pygame.K_SPACE:

			for o in selectedBalls:
				o.Display(screen)
			snakeHead.Display(screen)
			PrintGameover(screen, SCREEN_SIZE_X, SCREEN_SIZE_Y)
		else:	
			# event handling, gets all event from the event queue
			for event in pygame.event.get():
				# only do something if the event is of type QUIT
				if event.type == pygame.QUIT:
					# change the value to False, to exit the main loop
					running = False
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN:
						snakeHead.UpdateDirection("DOWN")
						#snakeHead.UpdateMove()
					if event.key == pygame.K_UP:
						snakeHead.UpdateDirection("UP")
						#snakeHead.UpdateMove()
					if event.key == pygame.K_LEFT:
						snakeHead.UpdateDirection("LEFT")
						#snakeHead.UpdateMove()
					if event.key == pygame.K_RIGHT:
						snakeHead.UpdateDirection("RIGHT")
						#snakeHead.UpdateMove()
				if event.type == MOVEEVENT:
					keys = pygame.key.get_pressed() 
					if keys[pygame.K_DOWN]:
						snakeHead.UpdateDirection("DOWN")
					if keys[pygame.K_UP]:
						snakeHead.UpdateDirection("UP")
					if keys[pygame.K_LEFT]:
						snakeHead.UpdateDirection("LEFT")
					if keys[pygame.K_RIGHT]:
						snakeHead.UpdateDirection("RIGHT")
					check = snakeHead.UpdateMove()
					if check == True:
						gameover = True
					else:
						for o in selectedBalls:
							if o.x == snakeHead.x and o.y == snakeHead.y :
								if snakeHead.TakeBall(o) == True :
									selectedBalls.remove(o)
								#else:
								#	gameover = True
								
			for o in selectedBalls:
				o.Display(screen)
			snakeHead.Display(screen)

		pygame.display.flip()

def PrintGameover(screen, x, y):
	font = pygame.font.SysFont("Gill Sans", 48)
	text = font.render("GAME OVER", True, (255, 0, 0))
	sizeX = text.get_width()
	screen.blit(text, (int((x / 2) - (sizeX / 2)), int(y / 2)))
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()