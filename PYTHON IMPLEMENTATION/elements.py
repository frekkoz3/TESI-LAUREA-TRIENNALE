"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from excpts import *
from decisions import *
from action_handler import *
import random

BLANK_COLOR = (210,250,250)
CELL_PARAMS = {"energy" : 0, "minimum" : 0, "maximum" : 0, "regeneration" : 0}
CELL_SIDE = 20
COSTS = {'Move_N' : 1, 'Move_W' : 1, 'Move_S' : 1, 'Move_E' : 1, 'Rest' : 0.1, 'Eat_1' : 0.1, 'Reproduce' : 5, 'Pollute' : 0.2}

class Cell():

    def __init__(self, parameters = {"energy" : 0, "minimum" : 0, "maximum" : 0, "regeneration" : 0}):
        # We need to tweak every parameter here. For now on we set all of them to 0 as default
        self.energy = parameters["energy"]
        self.minimum_energy_level = parameters["minimum"]
        self.maximum_energy_level = parameters["maximum"]
        self.regeneration_level = parameters["regeneration"]    

    def charge_energy(self, energy):
        # This function is built in case we want to give some enery at block to the cell
        self.energy = min(self.maximum_energy_level, energy)    
    
    def release_energy(self, request):
        # This function is built in case for when someone pick up the energy
        # We return how actual energy is released
        actual_energy = min (self.energy, request)
        self.energy = self.energy - actual_energy
        return actual_energy
    
    def update(self):
        if self.energy > self.minimum_energy_level:
            self.energy = min(self.maximum_energy_level, self.energy + self.regeneration_level)

    def get_color(self):
        if self.energy == 0:
            return BLANK_COLOR
        # For the color visualization we will have to think about it
        if self.energy < self.minimum_energy_level:
            return (255, 255*(self.energy/self.minimum_energy_level), 125)
        return (255, 255*(self.energy/self.maximum_energy_level), 0)

