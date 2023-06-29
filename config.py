# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60
GEN_BEFORE_SCREEN = 300

# Set screen output
VERBOSE = False

# Set number of fish
N_FISH = 20
NN_WEIGHTS_FACTOR = 1

# Set number of food
N_FOOD = 40

# Hunt radius
HUNT_RADIUS = 100
EAT_RADIUS = 8
SPEED = 1

# Decisions
DECISIONS = 50

# Angle magnitude
ANGLE_MAG = 1.2

# Set reproduction timer
REPRODUCTION_TIMER = 300

# Parent selection
PARENTS = 1

# Mutation
MUTATION_MAG = 0.1
MUTATION_PROB = 0.3

# Activation function
ACTIVATION_FUNCTION = "linear" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2
