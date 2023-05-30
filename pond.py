import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import random
import math
from models.Fish_pop import Fish_pop
from models.Food import Food

WIDTH = 800
HEIGHT = 600


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
    population.draw(screen)
    population.eat_food(food)
    population.check_food(food)
    population.lose_life()
    population.digest()
    
    food.draw(screen)
    food.spawn_food()

    pygame.display.flip()
    clock.tick(30) # FPS

    iterations += 1
    if iterations >= 1000000:
        running = False

# Quit Pygame
pygame.quit()
