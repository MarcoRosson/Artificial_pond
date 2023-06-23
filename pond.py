import pygame
from models.Fish_pop import Fish_pop
from models.Food_pop import Food_pop
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets
from config import *
from models.Graph import Graph
import sys

def write_config_file(config):
    with open('config.txt', 'w') as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")
    print("Config file created successfully.")


# parents = [2,3,4]
# mutation_mag = [0.05, 0.1, 0.15, 0.2]
# mutation_prob = [0.1, 0.2, 0.3, 0.4]
parents = [4]
mutation_mag = [0.02, 0.05]
mutation_prob = [0.1, 0.2]
activation_function = ["tanh"]

for p in parents:
    for m_mag in mutation_mag:
        for m_prob in mutation_prob:
            for act_func in activation_function:
                gen = 0
                config = {
                    'parents': p,
                    'mutation_mag': m_mag,
                    'mutation_prob': m_prob,
                    'activation_function': act_func,
                }
                write_config_file(config)

                graph = Graph()

                population = Fish_pop()
                food = Food_pop()

                screen = None
                non_screen_iterations = REPRODUCTION_TIMER*30
                for it in range(non_screen_iterations):
                    if len(food) < N_FOOD:
                        food.spawn_food()
                    population.fish_pop_step(food, screen, graph)

                graph.save_graph_jpg(f"parents={p}_mutation_mag={m_mag}_mutation_prob={m_prob}")

sys.exit()

#graph = Graph()

population = Fish_pop()
food = Food_pop()

screen = None
non_screen_iterations = REPRODUCTION_TIMER*30
for _ in range(non_screen_iterations):
    if len(food) < N_FOOD:
        food.spawn_food()
    population.fish_pop_step(food, screen)

#graph.save_graph_jpg()

# #sys.exit()

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

slider = Slider(screen, 30, 20, 200, 10, min=10, max=240, step=5, colour=(10, 200, 50), initial=FPS)
output = TextBox(screen, 230, 5, 40, 30, fontSize=20)
output.disable()

# Main game loop
running = True
iterations = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame_widgets.update(event)
    output.setText(slider.getValue())

    # Update and draw particles
    population.fish_pop_step(food, screen)
    
    if VERBOSE:
        population.dead_born()
    
    food.draw(screen)

    if len(food) < N_FOOD:
        food.spawn_food()

    pygame.display.flip()
    clock.tick(slider.getValue()) # FPS

    # iterations += 1
    # if iterations >= 1000000:
    #     running = False

# Quit Pygame
pygame.quit()
