import numpy as np
from models.Food_particle import Food_particle

class Food:
    def __init__(self):
        self.food_particles = []
        for _ in range(10):
            self.food_particles.append(Food_particle())

    def draw(self, screen):
        for f in self.food_particles:
            f.draw(screen)

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
            self.food_particles.append(Food_particle())