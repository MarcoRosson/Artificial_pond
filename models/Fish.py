import pygame
import numpy as np
import math
from models.Network import NN
import random
from config import *

class Fish:
    def __init__(self, weights, color=(255, 255, 255), gen=0):
        self.genotype = weights
        self.speed = SPEED
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = color
        self.radius = 6
        self.NN = NN([2,1])
        self.NN.set_weights(self.genotype)
        self.food_target = 0
        self.food_distance = 0
        self.food_angle = 0
        self.gen = gen
        self.eaten_food = 0
        self.fitness = 0
        self.decisions = []

    def eval(self):
      
        inputs = [self.angle, self.food_angle]
        outputs = self.NN.activate(inputs)

        if inputs[1] != 0 or inputs[0] != 0:
            self.decisions.append(outputs[0] - (inputs[1]-inputs[0]))
        else:
            self.decisions.append(99)
    
        self.angle += outputs[0]
        self.angle = self.angle % (2*np.pi)

        self.fitness = abs(sum(self.decisions)/len(self.decisions))
        print("\nfitness: ", self.fitness, " angle: ", inputs[0], " output: " , outputs[0], "food_angle: ", inputs[1])
        # print("\nfitness: ", self.fitness, " angle: ", inputs[0], " output: " , outputs[0])
        print("\nweights: ", self.genotype)
        self.update_position()
            

    def update_position(self):
        self.position_x += self.speed * np.cos(self.angle)
        self.position_y -= self.speed * np.sin(self.angle)
        if self.position_x > WIDTH:
            self.angle = (np.pi - self.angle) % (2*np.pi)
        if self.position_x < 0:
            self.angle = (np.pi - self.angle) % (2*np.pi)
        if self.position_y > HEIGHT:
            self.angle = -self.angle % (2*np.pi)
        if self.position_y < 0:
            self.angle = -self.angle % (2*np.pi)

    def draw(self, screen, total_food, highest_fitness):
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
        # pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, (self.eaten_food/total_food)*100, 5))
        # pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 30, (self.fitness/highest_fitness)*100, 5))
        
        #pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), HUNT_RADIUS,1)
        pygame.draw.line(screen, (255, 0, 255), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.food_angle), self.position_y - 50 * math.sin(self.food_angle)))
        # pygame.draw.line(screen, (255, 255, 0), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.angle-self.food_angle), self.position_y - 50 * math.sin(self.angle-self.food_angle)))

    def get_genotype(self, mutation=True):
        if VERBOSE:
            print("Old genotype:", self.genotype)
        if mutation:
            new_genotype = self.genotype
            for i in range(len(self.genotype)):
                choice = np.random.choice([True, False], p=[MUTATION_PROB, 1-MUTATION_PROB])
                if choice:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG)
            if VERBOSE:
                print("New genotype:", new_genotype)
            return new_genotype
        else:
            return self.genotype
        
    def get_fitness(self):
        # self.fitness = sum(self.decisions) / (len(self.decisions)+1) # - ((self.time_alive+1)**2)/self.eaten_food
        return self.fitness
    
    def get_eaten_food(self):
        return self.eaten_food