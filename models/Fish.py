import pygame
import numpy as np
import math

WIDTH = 800
HEIGHT = 600

class Fish:
    def __init__(self):
        self.speed = np.random.random()
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = WIDTH/2
        self.position_y = HEIGHT/2
        self.color = (255, 255, 255)
        self.radius = 5
        self.life = 100
        self.stomach = 0
        self.max_life = 100

    def update_position(self):
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

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)
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
        pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 10, self.life, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, self.stomach, 5))