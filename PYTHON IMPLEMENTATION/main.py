"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from graphics import *
from elements import *
from initial_condition_gui import *
from initial_condition_handler import *
from off_graphics_simulation import *

if __name__ == "__main__":
    data = inital_condition_GUI()
    pop, world, init_cond = initial_condition_handler(data).begin()
    play_off_graphics(pop, world, init_cond, verbose = False, report=True)
