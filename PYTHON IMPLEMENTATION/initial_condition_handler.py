from elements import *
import random

class initial_condition_handler():

    def __init__(self, init_conds):
        self.height = init_conds["Height"]
        self.width = init_conds["Width"]
        self.density = init_conds["Active"]
        self.c_min = init_conds["C_Min"]
        self.c_max = init_conds["C_Max"]
        self.c_distr = init_conds["C_Distr"]
        self.world = self.world_handler()

        self.size = init_conds["Size"]
        self.i_energy = init_conds["I_Energy"]
        self.i_age = init_conds["I_Age"]
        self.i_distr = init_conds["I_Distr"]
        self.p_distr = init_conds["P_Distr"]
        self.population = self.individual_handler()

        self.move_cost = init_conds["Move"]
        self.eat_cost = init_conds["Eat"]
        self.rest_cost = init_conds["Rest"]
        self.reproduce_cost = init_conds["Reproduce"]
        self.costs = self.cost_handler()

    def world_handler(self):
        world = World(self.width, self.height, cell_energy=(self.c_max+self.c_min)/2, parameters = {"energy" : 0, "minimum" : self.c_min, "maximum" : self.c_max, "regeneration" : self.c_max/10})
        # WELL THERE ARE SOME PARAMETERS WE SHOULD IMPLEMENT BEFORE 
        return world

    def individual_handler(self):
        # For now we implement only the Uniform Distribution 
        Params ={
                    "Uniform" : [1/3, 1/3, 1/3], 
                    "Selfish" : [1, 0, 0], 
                    "Altruistic" : [0, 1, 0], 
                    "Normal" : [0, 0, 1], 
                    "Selfish-Altruistic" : [0.5, 0.5, 0], 
                    "Selfish-Normal" : [0.5, 0, 0.5], 
                    "Altruistic-Normal" : [0, 0.5, 0.5]
                }
        max_ages = [random.randint(max(0, self.i_age*3//4), self.i_age*5//4) for _ in range (self.size)] # We sample by a uniform in the range [avg_age * 0.75, avg_age * 1.25]
        max_energies = [random.randint(max(0, self.i_energy*3//4), self.i_energy*5//4) for _ in range (self.size)] # We sample by a uniform in the range [avg_energy * 0.75, avg_energy * 1.25]
        birth_energies = [max_en * random.uniform(0.25, 0.5) for max_en in max_energies] #  The birth energy is set as the max_energy by a random factor that goes from 0.25 to 0.5 -> MAYBE TO TWEAK 
        position = [[random.randrange(0, self.height), random.randrange(0, self.width)] for _ in range (self.size)] #  This is the uniform distribution init -> this should be implemented in the Population class!
        # This is needed to obtain unique positions
        for i in range (self.size):
            while position.count(position[i]) > 1:
                position[i] = [[random.randrange(0, self.height), random.randrange(0, self.width)] for _ in range (self.size)]
        social_params = [Params[self.p_distr] for _ in range (self.size)] # WE SHOULD TWEAK THIS A BIT WITH SOME RANDOM FLUTTUATION
        population = Population([Individual(max_ages[i], birth_energies[i], max_energies[i], social_params[i], position[i]) for i in range (self.size)])
        return population
    
    def cost_handler(self):
        return {
                    'Move_N' : self.move_cost, 
                    'Move_W' : self.move_cost, 
                    'Move_S' : self.move_cost, 
                    'Move_E' : self.move_cost, 
                    'Rest' : self.rest_cost, 
                    'Eat_1' : self.eat_cost, 
                    'Reproduce' : self.reproduce_cost, 
                    'Pollute' : 0.2
                }
    
    def begin(self):
        return self.population, self.world, self.costs
