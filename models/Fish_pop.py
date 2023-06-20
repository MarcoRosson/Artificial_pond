from models.Fish import Fish
import numpy as np
from config import *

class Fish_pop:
    def __init__(self):
        self.fish = []
        self.born = 0
        self.dead = 0
        self.count_timer = 0
        for _ in range(N_FISH):
            weights = [np.random.random() for _ in range(39)]
            for i, _ in enumerate(weights):
                if np.random.random() < 0.5:
                    weights[i] *= -1
            self.fish.append(Fish(weights))

    def fish_pop_step(self, screen, food):
        self.update_position()
        self.draw(screen)
        self.eat_food(food)
        self.check_food(food)
        self.eval_pop()
        self.lose_life()
        self.digest()
        self.dead_born()
        self.update_timer()
        if self.count_timer == 0:
            self.check_reproduction()
            print("reproduction")

    def eval_pop(self):
        for f in self.fish:
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
        self.fish.append(Fish(weights, color, gen+1))
        self.born += 1

    def update_position(self):
        for f in self.fish:
            f.update_position()

    def draw(self, screen):
        for f in self.fish:
            f.draw(screen)

    def check_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            f.food_distance = 60
            for mcnugget in food_positions:
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<4000:
                    f.food_angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                    f.food_distance = np.sqrt((mcnugget[0]-f.position_x)**2 + (mcnugget[1]-f.position_y)**2)

    def check_reproduction(self):
        fishes = self.fish.copy()
        for _ in range(OFFSPRING):
            best_fish = fishes[0]
            best_score = fishes[0].get_fitness()
            for f in fishes:
                if f.get_fitness() > best_score:
                    best_score = f.get_fitness()
                    best_fish = f
            self.reproduce(best_fish.get_genotype(), best_fish.gen)
            fishes.remove(best_fish)

        # new_list = []
        # # for f in self.fish:
        # #     if f.stomach > 50 and f.life > 60:
        # #         self.reproduce(f.get_genotype(), f.color)
        # new_list = sorted(self.fish, key=lambda x: x.eaten_food, reverse=True)
        # self.reproduce(new_list[0].get_genotype(), new_list[0].color, new_list[0].gen)


    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<10:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    #f.speed = 1
                    f.stomach += 50
                    if f.stomach > 100:
                        f.stomach = 100
                    f.eaten_food += 1
                    #self.reproduce(f.get_genotype(), f.color)
                    

    def lose_life(self):
        for f in self.fish:
            f.life -= (LIFE_LOSS_SPEED*f.speed+LIFE_LOSS)
            f.max_life -= 0.01
            if f.life <= 0:
                self.fish.remove(f)
                self.dead += 1

    def digest(self):
        for f in self.fish:
            if f.stomach > 0 and f.life < f.max_life:
                f.stomach -= 0.5
                f.life += 0.25

    def dead_born(self):
        max_gen = []
        max_food = []
        for f in self.fish:
            max_gen.append(f.gen)
            max_food.append(f.eaten_food)
        
        print(f"Born: {self.born}, Dead: {self.dead}, Food prob: {self.get_food_prob()}, Gen: {max(max_gen)}, Food: {max(max_food)}")

    def update_timer(self):
        self.count_timer += 1
        if self.count_timer >= 80:
            self.count_timer = 0

    def get_food_prob(self):
        total_life = 0 
        for f in self.fish:
            total_life += f.life
        return (1 - (total_life/len(self.fish)/100))