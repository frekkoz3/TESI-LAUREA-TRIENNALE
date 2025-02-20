"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""

from elements import *
from vector import *
from stats_reporter import *

def write_report(reporter : StatsReporter):
    reporter.report()

def play_off_graphics(pop : Population, world : World, init_cond : str, verbose = False, report = True, t_max = 10000):
    if report:
        reporter = StatsReporter(initial_condition=init_cond) # We use the default path of the class

    t = 0
    while True:
        if report:
            reporter.update(pop, world)
        # Update population
        errn = pop.update(world)
        if errn == -1:
            print("Population Dead")
            if report:
                write_report(reporter)
            break
        # Update the world
        errn = world.update()
        if errn == -1:
            print("World Dead")
            if report:
                write_report(reporter)
            break
        # Increment time and regulate frame rate
        t += 1

        if verbose:
            if t%100 == 0:
                print(t)

        if t > t_max:
            print("Time exceeded")
            if report:
                write_report(reporter)
            break

if __name__ == "__main__":
    pass