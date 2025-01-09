from graphics import *
from elements import *
if __name__ == "__main__":
    LENGHT = 20
    HEIGHT = 20
    pop = Population(1, initial_position=[[10, 10]])
    world = World(LENGHT, HEIGHT, density = 0.05)
    play(pop, world, True)