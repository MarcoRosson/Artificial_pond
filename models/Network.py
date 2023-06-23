import numpy as np
import matplotlib.pyplot as plt
from config import *
import math

def read_config_file():
        config = {}
        with open('config.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value
        return config

ACTIVATION_FUNCTION = read_config_file()['activation_function']

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def relu(x):
    return max(0, x)

def leaky_relu(x):
    return max(0.01*x, x)

def act_function(x):
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
    


class NN():
    def __init__(self, nodes: list):
        self.nodes = nodes
        self.activations = [[0 for i in range(node)] for node in nodes]
        self.nweights = sum([self.nodes[i] * self.nodes[i + 1] for i in
                             range(len(self.nodes) - 1)])  # nodes[0]*nodes[1]+nodes[1]*nodes[2]+nodes[2]*nodes[3]

        self.weights = [[] for _ in range(len(self.nodes) - 1)]

    def activate(self, inputs):
        self.activations[0] = [act_function(inputs[i]) for i in range(self.nodes[0])]
        for i in range(1, len(self.nodes)):
            self.activations[i] = [0. for _ in range(self.nodes[i])]
            for j in range(self.nodes[i]):
                sum = 0  # self.weights[i - 1][j][0]
                for k in range(self.nodes[i - 1]):
                    sum += self.activations[i - 1][k - 1] * self.weights[i - 1][j][k]
                self.activations[i][j] = act_function(sum)
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

