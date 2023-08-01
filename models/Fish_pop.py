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
            weights = NN_WEIGHTS_FACTOR*[np.random.random() for _ in range(6)]
            for i, _ in enumerate(weights):
                if np.random.random() < 0.5:
                    weights[i] *= -1
                # if np.random.random() < 0.5:
                #     weights[i] = 0
            
            # # with this weights it works fine
            # weights = [1, -1] # weight[0] is for input[1]

            self.fish_pop.append(Fish(weights))

    def fish_pop_step(self, food, screen=None, graph=None):
        if screen:
            self.draw(screen)

        self.update_position()
        self.check_food(food)
        self.eat_food(food)

        if (self.count_timer % 5) == 0:
            self.eval_pop()
        
        
        self.update_timer()
        if self.count_timer == 0:
            self.replace_pop(graph)
            generations = set([f.gen for f in self.fish_pop])
            print("Generation: ", generations)

    def eval_pop(self):
        for f in self.fish_pop:
            f.eval()

    def update_position(self):
        for f in self.fish_pop:
            f.update_position()

    def draw(self, screen):
        max_eaten_food = 1  
        max_fitness = 1
        for f in self.fish_pop:
            if f.get_eaten_food() > max_eaten_food:
                max_eaten_food = f.get_eaten_food()
            if f.get_fitness() > max_fitness:
                max_fitness = f.get_fitness()
        
        for f in self.fish_pop:
            f.draw(screen, max_eaten_food, max_fitness)

    def check_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish_pop:
            f.food_angle = f.angle % (2*np.pi)
            min_distance = HUNT_RADIUS*4
            for mcnugget in food_positions:
                if f.target_on == 0 and (((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<HUNT_RADIUS**2):
                    distance = np.sqrt((mcnugget[0]-f.position_x)**2 + (mcnugget[1]-f.position_y)**2)
                    if distance < min_distance:
                        f.food_angle = - np.arctan2(mcnugget[1]-f.position_y, mcnugget[0]-f.position_x)
                        min_distance = distance
                        f.target_on = 1
                        f.current_target = mcnugget

                if f.target_on == 1 and (((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)<HUNT_RADIUS**2):
                    f.food_angle = - np.arctan2(f.current_target[1]-f.position_y,f.current_target[0]-f.position_x)
                else :
                    f.target_on = 0
                    f.current_target = [0,0]

            f.food_distance = min_distance

    def eat_food(self, food):
        food_positions = food.get_positions()
        for f in self.fish_pop:
            for index, mcnugget in enumerate(food_positions):
                if ((f.position_x-mcnugget[0])**2 + (f.position_y-mcnugget[1])**2)< EAT_RADIUS**2:
                    food_positions.remove(mcnugget)
                    food.remove_food(index)
                    f.target_on = 0
                    f.eat_food()

                    # if len(f.decisions) <= DECISIONS:
                    #     dec = np.asarray(f.decisions)
                    #     diff_dec = np.diff(dec)
                    #     if np.sum(diff_dec) != 0:
                    #         f.eaten_food += 1
                    #         # f.decisions = []
                    # elif len(f.decisions) > DECISIONS:
                    #     last_i = len(f.decisions)-1
                    #     dec = np.asarray(f.decisions[last_i-DECISIONS:-1])
                    #     diff_dec = np.diff(dec)
                    #     if np.sum(diff_dec) != 0:
                    #         f.eaten_food += 1
                    #         # f.decisions = []

                    # f.fitness = f.get_fitness() 

    def rank_pop(self):
        ranked_pop = sorted(self.fish_pop, key=lambda x: x.get_fitness(), reverse=False)
        return ranked_pop[:PARENTS]
    
    def replace_pop(self, graph=None):
        best_fishes = self.rank_pop()

        if graph:
            fitness_for_graph = [f.get_fitness() for f in best_fishes]
            graph.add_gen(np.mean(fitness_for_graph), np.max(fitness_for_graph))

        
        # Parents Genotype
        for i,f in enumerate(best_fishes):
            print("\nParent ", i,' : ',f.get_genotype(mutation=False))
            print("\tFitness: ", i,' : ', f.get_fitness())

        new_pop = []
        n_offspring_tot = int(N_FISH-PARENTS)
        n_offspring = int(n_offspring_tot/PARENTS)
        print('n_offsprings: ',n_offspring)

        for fish in best_fishes:
            
            # reset and append parent
            fish.eaten_food = 0
            fish.fitness = 0
            fish.decisions = []
            new_pop.append(fish)

            # create offspring
            if VERBOSE:
                print("Fish ", fish.get_genotype(mutation=False))
            for i in range(n_offspring):
                weights = fish.get_genotype(mutation=True)
                new_pop.append(Fish(weights, fish.color, fish.gen+1))
            
    
        # new_pop.extend(best_fishes)

        # New Pop Genotype
        print('length new pop: ', len(new_pop))
        for i,f in enumerate(new_pop):
            print("Fish ", i,' : ', f.get_genotype(mutation=False))

        self.fish_pop = new_pop
        
    def update_timer(self):
        self.count_timer += 1
        if self.count_timer >= REPRODUCTION_TIMER:
            self.count_timer = 0