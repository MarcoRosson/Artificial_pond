import pygame
import numpy as np
import math
from models.Network import NN
import random
from config import *

class Fish:
    def __init__(self, weights):
        self.genotype = weights
        self.speed = np.random.random()
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = (255, 255, 255)
        self.radius = 5
        self.life = 100
        self.stomach = 0
        self.max_life = 100
        self.NN = NN([5, 3, 3, 5])
        self.NN.set_weights(self.genotype)
        self.food_distance = 0
        self.food_angle = 0

    def get_genotype(self):
        return self.genotype

    def eval(self):
        inputs = [(self.food_distance/60), (self.food_angle/(2*math.pi)), (self.life/100), (self.speed/20), (self.angle/(2*math.pi))]
        outputs = self.NN.activate(inputs)
        choice = np.argmax(outputs)
        if choice == 0:
            self.angle += 0.5
            if VERBOSE:
                print("left")
        if choice == 1:
            self.angle -= 0.5
            if VERBOSE:
                print("right")
        if choice == 2:
            self.speed += 0.5
            if VERBOSE:
                print("speed up")
                print(self.speed)   
        if choice == 3:
            self.speed -= 0.5
            if VERBOSE:
                print("speed down")
                print(self.speed)
        if choice == 4:
            self.speed = 0
            if VERBOSE:
                print("stop")
        self.speed = np.abs(self.speed)

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
        #pygame.draw.polygon(screen, cone_color, [(x1, y1), (x2, y2), (x3, y3)])
        pygame.draw.line(screen, (255, 255, 255), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.angle), self.position_y - 50 * math.sin(self.angle)))
        pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 10, self.life, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, self.stomach, 5))