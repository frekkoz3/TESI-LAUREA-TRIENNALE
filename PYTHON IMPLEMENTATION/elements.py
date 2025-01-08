from excpts import *
import random

BLANK_COLOR = (255, 255, 255)
CELL_PARAMS = {"energy" : 0, "minimum" : 0, "maximum" : 0, "regeneration" : 0}
CELL_SIDE = 10

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
        self.energy = max (0, self.energy - request)
    
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

    def __init__(self, length, height, cell_energy = 10, parameters = {"energy" : 0, "minimum" : 5, "maximum" : 20, "regeneration" : 1}, density = 0.1, cell_side = 5):
        # The density parameter tell the portion of cells that should be activate
        self.length = length
        self.height = height
        self.cell_energy = cell_energy
        self.__cells__ = [[Cell(parameters) for l in range (length)] for h in range (height)]
        self.density = density
        self.cell_side = cell_side
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

    def __init__(self):
        self.age = 0
        self.energy = 0
        self.social_params = [0, 0, 0] # Selfishness, Altruism, Normality
        pass

    def update(self):
        pass
    
    def action(self):
        pass

    def get_color(self):
        return (self.social_params[0], self.social_params[1], self.social_params[2])

        
class Population():

    def __init__(self, initial_population_size):
        self.__individuals__ = [Individual() for i in range (initial_population_size)]

    def __getitem__(self, idx):
        return self.__individuals__[idx]