class World():

    def __init__(self, length, height, cell_energy = 10, parameters = {"energy" : 0, "minimum" : 5, "maximum" : 20, "regeneration" : 1}, density = 0.1, costs = COSTS):
        # The density parameter tell the portion of cells that should be activate
        self.length = length
        self.height = height
        self.cell_energy = cell_energy
        self.__cells__ = [[Cell(parameters) for l in range (length)] for h in range (height)]
        self.density = density
        self.cell_side = CELL_SIDE
        self.active = 0
        self.costs = costs
        self.populate()
    
    def populate(self):
        # For now we just activate the right amount of cells into the totals. Then we will think about more
        size = self.length * self.height
        to_activate_size = int(size * self.density) # We need an integer
        idxs = [i for i in range (size)]
        random.shuffle(idxs)
        to_activate_idxs = idxs[:to_activate_size]
        for idx in to_activate_idxs:
            self.__cells__[idx//self.length][idx%self.height].charge_energy(self.cell_energy)

    def update(self):
        self.active = 0
        for i in range(self.length):
            for j in range(self.height):
                self.__cells__[i][j].update()
                if self.__cells__[i][j].energy > 0:
                    self.active += 1
        if self.active == 0:
            return - 1 # This means all that the world is dead
        self.density = self.active/(self.length*self.height)
        return 0
    
    def __getitem__(self, idx) -> Cell:
        if type(idx) is not list and type(idx) is not tuple:
            print("Idx while accessing a cell must be in the format [i, j] or (i, j), hence list or tuple format.")
            raise WorldException
        if len(idx) != 2:
            print(f"Idx dimension must be exactly 2. Given : {len(idx)}.")
            raise WorldException
        return self.__cells__[idx[0]][idx[1]]
    
    def asList(self):
        # Return the idxs of the cell active as a list of tuples
        idxs = []
        for i in range (self.length):
            for j in range (self.height):
                if self.__cells__[i][j].energy > 0:
                    idxs.append((i, j))
        return idxs
    
class Individual():

    def __init__(self, max_age = 100, birth_energy = 20, max_energy = 30, social_param = [1, 0, 0], position = [0, 0]):
        # Now we have to consider that individual will born only once with prefixed values, then it 
        # will depends on the parents state at the moment of the birth
        self.age = 0
        self.max_age = max_age
        self.energy = birth_energy
        self.max_energy = max_energy
        self.selfishness_param = social_param[0]
        self.altruism_param = social_param[1]
        self.normality_param = social_param[2]
        self.position = position
        self.last_action = 'Rest'
        self.maturity = max_age//4 # For now we set as follow
        self.senility = max_age*3//4 # For now we set as follow
        self.dead = False

    def update(self, costs):
        if self.energy <= 0 or self.age >= self.max_age:
            self.energy = 0
            self.dead = True
            return self
        else:
            self.energy -= costs[self.last_action] # cost of the last action taken
            """
                BASAL METABOLISM - quadratic formula (an alternative could be a lorentzian)
                Am = Maximum Age
                Em = Maximum Energy
                k (in [0, 1]) = Maximum ratio of Em requested by the Metabolism (we have the y_vertex here)
                Resolving imposing x(0) = 0, x(Am) = 0 and Vertex in (Am/2, kEm) we obtain the following parameters
                    a = -(4*k*Em)/(Am^2), b = (4*k*Em)/(Am), c = 0

            """
            Am = self.max_age
            Em = self.max_energy
            k = 0.02 # PARAMETERS THAT CAN BE TWEAK
            metabolism = self.age*(-(4*k*Em/(Am*Am))*self.age + (4*k*Em/Am)) # x(ax + b)
            self.energy -= metabolism
            self.age += 1
            return None
    
    def die(self):
        self.energy = 0
        self.dead = True
        return self
    
    def action(self, pop, world : World, selfish, altruistic, normal, verbose = False):
        if self.dead == True: # This is not the right way to do but no matter now
            return 'Rest'
        # DECISION PROCESS
        selfish_decision = selfish.decision(self, pop, world)
        altruistic_decision = altruistic.decision(self, pop, world)
        normal_decision = normal.decision(self, pop, world)
        actual_decision = "Rest"
        # SAMPLE PROCESS
        sample = random.uniform(0, 1)
        if sample < self.selfishness_param:
            actual_decision = selfish_decision
        elif sample < self.altruism_param:
            actual_decision = altruistic_decision
        else:
            actual_decision = normal_decision
        # ACTION PROCESS
        split_decision = actual_decision.split("_")
        if split_decision[0] == 'Move':
            self.move(split_decision[1])
        elif split_decision[0] == 'Rest':
            self.rest()
        elif split_decision[0] == 'Eat':
            self.eat(float(split_decision[1]), world[self.position])
            actual_decision = 'Eat_1'
        elif split_decision[0] == 'Reproduce':
            self.reproduce(pop)
        elif split_decision[0] == 'Pollute':
            self.pollute()
        self.last_action = actual_decision
        if verbose:
            print(f"POSITION : {self.position} ; ENERGY : {self.energy}; AGE : {self.age} ; DECISION : {actual_decision}")
                
    def move(self, direction = 'N'):
        # It moves only in the 4 directions
        # And since it change the index the increment is opposite to the direction
        if direction == 'N':
            self.position = [self.position[0] - 1, self.position[1]]
        elif direction == 'S':
            self.position = [self.position[0] + 1, self.position[1]]
        elif direction == 'W':
            self.position = [self.position[0], self.position[1] - 1]
        elif direction == 'E':
            self.position = [self.position[0], self.position[1] + 1]

    def rest(self):
        # It just stays where it is
        pass

    def eat(self, request, cell : Cell):
        self.energy = min(self.energy + cell.release_energy(request), self.max_energy)

    def reproduce(self, pop):
        # To reproduce we are guaranteed to have 4 free cells in our neighbourhood
        # This should implement the classical evolution scheme
        # SOCIAL PARAM MUTATION
        mutation_1 = random.uniform(-0.1, 0.1)
        mutation_2 = random.uniform(-0.1, 0.1)
        mutation_3 = - (mutation_1 + mutation_2)
        son_social_param = [self.selfishness_param + mutation_1, self.altruism_param + mutation_2, self.normality_param + mutation_3] # THIS IS A MESS but work
        # AGE MUTATION
        age_mutation = random.uniform(0.9, 1.1)
        son_max_age = int(age_mutation*self.max_age)
        # BIRTH POSITION
        directions = { 1 : [0, 1], 2 : [0, -1], 3 : [-1, 0], 4 : [1, 0] }
        r_dir = random.randint(1, 4)
        son_position = [self.position[0] + directions[r_dir][0] , self.position[1] + directions[r_dir][1]]
        # BIRTH ENERGY
        son_energy = self.energy//4
        # MAX ENERGY 
        energy_mutation = random.uniform(0.9, 1.1)
        son_max_energy = self.max_energy * energy_mutation
        son = Individual( max_age=son_max_age, birth_energy=son_energy, max_energy=son_max_energy, position=son_position, social_param=son_social_param) # We should implement a lot of think here, don't worry for now
        self.energy = 3*self.energy//4 # This parameter is to tweak
        pop.birth(son)

    def pollute(self):
        pass

    def get_color(self):
        return (min(max(0, 255*self.selfishness_param), 255), min(max(0, 255*self.altruism_param), 255), min(max(0, 255*self.normality_param), 255))

        
class Population():

    def __init__(self, initial_population):
        # For now the processes stay here
        self.cell_side = CELL_SIDE
        self.__individuals__ = initial_population
        self.selfish_process = SelfishProcess()
        self.altruistic_process = AltruisticProcess()
        self.normal_process = NormalProcess()

    def __getitem__(self, idx):
        return self.__individuals__[idx]

    def birth(self, newOne):
        self.__individuals__.append(newOne)
    
    def death(self, individual):
        # We will try if this actually work
        self.__individuals__.remove(individual)
    
    def update(self, world : World, verbose = False):
        for i in range (len(self.__individuals__)):
            self.__individuals__[i].action(self, world, self.selfish_process, self.altruistic_process, self.normal_process, verbose)
            # HERE WE MUST think at the conflicts, do not worry now 
            # MAYBE they are already thinked in the processes system but i don't think 

        Dead = []
        for i in range (len(self.__individuals__)):
            ind = self.__individuals__[i].update(world.costs)
            if ind != None:
                Dead.append(ind)
        for i in range (len(Dead)):
            self.death(Dead[i])
        
        # COLLISION: the weaker die
        Dead = []
        for i in range (len(self.__individuals__)):
            for j in range(i + 1, len(self.__individuals__)):
                ind_i = self.__individuals__[i]
                ind_j = self.__individuals__[j]
                if ind_i.position == ind_j.position:
                    tie = ind_i if random.uniform(0, 1) < 0.5 else ind_j # Tie break
                    if ind_i.energy > ind_j.energy:
                        Dead.append(ind_j.die())
                    elif ind_j.energy > ind_i.energy:
                        Dead.append(ind_i.die())
                    else:
                        Dead.append(tie.die())

        # This trick is done to avoid multiple dead (can occours in the init)
        Dead = list(set(Dead))

        for i in range (len(Dead)):
            self.death(Dead[i])

        if len(self.__individuals__) == 0:
            return -1 # This means the population is all dead
        
        return 0

    def alive(self):
        return len(self.__individuals__)
        