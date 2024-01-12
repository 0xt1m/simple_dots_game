import pygame
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_DOTS = 50
MUTATION_RATE = 0.1

# Neural network parameters
INPUT_SIZE = 2
HIDDEN_SIZE = 8
OUTPUT_SIZE = 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Dot class
class Dot(pygame.sprite.Sprite):
	def __init__(self, color, radius, position=None, velocity=None, brain=None):
		super().__init__()
		self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.image, color, (radius, radius), radius)
		self.rect = self.image.get_rect()
		if position is None:
			self.rect.center = (random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius))
		else:
			self.rect.center = position
		if velocity is None:
			self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
		else:
			self.velocity = velocity

		# Neural network parameters
		self.input_size = INPUT_SIZE
		self.hidden_size = HIDDEN_SIZE
		self.output_size = OUTPUT_SIZE

		# Initialize weights for the neural network
		if brain is None:
			self.weights_ih = np.random.uniform(-1, 1, (self.hidden_size, self.input_size))
			self.weights_ho = np.random.uniform(-1, 1, (self.output_size, self.hidden_size))
		else:
			self.weights_ih, self.weights_ho = brain

	def update(self):
		# Feedforward neural network to get output
		inputs = np.array([self.rect.x / WIDTH, self.rect.y / HEIGHT], dtype=np.float32)
		hidden = np.tanh(np.dot(self.weights_ih, inputs))
		outputs = np.tanh(np.dot(self.weights_ho, hidden))

		# Convert outputs to movement
		self.velocity = (outputs[0] * 2, outputs[1] * 2)

		# Update dot's position
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]

		# Check if dot is out of bounds
		if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
			self.kill()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dot Simulation")
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()
dots = pygame.sprite.Group()

# Create stationary dot
stationary_dot = Dot(BLUE, 20, (WIDTH // 2, HEIGHT // 2), (0, 0))
all_sprites.add(stationary_dot)

# Create initial dots
for _ in range(NUM_DOTS):
	dot = Dot(RED, 10)
	all_sprites.add(dot)
	dots.add(dot)

# Main loop
generation = 1
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Update
	all_sprites.update()

	# Check if all dots have died
	if not dots:
		print(f"Generation {generation} - All dots died")

		# Create the next generation
		new_dots = []
		for _ in range(NUM_DOTS):
			parent = random.choice(all_sprites.sprites())
			child_brain = (
				parent.weights_ih + np.random.uniform(-MUTATION_RATE, MUTATION_RATE, parent.weights_ih.shape),
				parent.weights_ho + np.random.uniform(-MUTATION_RATE, MUTATION_RATE, parent.weights_ho.shape)
			)
			new_dot = Dot(RED, 10, brain=child_brain)
			new_dots.append(new_dot)

		# Replace old generation with the new one
		dots.empty()
		dots.add(new_dots)

		# Reset the position of the stationary dot
		stationary_dot.rect.center = (WIDTH // 2, HEIGHT // 2)

		# Increment generation
		generation += 1

	# Check for collisions with stationary dot
	collisions = pygame.sprite.spritecollide(stationary_dot, dots, dokill=False)

	for dot in collisions:
		dot.velocity = [0, 0]  # Stop dot

	# Draw
	screen.fill(WHITE)
	all_sprites.draw(screen)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()
