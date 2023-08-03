import numpy as np
import matplotlib.pyplot as plt
from config import *
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def relu(x):
    return max(0, x)

def leaky_relu(x):
    return max(0.01*x, x)

def act_function_input(x):
    return x

def act_function_hidden(x):
    if ACTIVATION_FUNCTION == "tanh":
        return np.tanh(x)
    elif ACTIVATION_FUNCTION == "sigmoid":
        return sigmoid(x)
    elif ACTIVATION_FUNCTION == "linear":
        return x
    elif ACTIVATION_FUNCTION == "relu":
        return relu(x)
    elif ACTIVATION_FUNCTION == "leaky_relu":
        return leaky_relu(x)
    
def act_function_output(x):
    return sigmoid(x)

class NN():
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.activations = [[0 for i in range(node)] for node in nodes]
        self.nweights = sum([self.nodes[i] * self.nodes[i + 1] for i in
                             range(len(self.nodes) - 1)])  # nodes[0]*nodes[1]+nodes[1]*nodes[2]+nodes[2]*nodes[3]

        self.weights = [[] for _ in range(len(self.nodes) - 1)]

    def activate(self, inputs):
        self.activations[0] = [act_function_input(inputs[i]) for i in range(self.nodes[0])]
        for i in range(1, len(self.nodes)-1):
            self.activations[i] = [0. for _ in range(self.nodes[i])]
            for j in range(self.nodes[i]):
                sum = 0  # self.weights[i - 1][j][0]
                for k in range(self.nodes[i - 1]):
                    sum += self.activations[i - 1][k - 1] * self.weights[i - 1][j][k]
                self.activations[i][j] = act_function_hidden(sum)
        self.activations[-1] = [0. for _ in range(self.nodes[-1])]
        for i in range(self.nodes[-1]):
            sum = 0
            for j in range(self.nodes[-2]):
                sum += self.activations[-2][j] * self.weights[-1][i][j]
            self.activations[-1][i] = act_function_output(sum)
        
        return np.array(self.activations[-1])

    def set_weights(self, weights):
        # self.weights = [[] for _ in range(len(self.nodes) - 1)]
        c = 0
        for i in range(1, len(self.nodes)):
            self.weights[i - 1] = [[0 for _ in range(self.nodes[i - 1])] for __ in range(self.nodes[i])]
            for j in range(self.nodes[i]):
                for k in range(self.nodes[i - 1]):
                    self.weights[i - 1][j][k] = weights[c]
                    c += 1
        #print(c)

    def get_list_weights(self):
        wghts = []
        for i in range(1, len(self.nodes)):
            for j in range(self.nodes[i]):
                for k in range(self.nodes[i - 1]):
                    wghts.append(np.abs(self.weights[i - 1][j][k]))
        return wghts

