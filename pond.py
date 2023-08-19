import pygame
from models.Fish_pop import Fish_pop
from models.Food_pop import Food_pop
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets
from config import *
from models.Graphs import Graph

# Initialize the fish population and food population
population = Fish_pop()
food = Food_pop()

# Initialize the graph
graph = Graph()

# Run the simulation for some iterations before displaying the screen
screen = None
non_screen_iterations = REPRODUCTION_TIMER * GEN_BEFORE_SCREEN
for _ in range(non_screen_iterations):
    population.fish_pop_step(food, screen, graph)
    if len(food) < N_FOOD:
        food.spawn_food()
        
# Save the graph
if COHESION:
    graph.save_graph_jpg(f"graph_{NETWORK_CONFIGURATION}_cohesion")
else:
    graph.save_graph_jpg(f"graph_{NETWORK_CONFIGURATION}")

# Initialize the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialize the slider for FPS
slider = Slider(screen, 30, 20, 200, 10, min=10, max=240, step=5, colour=(10, 200, 50), initial=FPS)
output = TextBox(screen, 230, 5, 40, 30, fontSize=20)
output.disable()

# Start the display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame_widgets.update(event)
    output.setText(slider.getValue())
    
    population.fish_pop_step(food, screen)
    food.draw(screen)

    if len(food) < N_FOOD:
        food.spawn_food()

    pygame.display.flip()
    clock.tick(slider.getValue()) # FPS

pygame.quit()
