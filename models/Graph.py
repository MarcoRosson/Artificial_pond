import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.generations = []
        self.fitness = []
        self.max_fitness = []
        self.current_gen = 0
    def add_gen(self, mean_fit, max_fit):
        self.generations.append(self.current_gen)
        self.fitness.append(mean_fit)
        self.max_fitness.append(max_fit)
        self.current_gen += 1
    def save_graph_jpg(self, title="graph"):
        print("Saving graph...")
        plt.plot(self.generations, self.fitness, color='blue')
        plt.plot(self.generations, self.max_fitness, color='red')
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.legend(['Mean Fitness', 'Max Fitness'], loc='upper left')
        plt.savefig(f"{title}.jpg")
        plt.clf()
