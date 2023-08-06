from models.Fish import Fish
import numpy as np
from config import *

class Fish_pop:
    def __init__(self):
        self.fish_pop = []
        self.count_timer = 0
        self.iteration = 0
        for _ in range(N_FISH):
            weights = [np.random.random() for _ in range(sum(NETWORK_LAYERS[i] * NETWORK_LAYERS[i+1] for i in range(len(NETWORK_LAYERS)-1)))]
            for i, _ in enumerate(weights):
                if np.random.random() < 0.5:
                    weights[i] *= -1
            self.fish_pop.append(Fish(weights))

    def fish_pop_step(self, food, screen=None, graph=None):
        self.update_position()
        if screen:
            self.draw(screen)
        self.eat_food(food)
        self.check_food(food)
        if NETWORK_CONFIGURATION == 'angle_decisions':
            self.check_neighborhood()
        elif NETWORK_CONFIGURATION == 'sensors_decisions':
            self.check_neighbors()
            self.check_walls()
        self.eval_pop()
        self.update_timer()
        if self.count_timer == 0:
            food.respawn_food()
            print(f"----------{self.iteration}----------")
            generations = set([f.gen for f in self.fish_pop])
            print("Active generations: ", generations)
            self.replace_pop(graph)
            self.iteration += 1
            print()


    def eval_pop(self):
        for f in self.fish_pop:
            f.eval()

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
            min_distance = HUNT_RADIUS*2
            f.food_sensors = [0, 0, 0, 0]
            f.food_angle = f.angle % (2*np.pi)
            for mcnugget in food_positions:
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<HUNT_RADIUS**2:
                    distance = np.sqrt((mcnugget[0]-f.position_x)**2 + (mcnugget[1]-f.position_y)**2)
                    if distance < min_distance:
                        f.food_angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                        min_distance = distance
            f.food_distance = min_distance
            if NETWORK_CONFIGURATION == 'sensors_decisions':
                relative_angle = (f.angle - f.food_angle) % (2*np.pi)
                if relative_angle >=7*np.pi/4 and relative_angle < np.pi/4 :
                    f.food_sensors[0] = sigmoid(min_distance)
                elif relative_angle < 3*np.pi/4 and relative_angle >= np.pi/4 :
                    f.food_sensors[1] = sigmoid(min_distance)
                elif relative_angle >= 3*np.pi/4 and relative_angle < 5*np.pi/4:
                    f.food_sensors[2] = sigmoid(min_distance)
                elif relative_angle >= 5*np.pi/4 and relative_angle < 7*np.pi/4:
                    f.food_sensors[3] = sigmoid(min_distance)

    def check_walls(self):
        for f in self.fish_pop:
            if f.position_x > WIDTH - WALL_RADIUS:
                f.wall_sensor = sigmoid(f.position_x - WIDTH + WALL_RADIUS)
            elif f.position_x < WALL_RADIUS:
                f.wall_sensor = sigmoid(f.position_x - WALL_RADIUS)
            elif f.position_y > HEIGHT - WALL_RADIUS:
                f.wall_sensor = sigmoid(f.position_y - HEIGHT + WALL_RADIUS)
            elif f.position_y < WALL_RADIUS:    
                f.wall_sensor = sigmoid(f.position_y - WALL_RADIUS)

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish_pop:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<EAT_RADIUS**2:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.eaten_food += 1

    def rank_pop(self):
        ranked_pop = sorted(self.fish_pop, key=lambda x: x.get_fitness(), reverse=True)
        return ranked_pop[:PARENTS]
    
    def replace_pop(self, graph=None):
        best_fishes = self.rank_pop()

        fitness_for_graph = [f.get_fitness() for f in self.fish_pop]
        if graph:
            graph.add_gen(np.mean(fitness_for_graph), np.max(fitness_for_graph))
        print(f"Average fitness: {np.mean(fitness_for_graph):.2f}")
        print(f"Max fitness: {np.max(fitness_for_graph):.2f}")
            
        new_pop = []
        n_offspring_tot = int(N_FISH-PARENTS)
        n_offspring = int(n_offspring_tot/PARENTS)

        if CROSSOVER:
            n_offspring = int(n_offspring/2)
            
            weights_1 = best_fishes[0].get_genotype(mutation=False)
            weights_2 = best_fishes[1].get_genotype(mutation=False)
            for _ in range(n_offspring*PARENTS):
                new_weights = []
                for j in range(len(weights_1)):
                    if np.random.random() < 0.5:
                        new_weights.append(weights_1[j])
                    else:
                        new_weights.append(weights_2[j])
                new_pop.append(Fish(new_weights, best_fishes[0].color, best_fishes[0].gen+1))

        for fish in best_fishes:
            fish.eaten_food = 0
            fish.penalty = 0
            for _ in range(n_offspring):
                weights = fish.get_genotype(mutation=True)
                new_pop.append(Fish(weights, fish.color, fish.gen+1))
        new_pop.extend(best_fishes)
        self.fish_pop = new_pop


    def check_neighborhood(self):
        for f in self.fish_pop:
            f.check_neighborhood(self.fish_pop)

    def check_neighbors(self):
        neighbors_positions = []
        for f in self.fish_pop:
            neighbors_positions.append([f.position_x, f.position_y])
        for f in self.fish_pop:
            f.fish_sensors = [0,0,0,0]
            f.fish_angle = f.angle % (2*np.pi)
            min_distance = SOCIAL_RADIUS*4
            fish_per_quadrant = [0,0,0,0]
            for friend in neighbors_positions:
                if ((f.position_x-friend[0])**2 + (f.position_y-friend[1])**2)<SOCIAL_RADIUS**2:
                    f.fish_angle = - np.arctan2(friend[1]-f.position_y, friend[0]-f.position_x)
                    relative_angle = (f.angle - f.fish_angle) % (2*np.pi)
                    if relative_angle >=7*np.pi/4 and relative_angle < np.pi/4 :
                        fish_per_quadrant[0] += 1
                    elif relative_angle < 3*np.pi/4 and relative_angle >= np.pi/4 :
                        fish_per_quadrant[1] += 1
                    elif relative_angle >= 3*np.pi/4 and relative_angle < 5*np.pi/4:
                        fish_per_quadrant[2]+= 1
                    elif relative_angle >= 5*np.pi/4 and relative_angle < 7*np.pi/4:
                        fish_per_quadrant[3]+= 1

            f.fish_sensors[0] = sigmoid(fish_per_quadrant[0])
            f.fish_sensors[1] = sigmoid(fish_per_quadrant[1])
            f.fish_sensors[2] = sigmoid(fish_per_quadrant[2])
            f.fish_sensors[3] = sigmoid(fish_per_quadrant[3])
        
    def update_timer(self):
        self.count_timer += 1
        if self.count_timer >= REPRODUCTION_TIMER:
            self.count_timer = 0

def sigmoid(x):
    return 1/(1 + np.exp(-x))