import pygame
import sys
from elements import *

# Draw the grid
def draw_world(screen, grid_world : World):
    height = grid_world.height
    length = grid_world.length
    side = grid_world.cell_side
    for i in range (height):
        for j in range (length):
            pygame.draw.rect(screen, grid_world[(i, j)].get_color(), pygame.Rect(i*side, j*side, side, side))

# Draw the agents
def draw_population(screen, pop : Population):
    side = pop.cell_side
    for individual in pop:
        x, y = individual.position
        color = individual.get_color()
        pygame.draw.rect(screen, color, pygame.Rect(x*side, y*side, side, side))

# Main game loop
def play(pop : Population, world : World):
    # Initialize PyGame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = world.length * world.cell_side , world.height * world.cell_side
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyGame Sketch")
    clock = pygame.time.Clock()

    # Add screen dimensions to `something`
    grid_world = world

    t = 0
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill((255, 255, 255))

        # Call the drawing functions
        draw_world(screen, grid_world)
        draw_population(screen, pop)

        pop.update(world)
        world.update()

        # Update the display
        pygame.display.flip()

        # Increment time and regulate frame rate
        t += 1
        clock.tick(2)

# Entry point
if __name__ == "__main__":
    world = World(15, 15)
    initial_position = [[random.randint(0, 14), random.randint(0, 14)] for i in range (5)]
    print(initial_position)
    pop = Population(5, initial_position)
    play(pop, world)
