import pygame
import numpy as np
import math
from models.Network import NN
import random
from config import *

class Fish:
    def __init__(self, weights, color=(255, 255, 255), gen=0):
        self.genotype = weights
        self.speed = 2
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = color
        self.radius = 6
        self.hunt_radius = 50
        self.social_radius = 200
        self.NN = NN([2,2,1])
        self.NN.set_weights(self.genotype)
        self.food_distance = 0
        self.food_angle = 0
        self.gen = gen
        self.eaten_food = 0
        self.time_alive = 0 
        self.fitness = 0
        self.decisions = []
        #self.life = 100
        #self.stomach = 0
        #self.max_life = 100

    def eval(self):

        if self.food_distance < self.hunt_radius:        
            Target = 1
        else:
            Target = 0

        inputs = [Target, (self.food_angle-self.angle/(2*math.pi))] #(self.angle/(2*math.pi))
        outputs = self.NN.activate(inputs)
        # print(outputs)
        
        # let's suppose outmin -1 and outmax 1
        if outputs > -1 and outputs < -0.34:
            self.angle += 0.1
            self.decisions.append(1)
            if VERBOSE:
                print("right")
        elif outputs > -0.33 and outputs < 0.33:
            self.angle = self.angle
            self.decisions.append(3)
            if VERBOSE:
                print("continue")
        elif outputs > 0.34 and outputs < 1:
            self.angle -= 0.1
            self.decisions.append(2)
            if VERBOSE:
                print("left")
        
        # adjust fitness if fish is stuck in a loop
        if len(self.decisions) == 500:
            decisions = self.decisions
            decisions = np.array(decisions)
            #print(decisions)
            diff_decisions = np.diff(decisions)
            #print(diff_decisions)
            if np.sum(diff_decisions) == 0:
                self.fitness -= 1
                self.fitness = max(0, self.fitness)
                print('fit decreased', self.fitness)
            
            self.decisions = []


        # choice = np.argmax(outputs)
        # if choice == 0:
        #     self.angle += 0.2
        #     if VERBOSE:
        #         print("right")
        
        # if choice == 1:
        #     self.angle -= 0.2
        #     if VERBOSE:
        #         print("left")

        # if choice == 2:
        #     self.angle = self.angle
        #     if VERBOSE:
        #         print("continue")
    
        #self.speed = np.abs(self.speed)
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
        #pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 10, self.life, 5))
        #pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, self.stomach, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, self.eaten_food, 5))
        pygame.draw.rect(screen, (255, 0, 0), (self.position_x-50, self.position_y + 30, self.fitness, 5))
        
        # For visualization
        #pygame.draw.circle(screen,  (255, 0, 0), (self.position_x, self.position_y), self.hunt_radius, width = 1)
        #pygame.draw.circle(screen,  (0, 0, 255), (self.position_x, self.position_y), self.social_radius, width = 1)

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
    
    # We should normalize the Fitness After
    def get_fitness(self):

        fitness = self.eaten_food # - ((self.time_alive+1)**2)/self.eaten_food
        self.fitness = fitness 

        return fitness