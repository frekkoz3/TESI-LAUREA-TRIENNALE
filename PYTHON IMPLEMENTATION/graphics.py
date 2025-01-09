import pygame
import sys
from elements import *

BAR_HEIGHT = 100

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

# Draw the statistics bar
def draw_stats(screen, pop : Population, world : World):
    # Draw stats bar
    WIDTH, HEIGHT = world.length * world.cell_side , world.height * world.cell_side
    pygame.draw.rect(screen, (0, 55, 180), pygame.Rect(0, HEIGHT, WIDTH, BAR_HEIGHT))

    font = pygame.font.Font(None, 28)

    # For now we don't have real statistic, we are just trying to have the bar
    health_text = font.render(f"POPULATION SIZE", True, (200, 255, 255))
    score_text = font.render(f"CELL SIZE", True, (200, 255, 255))
    fps_text = font.render(f"AVG ENERGY", True,  (200, 255, 255))

    # This is done to actually "print"
    screen.blit(health_text, (10, HEIGHT + 10))
    screen.blit(score_text, (10, HEIGHT + 40))
    screen.blit(fps_text, (10, HEIGHT + 70))

# Main game loop
def play(pop : Population, world : World, verbose = False):
    # Initialize PyGame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = world.length * world.cell_side , world.height * world.cell_side
    TOTAL_HEIGHT = HEIGHT + BAR_HEIGHT
    screen = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
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

        pop.update(world, verbose)
        world.update()

        # Drawing the stats
        draw_stats(screen, pop, grid_world)

        # Update the display
        pygame.display.flip()

        # Increment time and regulate frame rate
        t += 1
        clock.tick(2)

# Entry point
if __name__ == "__main__":
    pass
