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

# Mutation
MUTATION_MAG = 0.1
MUTATION_PROB = 0.6

# Set Test mode
TEST = False
if TEST:
    VERBOSE = True
    FPS = 3
    N_FISH = 2