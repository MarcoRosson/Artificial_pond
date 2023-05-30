from models.Fish import Fish
import numpy as np

class Fish_pop:
    def __init__(self):
        self.fish = []
        for _ in range(10):
            self.fish.append(Fish())

    def update_position(self):
        for f in self.fish:
            f.update_position()

    def draw(self, screen):
        for f in self.fish:
            f.draw(screen)

    def check_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for mcnugget in food_positions:
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<500:
                    f.angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                    f.speed = 3

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<10:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.speed = 1
                    f.stomach += 50
                    if f.stomach > 100:
                        f.stomach = 100

    def lose_life(self):
        for f in self.fish:
            f.life -= 0.1
            f.max_life -= 0.01
            if f.life <= 0:
                self.fish.remove(f)

    def digest(self):
        for f in self.fish:
            if f.stomach > 0 and f.life < f.max_life:
                f.stomach -= 1
                f.life += 0.5