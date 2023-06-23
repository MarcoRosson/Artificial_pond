from models.Fish import Fish
import numpy as np
from config import *

class Fish_pop:
    def __init__(self):
        self.fish_pop = []
        self.born = 0
        self.dead = 0
        self.count_timer = 0
        for _ in range(N_FISH):
            weights = [np.random.random() for _ in range(15)]
            for i, _ in enumerate(weights):
                if np.random.random() < 0.5:
                    weights[i] *= -1
            self.fish_pop.append(Fish(weights))

    def fish_pop_step(self, food, screen=None):
        self.update_position()
        if screen:
            self.draw(screen)
        self.eat_food(food)
        self.check_food(food)
        self.eval_pop()
        self.update_timer()
        if self.count_timer == 0:
            self.replace_pop()
            generations = set([f.gen for f in self.fish_pop])
            print("Generation: ", generations)

    def eval_pop(self):
        for f in self.fish_pop:
            f.eval()

    def reproduce(self, weights, gen):
        r = 255 - gen*5
        g = 255 - gen*10
        b = 255 - gen*50

        if r < 6:
            r = 255
        if g < 11:
            g = 255
        if b < 51:
            b = 255
        color = (r,g,b)
        self.fish_pop.append(Fish(weights, color, gen+1))
        self.born += 1

    def update_position(self):
        for f in self.fish_pop:
            f.update_position()

    def draw(self, screen):
        max_eaten_food = 1  
        for f in self.fish_pop:
            if f.get_eaten_food() > max_eaten_food:
                max_eaten_food = f.get_eaten_food()
        for f in self.fish_pop:
            f.draw(screen, max_eaten_food)

    def check_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish_pop:
            f.food_target = -1
            min_distance = HUNT_RADIUS*2
            for mcnugget in food_positions:
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<HUNT_RADIUS**2:
                    distance = np.sqrt((mcnugget[0]-f.position_x)**2 + (mcnugget[1]-f.position_y)**2)
                    if distance < min_distance:
                        f.food_angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                        min_distance = distance
                    f.food_target = 1
            f.food_distance = min_distance

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish_pop:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<10:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.eaten_food += 1

    def rank_pop(self):
        ranked_pop = sorted(self.fish_pop, key=lambda x: x.get_fitness(), reverse=True)
        return ranked_pop[:PARENTS]
    
    def replace_pop(self):
        best_fishes = self.rank_pop()
        new_pop = []
        n_offspring = int(N_FISH/PARENTS)-PARENTS
        for fish in best_fishes:
            fish.eaten_food = 0
            if VERBOSE:
                print("Fish ", fish.get_genotype(mutation=False))
            for _ in range(n_offspring):
                weights = fish.get_genotype(mutation=True)
                new_pop.append(Fish(weights, fish.color, fish.gen+1))
        new_pop.extend(best_fishes)
        self.fish_pop = new_pop
        
    def update_timer(self):
        self.count_timer += 1
        if self.count_timer >= REPRODUCTION_TIMER:
            self.count_timer = 0