"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # THIS SHOULD RESOLVE THE ANNOYING MESSAGE 
import pygame
import sys
from elements import *
import tkinter as tk
from tkinter import messagebox
import math
from vector import *
from stats_reporter import *
from initial_condition_handler import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BAR_HEIGHT = 100

BACKGROUND_COLOR = (245,245,220)

FPS = 20

def write_report(reporter : StatsReporter, simulation_number : int, forced_end : bool = False):
    reporter.report(simulation_number, forced_end)

# For the message dialog window 
def message_dialog(text):
            root = tk.Tk()
            root.withdraw()  # This is done to hide the root
            messagebox.showinfo("Message", text)
            root.destroy()

def draw_arrow(screen, start, vector, cell_side, color=(0, 0, 255), arrow_size=3, void_visualization = False):
    if not void_visualization:
        if vector[0]==0 and vector[1]==0:
            return 
    """ Draws an arrow from start position in the direction of vector """
    end = (start[0] + vector[0] * (cell_side // 3), 
           start[1] + vector[1] * (cell_side // 3))

    pygame.draw.line(screen, color, start, end, 2)

    # Calculate arrowhead
    angle = math.atan2(vector[1], vector[0])
    left_wing = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
                 end[1] - arrow_size * math.sin(angle - math.pi / 6))
    right_wing = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end[1] - arrow_size * math.sin(angle + math.pi / 6))

    pygame.draw.polygon(screen, color, [end, left_wing, right_wing])

# Draw the grid
def draw_world(screen, grid_world : World, field_visualization = False):
    height = grid_world.height
    length = grid_world.length
    side = grid_world.cell_side
    information = grid_world.get_information()
    for i in range (height):
        for j in range (length):
            pygame.draw.rect(screen, grid_world[(i, j)].get_color(), pygame.Rect(i*side, j*side, side, side))
            if field_visualization:
                # drawing the information field 
                info = information[i][j].value
                if isinstance(info, Vector):
                    x, y = i * side, j * side
                    norm = info.norm() if info.norm() > 0 else 1
                    normalized_v = info * (1/norm) 
                    start_pos = (x + side//2, y + side//2)
                    draw_arrow(screen, start_pos, (normalized_v.x, normalized_v.y), side)
    
# Draw the agents
def draw_population(screen, pop : Population, grid_world : World, neigh_visualization = False):
    side = pop.cell_side
    font = pygame.font.Font(None, side)  # Default font
    for individual in pop:
        x, y = individual.position
        color = individual.get_color()
        circle_pos = (x*side + side/2, y*side + side/2)
        pygame.draw.circle(screen, color, circle_pos, side/2)
        text_surface = font.render(str(individual.idx), True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=circle_pos)  # Center text on the circle
        screen.blit(text_surface, text_rect)
        if neigh_visualization:
            neigh = grid_world.get_neighbourhood_clip(individual.position, 4)
            target_rect = pygame.Rect(neigh[0]*side, neigh[1]*side, (neigh[2] - neigh[0])*side, (neigh[3] - neigh[1])*side)
            neigh_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            col = list(individual.get_color())
            col[3] = 50
            pygame.draw.rect(neigh_surface, col, neigh_surface.get_rect())
            screen.blit(neigh_surface, target_rect)        

# Draw the statistics bar
def draw_stats(screen, pop : Population, world : World, camera_x, camera_y, zoom_level, time):

    font = pygame.font.Font(None, 18)

    # Draw the graphic stats
    camera_text = font.render(f"({int(camera_x)}, {int(camera_y)})", True, (0, 0, 0))
    zoom_text = font.render(f"{zoom_level:.2f}x", True, (0, 0, 0))
    screen.blit(camera_text, (10, SCREEN_HEIGHT - BAR_HEIGHT - 30))
    screen.blit(zoom_text, (SCREEN_WIDTH - 40, SCREEN_HEIGHT - BAR_HEIGHT - 30))

    pop_size = pop.alive()
    cell_size = world.alive()
    avg_energy = pop.mean_energy

    # For now we don't have real statistic, we are just trying to have the bar
    health_text = font.render(f"POPULATION SIZE {pop_size}", True, (200, 255, 255))
    score_text = font.render(f"CELL SIZE {cell_size}", True, (200, 255, 255))
    fps_text = font.render(f"AVG ENERGY {avg_energy}", True,  (200, 255, 255))
    

    # This is done to actually "print"
    screen.blit(health_text, (10, SCREEN_HEIGHT - BAR_HEIGHT + 10))
    screen.blit(score_text, (10, SCREEN_HEIGHT - BAR_HEIGHT + 40))
    screen.blit(fps_text, (10, SCREEN_HEIGHT - BAR_HEIGHT + 70))

    font = pygame.font.Font(None, 12)
    time_text = font.render(f"{time}", True,  (200, 255, 255))
    screen.blit(time_text, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - BAR_HEIGHT + 10))

# Main game loop
def play(data : dict, verbose = False, report = True, t_max = 10000):

    n_simulations = data["N_Simulations"]
    pop, world, init_cond = initial_condition_handler(data).begin()

    if report:
        reporter = StatsReporter(initial_condition=init_cond, n_simulation=n_simulations) # We use the default path of the class    

    for actual_simulation in range(n_simulations):

        print(f"Simulation number {actual_simulation}")
        
        # Initialize PyGame
        pygame.init()
        pop, world, init_cond = initial_condition_handler(data).begin()
        # Screen setup
        WIDTH, HEIGHT = world.length * world.cell_side , world.height * world.cell_side

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SOCIAL SIMULATION")

        # This is the surface where we draw the world
        w_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
        clock = pygame.time.Clock()

        grid_world = world

        # Camera position
        camera_x, camera_y = 0, 0

        # Zoom level
        zoom_level = 1.0
        min_zoom, max_zoom = 0.5, 2.0  # Set zoom limits

        # Dragging state
        dragging = False
        last_mouse_pos = (0, 0)

        t = 0

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if report:
                        write_report(reporter, actual_simulation, forced_end = True)
                    pygame.quit()
                    sys.exit()
                # THIS IS DONE FOR THE CAMERA
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        dragging = True
                        last_mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        # Calculate the difference in mouse movement
                        dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                        # Update camera position
                        camera_x -= dx
                        camera_y -= dy
                        # Clamp the camera position to stay within the world bounds
                        camera_x = max(0, min(camera_x, WIDTH - SCREEN_WIDTH))
                        camera_y = max(0, min(camera_y, HEIGHT - SCREEN_HEIGHT))
                        # Update the last mouse position
                        last_mouse_pos = event.pos
                # THIS IS DONE FOR THE ZOOM
                elif event.type == pygame.MOUSEWHEEL:
                    # Adjust zoom level
                    old_zoom = zoom_level
                    zoom_level += event.y * 0.1
                    zoom_level = max(min_zoom, min(max_zoom, zoom_level))  # Clamp zoom level
                    
                    # Adjust camera position to zoom in/out towards the mouse pointer
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_mouse_x = camera_x + mouse_x / old_zoom
                    world_mouse_y = camera_y + mouse_y / old_zoom
                    camera_x = world_mouse_x - (mouse_x / zoom_level)
                    camera_y = world_mouse_y - (mouse_y / zoom_level)

                    # Clamp the camera position
                    camera_x = max(0, min(camera_x, WIDTH - SCREEN_WIDTH/zoom_level))
                    camera_y = max(0, min(camera_y, HEIGHT - SCREEN_HEIGHT/zoom_level))

            # Clear the screen
            screen.fill((255, 255, 255, 255))

            if report:
                reporter.update(pop, world, actual_simulation)

            # Update population
            errn = pop.update(world)

            if errn == -1:
                print("Population Dead")
                if report:
                    write_report(reporter, actual_simulation)
                pygame.quit()
                break
                

            # Update the world
            errn = world.update()
            if errn == -1:
                print("World Dead")
                if report:
                    write_report(reporter, actual_simulation)
                pygame.quit()
                break

            # Call the drawing functions
            draw_world(w_surface, grid_world)
            draw_population(w_surface, pop, grid_world)
            
            # This is needed to scale the world surface based on the zoom
            scaled_world = pygame.transform.smoothscale(
                w_surface, 
                (int(WIDTH * zoom_level), int(HEIGHT * zoom_level))
            )
            screen.blit(scaled_world, (0, 0), (camera_x * zoom_level, camera_y * zoom_level, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # This is the stats bar
            stat_bar = pygame.Surface((SCREEN_WIDTH, BAR_HEIGHT))
            stat_bar.fill((65,105,225))
            screen.blit(stat_bar, (0, SCREEN_HEIGHT - BAR_HEIGHT))

            # Drawing the stats
            draw_stats(screen, pop, grid_world, camera_x*zoom_level//CELL_SIDE, camera_y*zoom_level//CELL_SIDE, zoom_level, t)        

            # Update the display
            pygame.display.flip()

            # Increment time and regulate frame rate
            t += 1

            if t > t_max:

                if report:
                    write_report(reporter, actual_simulation)
                pygame.quit()
                break
                

            clock.tick(FPS)

    sys.exit()

# Entry point
if __name__ == "__main__":
    pass
