from models.Fish import Fish
import numpy as np

class Fish_pop:
    def __init__(self):
        self.fish = []
        self.born = 0
        self.dead = 0
        for _ in range(20):
            weights = [np.random.random() for _ in range(39)]
            self.fish.append(Fish(weights))

    def reproduce(self, weights):
        self.fish.append(Fish(weights))
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
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<3000:
                    f.food_angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                    f.food_distance = np.sqrt((mcnugget[0]-f.position_x)**2 + (mcnugget[1]-f.position_y)**2)
                
            

    def eval_pop(self):
        for f in self.fish:
            f.eval()

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
                    self.reproduce(f.get_genotype())
                    

    def lose_life(self):
        for f in self.fish:
            f.life -= (0.03*f.speed+0.1)
            f.max_life -= 0.01
            if f.life <= 0:
                self.fish.remove(f)
                self.dead += 1

    def digest(self):
        for f in self.fish:
            if f.stomach > 0 and f.life < f.max_life:
                f.stomach -= 1
                f.life += 0.5

    def dead_born(self):
        print(f"Born: {self.born}, Dead: {self.dead}")