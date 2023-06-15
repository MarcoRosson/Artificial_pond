import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import random
import math
from models.Fish_pop import Fish_pop
from models.Food_pop import Food_pop
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets
from config import *


population = Fish_pop()
food = Food_pop()

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

slider = Slider(screen, 30, 20, 200, 10, min=0, max=0.5, step=0.01, colour=(10, 200, 50), initial=FOOD_PROB)
output = TextBox(screen, 230, 5, 40, 30, fontSize=20)
output.disable()

# Main game loop
running = True
iterations = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame_widgets.update(event)
    output.setText(slider.getValue())

    # Update and draw particles
    population.update_position()
    population.draw(screen)
    population.eat_food(food)
    population.check_food(food)
    population.eval_pop()
    population.lose_life()
    population.digest()
    if VERBOSE:
        population.dead_born()
    
    food.draw(screen)
    food.spawn_food(probability=slider.getValue())

    pygame.display.flip()
    clock.tick(FPS) # FPS

    iterations += 1
    if iterations >= 1000000:
        running = False

# Quit Pygame
pygame.quit()
