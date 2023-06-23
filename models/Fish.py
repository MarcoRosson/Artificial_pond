import pygame
import numpy as np
import math
from models.Network import NN
import random
from config import *

class Fish:
    def __init__(self, weights, color=(255, 255, 255), gen=0):
        self.genotype = weights
        self.speed = 10
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = color
        self.radius = 6
        self.NN = NN([2, 1, 3])
        self.NN.set_weights(self.genotype)
        self.food_target = 0
        self.food_distance = 0
        self.food_angle = 0
        self.gen = gen
        self.eaten_food = 0
        self.fitness = 0
        self.decisions = []
        self.MUTATION_PROB = float(self.read_config_file()['mutation_prob'])
        self.MUTATION_MAG = float(self.read_config_file()['mutation_mag'])

    def eval(self):
        inputs = [self.food_distance/(HUNT_RADIUS*2), self.food_angle/(2*np.pi)]
        if VERBOSE:
            print("Inputs:", inputs)
        outputs = self.NN.activate(inputs)
        choice = np.argmax(outputs)
        if choice == 0:
            self.angle += ANGLE_MAG
            if VERBOSE:
                print("left")
        if choice == 1:
            self.angle -= ANGLE_MAG
            if VERBOSE:
                print("right")
        if choice == 2:
            if VERBOSE:
                print("nothing")
        self.angle = self.angle % (2*np.pi)

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

    def draw(self, screen, total_food):
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
        pygame.draw.line(screen, (255, 255, 255), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.angle), self.position_y - 50 * math.sin(self.angle)))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, (self.eaten_food/total_food)*100, 5))
        #pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 30, self.fitness, 5))

    def get_genotype(self, mutation=True):
        if VERBOSE:
            print("Old genotype:", self.genotype)
        if mutation:
            new_genotype = self.genotype
            for i in range(len(self.genotype)):
                choice = np.random.choice([True, False], p=[self.MUTATION_PROB, 1-self.MUTATION_PROB])
                if choice:
                    new_genotype[i] += np.random.normal(0, self.MUTATION_MAG)
            if VERBOSE:
                print("New genotype:", new_genotype)
            return new_genotype
        else:
            return self.genotype
        
    def get_fitness(self):
        fitness = self.eaten_food # - ((self.time_alive+1)**2)/self.eaten_food
        self.fitness = fitness 
        return fitness
    
    def get_eaten_food(self):
        return self.eaten_food
    
    def read_config_file(self):
        config = {}
        with open('config.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
        return config