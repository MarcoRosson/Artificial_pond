# Artificial_pond
Repository for Bio-inspired AI project

## Installation
In order to run the project, you need to install the following packages: 

**Numpy**:
```bash
pip install numpy
```
**Matplotlib**:
```bash
pip install matplotlib
```
**Pygame**:
```bash
pip install pygame
```

**Pygame-widgets**:
```bash
pip install pygame-widgets
```

The project has been developed using Python 3.10.9 and the following versions of the packages:

* Numpy 1.25.0
* Matplotlib 3.7.1
* Pygame 2.5.0
* Pygame-widgets 1.1.1

## Usage
In order to run the project, you need to first clone the repository:
```bash
git clone https://github.com/MarcoRosson/Artificial_pond.git
```
Then, you need to change the parameters in the file `config.py`. The meaning of each parameter will be explained in the next section. 

Finally, you can run the project by typing:
```bash
python pond.py
```

The program will start evaluating a number of generations equal to the one specified in the `config.py` file via the parameter **GEN_BEFORE_SCREEN**. After that, the program will save a graph showing the average and max fitness of the population for each generation and will display the individual from the final generation. The evolution process will continue also when the screen is shown, but the graph will not be updated.

## Config.py parameters
### Network parameters
* **NETWORK_CONFIGURATION**: is used to decide the configuration of the used network and the corresponding input, as well as some behavioural parameters. It can be set to:
  * **"angle_decisions"**: the network will have 3 inputs, corresponding to the orientation of the fish, the angle between the fish and the food and the distance between the fish and food. The network will have 3 outputs, corresponding to the decision of turning left, right or going straight.
  * **"sensors_decisions"**: In this case the inputs are the sensors surrounding the agents, that can capture the presence of food or other agents, as well as the presence of walls. The outputs are the same as before with the addition of a fourth output, corresponding to the decision of inverting the angle.

* **COHESION**: allows the fish to be aware or not of the presence of other fish

### Display parameters
* **WIDTH** and **HEIGHT**: the width and height of the screen
* **FPS**: the number of frames per second of the simulation

### Population parameters
* **N_FISH**: the number of agents in the population for each generation
* **PARENTS**: the number of parents that will produce the next generation The best parents are chosen according to their fitness and will generate an equal number of children

### Food parameters
* **N_FOOD**: the number of food sources in the pond
* **EAT_RADIUS**: the maximum distance from which the fish can eat the food
* **HUNT_RADIUS**: the maximum distance from which the fish can see the food

### Walls parameters
* **WALL_RADIUS**: the maximum distance from which the fish can see the walls. Note that this parameter is used also with the '"angle_decisions"' configuration

### Fish parameters
* **ANGLE_MAG**: the angle that the fish can turn in one step

### Reproduction parameters
* **MUTATION_MAG**: the standard deviation of the gaussian distribution used to mutate the weights of the network
* **MUTATION_PROB**: the probability of mutating a weight
* **CROSSOVER**: if enabled, part of the offspring will be generated via crossover between the two best parents

### Social parameters
* **NEIGHBOUR_TYPE**: defines if the fish can see all the other fish ("global") or only the ones in a certain radius ("local")
* **SOCIAL_RADIUS**: the radius in which the fish can see the other fish, if 'NEIGHBOUR_TYPE' is set to "local"

### Non screen parameters
* **GEN_BEFORE_SCREEN**: the number of generations that will be evaluated before showing the screen

### Other parameters
The **config.py** file contains also other parameters that are not meant to be changed by the user. These parameters are dependent on the previous ones and are meant to maximize the performance of the program, depending on the chosen parameters.