import pygame
import numpy as np
import math
from models.Network import NN
import random
from config import *

class Fish:
    def __init__(self, weights, color=(255, 255, 255), gen=0):
        self.genotype = weights
        self.speed = FISH_SPEED
        self.angle = np.random.random() * 2 * np.pi
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.color = color
        self.radius = 6
        self.NN = NN(NETWORK_LAYERS.copy())
        self.NN.set_weights(self.genotype)
        self.food_distance = 0
        self.food_angle = 0
        self.gen = gen
        self.eaten_food = 0
        self.fitness = 0
        self.center_neighborhood_angle = 0
        self.food_sensors = [0,0,0,0]
        self.fish_sensors = [0,0,0,0]
        self.wall_sensor = 0
        self.collisions = 0
        self.pop_fitness = 0

    def eval(self):
        if NETWORK_CONFIGURATION == 'angle_decisions':
            inputs = [self.angle, self.food_angle, self.food_distance/HUNT_RADIUS]
            if COESION:
                inputs.append(self.center_neighborhood_angle)

            outputs = self.NN.activate(inputs)
            choice = np.argmax(outputs)
            if choice == 0:
                self.angle += ANGLE_MAG
            if choice == 1:
                self.angle -= ANGLE_MAG
            if choice == 2:
                pass

        elif NETWORK_CONFIGURATION == 'sensors_decisions':
            inputs = [self.food_sensors[0],self.food_sensors[1],self.food_sensors[2],self.food_sensors[3],self.wall_sensor]
            if COESION:
                inputs = [self.food_sensors[0],self.food_sensors[1],self.food_sensors[2],self.food_sensors[3],
                    self.fish_sensors[0],self.fish_sensors[1],self.fish_sensors[2],self.fish_sensors[3],
                    self.wall_sensor]
            outputs = self.NN.activate(inputs)
            choice = np.argmax(outputs)
            if choice   == 0:
                self.angle = self.angle
            elif choice == 1:
                self.angle += ANGLE_MAG
            elif choice == 2:
                self.angle -= ANGLE_MAG
            elif choice == 3:
                self.angle += np.pi

        self.angle = self.angle % (2*np.pi)
        

    def update_position(self):
        if self.position_x > WIDTH:
            self.angle = np.pi - self.angle
        if self.position_x < 0:
            self.angle = np.pi - self.angle
        if self.position_y > HEIGHT:
            self.angle = -self.angle
        if self.position_y < 0:
            self.angle = -self.angle
        self.position_x += self.speed * np.cos(self.angle)
        self.position_y -= self.speed * np.sin(self.angle)

    def draw(self, screen, total_food):
        pygame.draw.circle(screen, self.color, (self.position_x, self.position_y), self.radius)
        pygame.draw.line(screen, (255, 255, 255), (self.position_x, self.position_y), (self.position_x + 50 * math.cos(self.angle), self.position_y - 50 * math.sin(self.angle)))
        pygame.draw.rect(screen, (0, 255, 0), (self.position_x-50, self.position_y + 20, (self.eaten_food/total_food)*100, 5))

    def get_genotype(self, mutation=True):
        if mutation:
            self.get_fitness()
            genes_to_mutate = int(len(self.genotype) * MUTATION_PROB)
            new_genotype = self.genotype.copy()
            possible_choices = np.arange(len(self.genotype))
            final_choice = random.sample(list(possible_choices), genes_to_mutate)
                
            for i in iter(final_choice):
                #choice = np.random.choice([True, False], p=[MUTATION_PROB, 1-MUTATION_PROB])
                if self.fitness > 20:
                    pass
                if self.fitness > 18:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG/40)
                if self.fitness > 16:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG/30)
                if self.fitness > 14:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG/20)
                if self.fitness > 12:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG/10)
                if self.fitness > 10:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG/5)
                else:
                    new_genotype[i] += np.random.normal(0, MUTATION_MAG)
            return new_genotype
        else:
            return self.genotype
        
    def check_neighborhood(self, fish_pop):
        if NEIGHBORHOOD_TYPE_CENTER == 'global':
            global_position_x = 0
            global_position_y = 0
            for f in fish_pop:
                global_position_x += f.position_x
                global_position_y += f.position_y
            global_position_x /= len(fish_pop)
            global_position_y /= len(fish_pop)
            self.center_neighborhood_angle = - np.arctan2(global_position_y-self.position_y, global_position_x-self.position_x)

        elif NEIGHBORHOOD_TYPE_CENTER == 'local':
            neighborhood_fish = []
            for f in fish_pop:
                if ((f.position_x-self.position_x)**2 + (f.position_y-self.position_y)**2)<SOCIAL_RADIUS**2:
                    neighborhood_fish.append(f)
            if len(neighborhood_fish) > 0:
                neighborhood_position_x = 0
                neighborhood_position_y = 0
                for f in neighborhood_fish:
                    neighborhood_position_x += f.position_x
                    neighborhood_position_y += f.position_y
                neighborhood_position_x /= len(neighborhood_fish)
                neighborhood_position_y /= len(neighborhood_fish)
                self.center_neighborhood_angle = - np.arctan2(neighborhood_position_y-self.position_y, neighborhood_position_x-self.position_x)
            else:
                self.center_neighborhood_angle = 0
        
    def get_fitness(self):
        fitness = self.eaten_food
        self.fitness = fitness 
        return fitness
    
    def get_eaten_food(self):
        return self.eaten_food