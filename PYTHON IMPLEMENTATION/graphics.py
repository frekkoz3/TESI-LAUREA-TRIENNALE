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
def agents(something, t):
    agents_list = something.get("agents", [])
    for agent in agents_list:
        x, y = agent.get("position", (0, 0))
        color = agent.get("color", (0, 0, 255))
        radius = agent.get("radius", 10)
        pygame.draw.circle(something["screen"], color, (x-radius, y-radius), radius)

# Main game loop
def play(something, world : World, *args, **kwargs):
    # Initialize PyGame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = world.length * world.cell_side , world.height * world.cell_side
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyGame Sketch")
    clock = pygame.time.Clock()

    # Add screen dimensions to `something`
    grid_world = world
    something["width"] = WIDTH
    something["height"] = HEIGHT
    something["screen"] = screen

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
        agents(something, t)
        # Update the display
        pygame.display.flip()

        # Increment time and regulate frame rate
        t += 1
        clock.tick(2)

# Something object with grid and agent info
something = {
    "cell_size": 50,
    "agents": [
        {"position": (100, 100), "color": (0, 0, 255), "radius": 25},
        {"position": (200, 150), "color": (255, 0, 0), "radius": 25},
    ]
}

# Entry point
if __name__ == "__main__":
    w = World(15, 15, cell_side=50)
    play(something, w)
