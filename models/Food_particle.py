import pygame
import random
from config import *

class Food_particle:
    def __init__(self):

        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = (0, 255, 0)
        self.radius = 3
        self.life = 400

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)