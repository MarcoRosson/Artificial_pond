# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60

# Set screen output
VERBOSE = False

# Set number of fish
N_FISH = 50

# Set food probability
FOOD_PROB = 0.2

# Offspring
OFFSPRING = 2

# Mutation
MUTATION_MAG = 0.05
MUTATION_PROB = 0.2

# Activation function
ACTIVATION_FUNCTION = "tanh" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

# Life Loss
LIFE_LOSS = 0.08 # Life loss per frame
LIFE_LOSS_SPEED = 0.05 # Life loss per speed

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2