import pygame
import sys
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

DOT_RADIUS = 3

GOAL_X = 400
GOAL_Y = 100

BRAIN_SIZE = 10
POPULATION_SIZE = 2
MUTATION_RATE = 0.01


# Neural Network
class NeuralNetwork:
	def __init__(self, input_size, output_size):
		self.input_size = input_size
		self.output_size = output_size
		self.weights = np.random.rand(output_size, input_size)

	def predict(self, inputs):
		inputs = np.array(inputs)
		return np.dot(self.weights, inputs)


# Classes
class Brain:
	def __init__(self, size):
		self.neural_network = NeuralNetwork(size, 2)
		self.step = 0

	def mutate(self):
		mutation = np.random.randn(*self.neural_network.weights.shape) * MUTATION_RATE
		self.neural_network.weights += mutation


class Goal:
	def __init__(self):
		self.x = GOAL_X
		self.y = GOAL_Y
		self.color = RED

	def show(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), DOT_RADIUS)


class Dot:
	def __init__(self, brain=None):
		if brain is None:
			self.brain = Brain(BRAIN_SIZE)
		else:
			self.brain = brain

		self.x = WIDTH / 2
		self.y = HEIGHT - 300
		self.velocity = 5
		self.dead = False
		self.reached_goal = False
		self.fitness = 0

	def move(self):
		if not self.dead:
			inputs = [self.x / WIDTH, self.y / HEIGHT, GOAL_X / WIDTH, GOAL_Y / HEIGHT]
			outputs = self.brain.neural_network.predict(inputs)

			# Normalize the output to be between -1 and 1
			x_direction = np.clip(outputs[0], -1, 1)
			y_direction = np.clip(outputs[1], -1, 1)

			# Update position based on the normalized output
			self.x += x_direction * self.velocity
			self.y += y_direction * self.velocity

			self.limit_position()
			self.calculate_fitness()
			self.is_dead()

	def limit_position(self):
		self.x = np.clip(self.x, 0, WIDTH)
		self.y = np.clip(self.y, 0, HEIGHT)

	def is_dead(self):
		if self.x < 0 or self.y < 0 or self.x > WIDTH or self.y > HEIGHT:
			self.dead = True
		elif math.sqrt((self.x - goal.x)**2 + (self.y - goal.y)**2) < DOT_RADIUS:
			self.reached_goal = True
			self.dead = True

	def calculate_fitness(self):
		distance_to_goal = math.sqrt((self.x - goal.x)**2 + (self.y - goal.y)**2)
		self.fitness = 1.0 / (distance_to_goal * distance_to_goal)

	def gimme_baby(self):
		baby = Dot(brain=Brain(BRAIN_SIZE))
		baby.brain.neural_network.weights = np.copy(self.brain.neural_network.weights)
		return baby

	def show(self, screen):
		pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), DOT_RADIUS)


class Population:
	def __init__(self, size):
		self.size = size
		self.dots = [Dot() for _ in range(size)]
		self.generation = 1

	def move(self):
		for dot in self.dots:
			dot.move()

	def update(self):
		if all(dot.dead for dot in self.dots):
			self.generation += 1

			# Select parents and create babies
			self.natural_selection()

	def natural_selection(self):
		fitness_sum = sum(dot.fitness for dot in self.dots)
		new_dots = [self.select_parent(fitness_sum).gimme_baby() for _ in range(self.size)]
		self.dots = new_dots

	def select_parent(self, fitness_sum):
		random_fitness = random.uniform(0, fitness_sum)
		running_sum = 0
		for dot in self.dots:
			running_sum += dot.fitness
			if running_sum > random_fitness:
				return dot

	def show_generation(self, screen):
		font = pygame.font.Font(None, 22)
		text_content = f"Generation: {self.generation}"
		text = font.render(text_content, True, BLUE)
		text_rect = text.get_rect(center=(100, 50))
		screen.blit(text, text_rect)

	def show(self):
		for dot in self.dots:
			dot.show(screen)


# The game loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neural Network Example")
clock = pygame.time.Clock()

goal = Goal()
population = Population(POPULATION_SIZE)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(WHITE)

	population.show()
	population.move()
	population.update()
	population.show_generation(screen)

	goal.show()

	pygame.display.flip()

	clock.tick(FPS)

pygame.quit()
sys.exit()
