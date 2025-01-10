from graphics import *
from elements import *
from initial_condition_gui import *
from initial_condition_handler import *
from common import POSSIBILITIES

if __name__ == "__main__":
    data = inital_condition_GUI()
    pop, world, POSSIBILITIES = initial_condition_handler(data).begin()
    play(pop, world)
