"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from elements import *
import random

class initial_condition_handler():

    def __init__(self, init_conds : dict):
        self.init_conds = init_conds
        # World param
        self.height = init_conds["Height"]
        self.width = init_conds["Width"]
        # Cell params
        self.initially_alive = init_conds["Active"]
        self.c_min = init_conds["C_Min"]
        self.c_max = init_conds["C_Max"]
        self.c_regen = init_conds["C_Regen"]
        self.c_distr = init_conds["C_Distr"]
        # Pop params
        self.size = init_conds["Size"]
        self.i_energy = init_conds["I_Energy"]
        self.i_age = init_conds["I_Age"]
        self.i_distr = init_conds["I_Distr"]
        self.p_distr = init_conds["P_Distr"]
        # Cost params
        self.move_cost = init_conds["Move"]
        self.eat_cost = init_conds["Eat"]
        self.rest_cost = init_conds["Rest"]
        self.reproduce_cost = init_conds["Reproduce"]

        # THIS PARAMETERS FOR NOW CAN BE TEWAKED ONLY HERE FOR NOW
        self.base_radius = 4 # THIS IS AN IMPORTANT PARAMETERS -> this is were we set the first one
        self.maturity = 0.18

        self.energy_needed  = 0.6
        self.extra_energy = 0.2
        self.mutation_rate = 0.1
        self.energy_requested = 0.5

        self.world = self.world_handler()
        self.population = self.individual_handler()        

    def world_handler(self):
        world = World(self.width, self.height, cell_energy=(self.c_max+self.c_min)/2, parameters = {"energy" : 0, "minimum" : self.c_min, "maximum" : self.c_max, "regeneration" : self.c_regen}, costs=self.cost_handler(), initially_alive=self.initially_alive, distribution=self.c_distr)
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
                position[i] = [random.randrange(0, self.height), random.randrange(0, self.width)]

        #social_params = [Params[self.p_distr] + random.uniform(-Params[self.p_distr], Params[self.p_distr]) for _ in range (self.size)] 
        social_params = [[p + random.uniform(-p, p) for p in Params[self.p_distr]] for _ in range (self.size)]
        normalizing_sum = [sum(sp) for sp in social_params]
        social_params = [[sp/n_s for sp in social_params[i]] for i, n_s in enumerate(normalizing_sum)]
        population = Population([Individual(max_ages[i], birth_energies[i], max_energies[i], social_params[i], position[i], radius = self.base_radius, maturity = self.maturity, energy_needed = self.energy_needed, extra_energy = self.extra_energy, mutation_rate = self.mutation_rate, idx=i, energy_requested=self.energy_requested) for i in range (self.size)])
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
                }
    
    def begin(self):
        return self.population, self.world, str(self)
    
    def __str__(self):
        s = ""
        for k in list(self.init_conds.keys()):
            s += f"{k} : {self.init_conds[k]}\n"
        s += f"Radius : {self.base_radius}\n"
        s += f"Maturity : {self.maturity}\n"
        s += f"Energy Needed : {self.energy_needed}\n"
        s += f"Extra Energy : {self.extra_energy}\n"
        s += f"Energy Requeste : {self.energy_requested}\n"
        s += f"Mutation Rate : {self.mutation_rate}\n"
        return s

if __name__ == "__main__":
    pass