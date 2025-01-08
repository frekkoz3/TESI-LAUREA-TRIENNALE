from excpts import *
from decisions import *
import random

BLANK_COLOR = (255, 255, 255)
CELL_PARAMS = {"energy" : 0, "minimum" : 0, "maximum" : 0, "regeneration" : 0}
CELL_SIDE = 20

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
            return (255*(self.energy/self.minimum_energy_level), 255, 255)
        return (255, 255*(self.energy/self.maximum_energy_level), 255)

class World():

    def __init__(self, length, height, cell_energy = 10, parameters = {"energy" : 0, "minimum" : 5, "maximum" : 20, "regeneration" : 1}, density = 0.1):
        # The density parameter tell the portion of cells that should be activate
        self.length = length
        self.height = height
        self.cell_energy = cell_energy
        self.__cells__ = [[Cell(parameters) for l in range (length)] for h in range (height)]
        self.density = density
        self.cell_side = CELL_SIDE
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
        active = 0
        for i in range(self.length):
            for j in range(self.height):
                self.__cells__[i][j].update()
                if self.__cells__[i][j].energy > 0:
                    active += 1
        self.density = active/(self.length*self.height)
    
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

    def __init__(self, max_age = 100, birth_energy = 10, social_param = [1/3, 1/3, 1/3], position = [0, 0]):
        # Now we have to consider that individual will born only once with prefixed values, then it 
        # will depends on the parents state at the moment of the birth
        self.age = 0
        self.max_age = max_age
        self.energy = birth_energy
        self.selfishness_param = social_param[0]
        self.altruism_param = social_param[1]
        self.normality_param = social_param[2]
        self.position = position
        self.last_action = 'Rest'

    def update(self, pop):
        if self.energy <= 0 or self.age >= self.max_age:
            pop.death(self)
        else:
            self.energy -= POSSIBILITIES[self.last_action]
            self.energy -= 1 # BASAL METABOLISM, TO IMPLEMENT
            self.age += 1
    
    def action(self, pop, world : World, selfish : SelfishProcess, altruistic : AltruisticProcess, normal : NormalProcess):
        selfish_decision = selfish.decision(self, pop, world)
        altruistic_decision = altruistic.decision(self, pop, world)
        normal_decision = normal.decision(self, pop, world)
        sample = random.uniform(0, 1)
        actual_decision = selfish_decision if sample < self.selfishness_param else altruistic_decision
        actual_decision = actual_decision if sample < self.altruism_param else normal_decision
        split_decision = actual_decision.split("_")
        if split_decision[0] == 'Move':
            self.move(split_decision[1])
        elif split_decision[0] == 'Rest':
            self.rest()
        elif split_decision[0] == 'Eat':
            self.eat(int(split_decision[1]), world[self.position])
            actual_decision = 'Eat_1'
        elif split_decision[0] == 'Reproduce':
            self.reproduce(pop)
        elif split_decision[0] == 'Pollute':
            self.pollute()
        self.last_action = actual_decision
                
    def move(self, direction = 'N'):
        # It moves only in the 4 directions
        if direction == 'N':
            self.position = [self.position[0] + 1, self.position[1]]
        elif direction == 'S':
            self.position = [self.position[0] - 1, self.position[1]]
        elif direction == 'W':
            self.position = [self.position[0], self.position[1] - 1]
        elif direction == 'W':
            self.position = [self.position[0], self.position[1] + 1]

    def rest(self):
        # It just stays where it is
        pass

    def eat(self, request, cell : Cell):
        self.energy += cell.release_energy(request)

    def reproduce(self, pop):
        # This should implement the classical evolution scheme
        son = Individual() # We should implement a lot of think here, don't worry for now
        self.energy *= 0.5 # This parameter is to tweak
        pop.birth(son)

    def pollute(self):
        pass

    def get_color(self):
        return (255*self.selfishness_param, 255*self.altruism_param, 255*self.normality_param)

        
class Population():

    def __init__(self, initial_population_size, initial_position):
        # For now the processes stay here
        self.cell_side = CELL_SIDE
        self.__individuals__ = [Individual(position=initial_position[i]) for i in range (initial_population_size)]
        self.selfish_process = SelfishProcess()
        self.altruistic_process = AltruisticProcess()
        self.normal_process = NormalProcess()

    def __getitem__(self, idx):
        return self.__individuals__[idx]

    def birth(self, newOne):
        self.__individuals__.append(newOne)
    
    def death(self, individual):
        # We will try if this actually work
        #self.__individuals__.remove(individual)
        pass
    
    def update(self, world : World):
        for i in range (len(self.__individuals__)):
            self.__individuals__[i].action(self, world, self.selfish_process, self.altruistic_process, self.normal_process)
            # HERE WE MUST think at the conflicts, do not worry now 
            # MAYBE they are already thinked in the processes system but i don't think 
        for i in range (len(self.__individuals__)):
            self.__individuals__[i].update(self)
            # Not sure the individual death works
        