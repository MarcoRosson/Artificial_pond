# Type of Network
NETWORK_CONFIGURATION = 'angle_decisions' # 'angle_decisions', 'sensors_decisions'
COHESION = False # True, False

# Set screen size and FPS
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Population parameters
N_FISH = 25
PARENTS = 5

# Set food parameters
N_FOOD = 75
EAT_RADIUS = 4
HUNT_RADIUS = 300

# Set wall parameters (only for sensors_decisions)
WALL_RADIUS = 100

# Set fish parameters
ANGLE_MAG = 0.2

# Set reproduction parameters
MUTATION_MAG = 0.2
MUTATION_PROB = 0.6
CROSSOVER = False

# Set social parameters
NEIGHBORHOOD_TYPE = "local" # "global", "local"
SOCIAL_RADIUS = 300

# Set generations before screen visualization
GEN_BEFORE_SCREEN = 20




# DO NOT MODIFY THE FOLLOWING LINES
if NETWORK_CONFIGURATION == 'angle_decisions':
    
    NETWORK_LAYERS = [3, 3, 3]
    FISH_SPEED = 3
    REPRODUCTION_TIMER = 1000
    ACTIVATION_FUNCTION = "linear" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

    if COHESION:
        NETWORK_LAYERS = [4, 3, 3]

elif NETWORK_CONFIGURATION == 'sensors_decisions':

    NETWORK_LAYERS = [5, 3, 3, 4]
    FISH_SPEED = 1
    REPRODUCTION_TIMER = 500
    ACTIVATION_FUNCTION = "relu" # "tanh", "sigmoid", "linear", "relu", "leaky_relu"

    if COHESION:
        NETWORK_LAYERS = [9, 3, 3, 4]

    
    