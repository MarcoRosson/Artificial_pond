import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import random
import math

WIDTH = 800
HEIGHT = 600

class fish:
    def __init__(self):
        geno0 = np.random.random()
        geno1 = np.random.random()
        self.genotype = [geno0, geno1]
        # self.velocity_x = self.genotype[0]
        # self.velocity_y = self.genotype[1]
        self.speed = self.genotype[0]
        self.angle = self.genotype[1] * 2 * np.pi
        self.position_x = WIDTH/2
        self.position_y = HEIGHT/2
        self.color = (255, 255, 255)
        self.radius = 5
    
    def update(self):
        # self.velocity_x = self.genotype[0]
        # self.velocity_y = self.genotype[1]
        self.angle = self.genotype[0]
        self.speed = self.genotype[1]

    def update_position(self):
        # self.position_x += self.velocity_x
        # self.position_y += self.velocity_y
        self.position_x += self.speed * np.cos(self.angle)
        self.position_y += self.speed * np.sin(self.angle)
        if self.position_x > WIDTH:
            self.angle = np.pi - self.angle
        if self.position_x < 0:
            self.angle = np.pi - self.angle
        if self.position_y > HEIGHT:
            self.angle = -self.angle
        if self.position_y < 0:
            self.angle = -self.angle

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)

class Fish_pop:
    def __init__(self):
        self.fish = []
        for _ in range(10):
            self.fish.append(fish())

    def update_position(self):
        for f in self.fish:
            f.update_position()

    def draw(self):
        for f in self.fish:
            f.draw()

    def check_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for mcnugget in food_positions:
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<500:
                    f.angle = math.atan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                    f.speed = 3

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<10:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.speed = 1


class food_particle:
    def __init__(self):

        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = (0, 255, 0)
        self.radius = 3

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)

    

class Food:
    def __init__(self):
        self.food_particles = []
        for _ in range(10):
            self.food_particles.append(food_particle())

    def draw(self):
        for f in self.food_particles:
            f.draw()

    def get_positions(self):
        positions = []
        for f in self.food_particles:
            positions.append([f.position_x, f.position_y])
        return positions
    
    def remove_food(self, index):
        self.food_particles.pop(index)

    def spawn_food(self):
        choice = random.choice([True, False])
        if choice==True:
            self.food_particles.append(food_particle())


population = Fish_pop()
food = Food()

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = WIDTH
screen_height = HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Main game loop
running = True
iterations = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Update and draw particles
    population.update_position()
    population.draw()
    population.eat_food(food)
    population.check_food(food)
    
    food.draw()
    food.spawn_food()

    pygame.display.flip()
    clock.tick(120) # FPS

    iterations += 1
    if iterations >= 1000000:
        running = False

# Quit Pygame
pygame.quit()
