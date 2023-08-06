# Type of Network
NETWORK_CONFIGURATION = 'angle_decisions' # 'angle_decisions', 'sensors_decisions', 'direct_angle'
COESION = False # True, False
ALIGNMENT = False # True, False

# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60

# Set number of fish
N_FISH = 25

# Set number of food
N_FOOD = 75

# Set food probability
FOOD_PROB = 0.2

# Set food radius
EAT_RADIUS = 4

# Hunt radius
HUNT_RADIUS = 300

WALL_RADIUS = 100

# Angle magnitude
ANGLE_MAG = 0.2

# Set generations before screen
GEN_BEFORE_SCREEN = 10

# Parent selection
PARENTS = 5

# Mutation
MUTATION_MAG = 0.2
MUTATION_PROB = 0.4
#GENES_TO_MUTATE = 5

# Crossover
CROSSOVER = False

# Activation function
ACTIVATION_FUNCTION = "linear" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

# Life Loss
LIFE_LOSS = 0.08 # Life loss per frame
LIFE_LOSS_SPEED = 0.05 # Life loss per speed

# Neighborhood Center
NEIGHBORHOOD_TYPE_CENTER = "local" # "global", "local"
SOCIAL_RADIUS = 300


# DO NOT MODIFY THE FOLLOWING LINES
if NETWORK_CONFIGURATION == 'angle_decisions':
    
    NETWORK_LAYERS = [3, 3, 3]
    FISH_SPEED = 3
    REPRODUCTION_TIMER = 1000

    if COESION:
        NETWORK_LAYERS = [4, 3, 3]

elif NETWORK_CONFIGURATION == 'sensors_decisions':

    NETWORK_LAYERS = [5, 3, 3, 4]
    FISH_SPEED = 1
    REPRODUCTION_TIMER = 500

    if COESION:
        NETWORK_LAYERS = [9, 3, 3, 4]

    
    