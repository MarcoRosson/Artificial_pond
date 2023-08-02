# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60

# Set screen output
VERBOSE = False

# Set number of fish
N_FISH = 25

# Set number of food
N_FOOD = 70

# Set food probability
FOOD_PROB = 0.2

# Hunt radius
HUNT_RADIUS = 100

# Angle magnitude
ANGLE_MAG = 0.2

# Set reproduction timer
REPRODUCTION_TIMER = 1000

# Set generations before screen
GEN_BEFORE_SCREEN = 20

# Parent selection
PARENTS = 5

# Mutation
MUTATION_MAG = 0.1
MUTATION_PROB = 0.3
#GENES_TO_MUTATE = 5

# Crossover
CROSSOVER = True

# Activation function
ACTIVATION_FUNCTION = "linear" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

# Life Loss
LIFE_LOSS = 0.08 # Life loss per frame
LIFE_LOSS_SPEED = 0.05 # Life loss per speed

# Neighborhood 
NEIGHBORHOOD_TYPE = "local" # "global", "local"
NEIGHBORHOOD_RADIUS = 300

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2