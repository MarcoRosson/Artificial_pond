# Sets the width and height of the game window
WIDTH = 1000
HEIGHT = 800

# Set FPS
FPS = 60

# Set screen output
VERBOSE = False

# Set number of fish
N_FISH = 20
N_FOOD = 100

# Set timer
TIMER = 100

# Set food probability
#FOOD_PROB = 0.2

# Mutation
MUTATION_MAG = 0.3
MUTATION_PROB = 0.4

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2