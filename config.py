# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60

# Set screen output
VERBOSE = False

# Set number of fish
N_FISH = 20

# Set number of food
N_FOOD = 80

# Set food probability
FOOD_PROB = 0.2

# Hunt radius
HUNT_RADIUS = 100

# Angle magnitude
ANGLE_MAG = 0.2

# Set reproduction timer
REPRODUCTION_TIMER = 1000

# Parent selection
# PARENTS = 3

# # Mutation
# MUTATION_MAG = 0.05
# MUTATION_PROB = 0.1

# Activation function
#ACTIVATION_FUNCTION = "linear" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

# Life Loss
LIFE_LOSS = 0.08 # Life loss per frame
LIFE_LOSS_SPEED = 0.05 # Life loss per speed

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2