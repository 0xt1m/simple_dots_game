import numpy as np
import pygame
import random
import math
import copy
import sys

# pygame initialization
pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (87, 132, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

DOT_RADIUS = 6

GOAL_X = 400
GOAL_Y = 50

DOTS_X = WIDTH / 2
DOTS_Y = HEIGHT - 30

BRAIN_SIZE = 3000
POPULATION_SIZE = 100
MUTATION_RATE = 0.001
FPS = 300


# The main screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dot Simulation")
clock = pygame.time.Clock()


# Additional Functions
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def from_angle(angle, length=1):
		x = length * math.cos(angle)
		y = length * math.sin(angle)
		return [x, y]


# Classes
class Brain:
	def __init__(self, size):
		self.directions = [0] * size
		self.step = 0

		self.randomize()


	def randomize(self):
		for i in range(len(self.directions)):
			random_angle = random.uniform(0, 2*math.pi)
			self.directions[i] = from_angle(random_angle)


	def mutate(self):
		for i in range(len(self.directions)):
			rand = random.uniform(0, 1)
			if (rand < MUTATION_RATE):
				random_angle = random.uniform(0, 2*math.pi)
				self.directions[i] = from_angle(random_angle)


class Goal:
	def __init__(self):
		self.x = GOAL_X
		self.y = GOAL_Y

		self.color = RED


	def show(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), DOT_RADIUS)


class Dot:
	def __init__(self, brain=None):
		if brain == None:
			self.brain = Brain(BRAIN_SIZE)
		else:
			self.brain = brain

		self.velocity = [0, 0]
		self.acceleration = [0, 0]

		self.x = DOTS_X
		self.y = DOTS_Y

		self.color = WHITE

		self.dead = False
		self.reached_goal = False
		self.fitness = 0


	def show(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), DOT_RADIUS)


	def move(self):
		if not self.dead:
			if self.brain.step < len(self.brain.directions):
				self.acceleration = self.brain.directions[self.brain.step]
				self.brain.step += 1
			else: 
				self.dead = True

			# Velocity + Acceleration
			self.velocity[0] += self.acceleration[0]
			self.velocity[1] += self.acceleration[1]

			# Position + Velocity
			self.x += self.velocity[0]
			self.y += self.velocity[1]

			self.limit_velocity(5)
			self.calculate_fitness()

			self.is_dead()


	def limit_velocity(self, max_velocity):
		velocity = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
		if velocity > max_velocity:
			scale_factor = max_velocity / velocity
			self.velocity = [self.velocity[0] * scale_factor, self.velocity[1] * scale_factor]


	def is_dead(self):
		for obs in obstacles:
			if pygame.Rect(self.x, self.y, DOT_RADIUS, DOT_RADIUS).colliderect(obs.rect):
				self.dead = True
		if self.x < 0 or self.y < 0:
			self.dead = True
		elif self.x > WIDTH or self.y > HEIGHT:
			self.dead = True
		elif distance(self.x, self.y, goal.x, goal.y) < DOT_RADIUS:
			self.reached_goal = True
			self.dead = True


	def calculate_fitness(self):
		if self.reached_goal:
			self.fitness = 1.0 / 16.0 + 10000.0 / (self.brain.step * self.brain.step)
		else:
			distance_to_goal = distance(self.x, self.y, goal.x, goal.y)
			self.fitness = 1.0 / 16.0 + 10000.0 / (distance_to_goal * distance_to_goal)


	def gimme_baby(self):
		baby = Dot()
		baby.brain.directions = copy.deepcopy(self.brain.directions)
		return baby


class Population:
	def __init__(self, size):
		self.size = size
		self.dots = [0] * self.size
	
		self.generation = 1

		for i in range(len(self.dots)):
			self.dots[i] = Dot()


	def show(self):
		for dot in self.dots:
			dot.show()


	def move(self):
		for dot in self.dots:
			dot.move()


	def update(self):
		if self.all_dead():
			self.generation += 1
			
			# Selects parents and borns babies
			self.natural_selection()
			
			# Modifies the babies
			self.mutate_dem_babies()


	def natural_selection(self):
		# Get the sum of all the fitnesses
		fitness_sum = self.calculate_fitness_sum()

		# Create new dots
		new_dots = [0] * self.size
		for i in range(len(new_dots)):
			
			# Chose a parent for each dot
			parent = self.select_parent(fitness_sum)
			
			# The parent borns a baby
			new_dots[i] = parent.gimme_baby()

		# Old dots turn into the new dots
		self.dots = new_dots


	def calculate_fitness_sum(self):
		fitness_sum = 0
		for dot in self.dots:
			fitness_sum += dot.fitness

		return fitness_sum


	def select_parent(self, fitness_sum):
		# We have the fitness sum
		# Dots that touched the goal have the highest fitness
		# Therefore, they have a bigger range in the fitness sum
		# Therefore, there is a better chance that a random number will be in the range of the winner dot
		random_fitness = random.uniform(0, fitness_sum)

		# Genius method to select the right dot.
		running_sum = 0
		for dot in self.dots:
			running_sum += dot.fitness
			if running_sum > random_fitness:
				return dot


	def mutate_dem_babies(self):
		for dot in self.dots:
			old_directions = dot.brain.directions
			dot.brain.mutate()
			new_directions = dot.brain.directions


	def all_dead(self):
		for dot in self.dots:
			if dot.dead == False:
				return False
		return True


	def show_generation(self, screen):
		text_content = "Generation: " + str(self.generation)
		
		font = pygame.font.Font(None, 22)
		text = font.render(text_content, True, BLUE)
		text_rect = text.get_rect()
		text_rect.center = (100, 50)
		screen.blit(text, text_rect)


class Obstacle:
	def __init__(self, x, y, width, height):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x, y, width, height)


	def show(self):
		pygame.draw.rect(screen, YELLOW, self.rect)



# The game is running here
running = True

goal = Goal()

# brain = Brain(700)
population = Population(POPULATION_SIZE)

obstacles = [
			Obstacle(100, 100, 150, 15), 
			Obstacle(300, 300, 250, 15), 
			Obstacle(100, 450, 350, 15)
]

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False



	screen.fill(BLACK)
	
	population.show()
	population.move()
	population.update()

	for obstacle in obstacles:
		obstacle.show()

	population.show_generation(screen)

	goal.show()


	pygame.display.flip()

	clock.tick(FPS)


pygame.quit()
sys.exit()






