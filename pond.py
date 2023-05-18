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
        self.life = 500
    
    def update(self):
        # self.velocity_x = self.genotype[0]
        # self.velocity_y = self.genotype[1]
        self.angle = self.genotype[0]
        self.speed = self.genotype[1]

    def update_position(self):
        # self.position_x += self.velocity_x
        # self.position_y += self.velocity_y
        self.position_x += self.speed * np.cos(self.angle)
        self.position_y -= self.speed * np.sin(self.angle)
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
        # Triangle that show sight of the particle in angle direction
        cone_radius = math.radians(60/2) 
        rotation_radius = self.angle
        cone_length = 50
        x1 = self.position_x
        y1 = self.position_y
        x2 = self.position_x + cone_length * math.cos(cone_radius+rotation_radius)
        y2 = self.position_y - cone_length * math.sin(cone_radius+rotation_radius)
        x3 = self.position_x + cone_length * math.cos(-cone_radius+rotation_radius)
        y3 = self.position_y - cone_length * math.sin(-cone_radius+rotation_radius)
        cone_color = (110, 0, 0) 
        pygame.draw.polygon(screen, cone_color, [(x1, y1), (x2, y2), (x3, y3)])
        #pygame.draw.line(screen, (255, 255, 255), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.angle), self.position_y - 50 * math.sin(self.angle)))
        pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 10, self.life*0.2, 5))

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
                    f.angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                    f.speed = 3

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<10:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.speed = 1
                    f.life += 100
                    if f.life > 500:
                        f.life = 500

    def lose_life(self):
        for f in self.fish:
            f.life -= 1
            if f.life <= 0:
                self.fish.remove(f)


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
        choice = np.random.choice([True, False], p=[0.1, 0.9])
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
    population.lose_life()
    
    food.draw()
    food.spawn_food()

    pygame.display.flip()
    clock.tick(30) # FPS

    iterations += 1
    if iterations >= 1000000:
        running = False

# Quit Pygame
pygame.quit()
