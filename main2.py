import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
DOT_RADIUS = 5
SPEED = 25
FPS = 30


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class Goal:
	def __init__(self):
		self.x = 400
		self.y = 100

		self.color = (0, 170, 100)


class Dot:
	def __init__(self):
		# self.x = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS)
		# self.y = random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
		self.x = 400
		self.y = 200

		self.color = (255, 255, 255)

		self.dead = False

		self.fitness = 0
		self.reached_goal = False


	def is_dead(self):
		if self.x < 0 or self.y < 0:
			self.dead = True
		elif self.x > WIDTH or self.y > HEIGHT:
			self.dead = True


	def update(self):
		if not self.dead and not self.reached_goal:
			self.x += random.randint(-SPEED, SPEED)
			self.y += random.randint(-SPEED, SPEED)

			# self.x = max(DOT_RADIUS, min(self.x, WIDTH - DOT_RADIUS))
			# self.y = max(DOT_RADIUS, min(self.y, HEIGHT - DOT_RADIUS))

			self.calculate_fitness()
			self.is_dead()
			
			if distance(self.x, self.y, goal.x, goal.y) < 5:
				self.reached_goal = True


	def calculate_fitness(self):
		distance_to_goal = distance(self.x, self.y, goal.x, goal.y)
		self.fitness = 1.0/(distance_to_goal * distance_to_goal)


	def gimme_baby(self):
		baby = Dot()


class Population:
	def __init__(self, size):
		self.dots = [Dot() for _ in range(size)]
		self.fitness_sum = 0


	def update(self):
		for dot in self.dots:
			dot.update()


	def draw(self):
		for dot in self.dots:
			pygame.draw.circle(screen, dot.color, (dot.x, dot.y), DOT_RADIUS)


	def calculate_fitness(self):
		for dot in self.dots:
			dot.calculate_fitness()


	def all_dots_dead(self):
		for dot in self.dots:
			if dot.dead == False and dot.reached_goal == False:
				return False

		return True


	def natural_selection(self):
		new_dots = [Dot() for _ in range(size)]
		self.calculate_fitness_sum()

		for dot in self.dots:
			parent = self.select_parent()

		# select parent based on fitness

		# get a baby from them


	def calculate_fitness_sum(self):
		for dot in self.dots:
			self.fitness_sum += dot.fitness 
	

	def select_parent(self):
		rand = random.uniform(0, self.fitness_sum)

		running_sum = 0

		for dot in self.dots:
			running_sum += dot.fitness
			if running_sum > rand:
				return dot

		return 0



test = Population(100)
goal = Goal()

# print(distance(390, 90, goal.x, goal.y))
# print(goal.x, goal.y)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Randomly Moving Dots")

clock = pygame.time.Clock()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Update dots
	test.update()

	screen.fill((0, 0, 0))

	test.draw()

	if test.all_dots_dead():
		test.calculate_fitness()
		test.natural_selection()
		test.mutate_dem_babies()



	else:
		pass


	
	pygame.draw.circle(screen, goal.color, (goal.x, goal.y), DOT_RADIUS)

	pygame.display.flip()

	clock.tick(FPS)


pygame.quit()



