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
from initial_condition_handler import *

def write_report(reporter : StatsReporter, simulation_number : int, forced_end : bool = False):
    reporter.report(simulation_number, forced_end)

# Main game loop
def play_off_graphics(data : dict, verbose = True, report = True, t_max = 10000):

    n_simulations = data["N_Simulations"]
    pop, world, init_cond = initial_condition_handler(data).begin()

    if report:
        reporter = StatsReporter(initial_condition=init_cond, n_simulation=n_simulations) # We use the default path of the class    

    for actual_simulation in range(n_simulations):
        if verbose:
            print(f"Executing simulation number {actual_simulation}.")
        
        pop, world, init_cond = initial_condition_handler(data).begin()

        t = 0

        while True:
            
            if report:
                reporter.update(pop, world, actual_simulation)

            # Update population
            errn = pop.update(world)

            if errn == -1:
                print("Population Dead")
                if report:
                    write_report(reporter, actual_simulation)
                break
                

            # Update the world
            errn = world.update()
            if errn == -1:
                print("World Dead")
                if report:
                    write_report(reporter, actual_simulation)
                break

            # Increment time and regulate frame rate
            t += 1

            if t > t_max:

                if report:
                    write_report(reporter, actual_simulation)
                break

# Entry point
if __name__ == "__main__":
    pass
