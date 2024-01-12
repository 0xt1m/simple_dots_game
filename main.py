import pygame
import random

import math




def add_double_tuples(t1, t2):
	return t1[0] + t2[0], t1[1] + t2[1]

class Brain:
	def __init__(self, size):
		self.directions = [0] * size
		self.step = 0

		self.x = 0
		self.y = 0

		self.randomize()


	def from_angle(self, angle, length=1):
		self.x = length * math.cos(angle)
		self.y = length * math.sin(angle)
		return self.x, self.y


	def randomize(self):
		for i in range(len(self.directions)):
			random_angle = random.uniform(0, 2*math.pi)
			self.directions[i] = self.from_angle(random_angle)


class Dot:
	def __init__(self, screen_borders=(800, 800)):
		self.color = (255, 255, 255)
		self.size = 5
		
		self.dead = False
		self.screen_borders = screen_borders

		self.pos = (400, 400)
		self.vel = (0.0, 0.0)
		self.acc = (0.0, 0.0)

		self.brain = Brain(400)


	def limit(self, max_length):
		length = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if length > max_length:
			scale_factor = max_length / length
			self.vel = (self.vel[0] * scale_factor, self.vel[1] * scale_factor)


	def check_if_out(self):
		if self.pos[0] < 0 or self.pos[1] < 0:
			self.dead = True
		elif self.pos[0] > self.screen_borders[0] or self.pos[1] > self.screen_borders[1]:
			self.dead = True
	

	def show(self):
		pygame.draw.circle(screen, self.color, self.pos, self.size)


	def move(self):
		if not self.dead:
			if len(self.brain.directions) > self.brain.step:
				self.acc = self.brain.directions[self.brain.step]
				self.brain.step += 1
			else:
				self.dead = True

			self.vel = add_double_tuples(self.vel, self.acc)
			self.limit(5)
			self.pos = add_double_tuples(self.pos, self.vel)

			self.check_if_out()


class Population:
	def __init__(self, size):
		self.dots = [Dot()] * size
		print(self.dots)

	def show(self):
		for dot in self.dots:
			dot.show()


	def update(self):
		for dot in self.dots:
			dot.move()
		



pygame.init()

screen = pygame.display.set_mode([800, 800])

test = Population(5)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    test.update()
    test.show()

    # running = False

    pygame.display.flip()





pygame.quit()