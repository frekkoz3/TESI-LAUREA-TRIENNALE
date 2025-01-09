from graphics import *
from elements import *
if __name__ == "__main__":
    LENGHT = 20
    HEIGHT = 20
    pop = Population(5, initial_position=[[10, 10], [0, 0], [19, 19], [2, 3], [5, 18]])
    world = World(LENGHT, HEIGHT, density = 0.1)
    play(pop, world)