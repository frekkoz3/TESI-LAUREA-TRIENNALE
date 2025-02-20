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
import math
from vector import *

BLANK_COLOR = (210,240,240)
CELL_PARAMS = {"energy" : 0, "minimum" : 0, "maximum" : 0, "regeneration" : 0}
CELL_SIDE = 20
COSTS = {
                    'Move_N' : 1, 
                    'Move_W' : 1, 
                    'Move_S' : 1, 
                    'Move_E' : 1, 
                    'Rest' : 1, 
                    'Eat_1' : 1, 
                    'Reproduce' : 1, 
                } # This is a default costs table just in case

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
    
    def __str__(self):
        return f"{self.energy}"

class Information():
    # This Object store the information transmitted by others
    def __init__(self):
        """
            The value can be of 2 type:
            None -> no information is known
            Vector -> this is a vector that hints where the food is : if infty is the vector magnitude an individual is present
        """
        self.vectors = []
        self.value = None
    
    def write(self, vec : Vector):
        self.vectors.append(vec)
    
    def process(self):
        # THE PROCESS COMPUTE THE WEIGHTED MEAN BY THE NORMS OF THE VECTORS 
        if self.vectors == []: #This is the case where no information is stored
            self.value = None 
        else: # This is the case where a position is free and there are more vectors stored.  We do a weigthed sum of the vectors
            norms_sum = sum([v.norm() for v in self.vectors]) 
            vectors_sum = Vector(0, 0)
            for v in self.vectors:
                vectors_sum += v*v.norm()
            self.value = vectors_sum*(1/norms_sum) if norms_sum != 0 else Vector(0, 0) # If there is a food the value will be of + infinity and also if there is only ourself! 

    def read(self):
        return self.value
    
    def __str__(self):
        if self.value == None:
            return "N"
        if self.value == -float("inf"):
            return "I"
        if self.value == float("inf"):
            return "F"
        return f"{self.value}"
    
class World():

    def __init__(self, length, height, cell_energy = 10, parameters = {"energy" : 0, "minimum" : 5, "maximum" : 20, "regeneration" : 1}, initially_alive = 1, costs = COSTS, distribution = "Uniform"):
        # The density parameter tell the portion of cells that should be activate
        self.length = length
        self.height = height
        self.cell_energy = cell_energy
        self.__cells__ = [[Cell(parameters) for l in range (self.length)] for h in range (self.height)]
        self.initially_alive = initially_alive
        self.cell_side = CELL_SIDE
        self.active = 0
        self.costs = costs
        self.__information_layer__ = [[Information() for l in range (self.length)] for h in range (self.height)]
        self.__position_layer__ = [[False for l in range (self.length)] for h in range (self.height)]
        self.mean_energy = 0
        self.distribution = distribution
        self.populate()
    
    def populate(self):
        if self.distribution == "Uniform" or self.distribution == "Uniform no regen":
            # For now we just activate the right amount of cells into the totals. Then we will think about more
            to_active = self.initially_alive
            while to_active > 0:
                idx_1 = random.randrange(0, self.height)
                idx_2 = random.randrange(0, self.length)
                if self.__cells__[idx_1][idx_2].energy == 0:
                    self.__cells__[idx_1][idx_2].charge_energy(self.cell_energy)
                    to_active -= 1
            
        if self.distribution == "4 Islands" or self.distribution == "4 Islands no regen":
            # This is a 4 gaussian distribution all centered in the corrispective quadrant of the world
            to_active = self.initially_alive      
            i = 0
            while to_active > 0:
                mean_1 = self.height * 0.25 if i%2 == 0 else self.height * 0.75
                mean_2 = self.length * 0.25 if i%4 < 2 else self.length * 0.75
                i = i + 1
                var_1 = self.height * (3 / 16)
                var_2 = self.length * (3 / 16) # This variance should be the one to obtain the 100% of values in to the quadrant limits
                idx_1 = int(random.gauss(mean_1, math.sqrt(var_1)))
                idx_2 = int(random.gauss(mean_2, math.sqrt(var_2)))
                idx_1 = max(min(idx_1, self.height - 1), 0)
                idx_2 = max(min(idx_2, self.length - 1), 0)
                if self.__cells__[idx_1][idx_2].energy == 0:
                    self.__cells__[idx_1][idx_2].charge_energy(self.cell_energy)
                    to_active -= 1
        
    def compute_mean_energy(self):
        # This is the mean of the energy of the active cells
        self.mean_energy = 0
        for i in range(self.height):
            for j in range(self.length):
                if self.__cells__[i][j].energy > 0:
                    self.mean_energy += self.__cells__[i][j].energy
        self.mean_energy = 0 if self.active == 0 else self.mean_energy/self.active

    def update(self):
        self.active = 0
        for i in range(self.height):
            for j in range(self.length):
                self.__cells__[i][j].update()
                if self.__cells__[i][j].energy > 0:
                    self.active += 1
        # When one cell die, an other one come alive
        if self.distribution == "Uniform":
            to_active = self.initially_alive - self.active
            while to_active > 0:
                idx_1 = random.randrange(0, self.height)
                idx_2 = random.randrange(0, self.length)
                if self.__cells__[idx_1][idx_2].energy == 0:
                    self.__cells__[idx_1][idx_2].charge_energy(self.cell_energy)
                    to_active -= 1
        if self.distribution == "4 Islands":
            to_active = self.initially_alive - self.active
            i = random.randrange(0, 4) # if not he prioritize the first quadrant
            while to_active > 0:
                mean_1 = self.height * 0.25 if i%2 == 0 else self.height * 0.75
                mean_2 = self.length * 0.25 if i%4 < 2 else self.length * 0.75
                i = i + 1
                var_1 = self.height * (3 / 16)
                var_2 = self.length * (3 / 16) # This variance should be the one to obtain the 100% of values in to the quadrant limits
                idx_1 = int(random.gauss(mean_1, math.sqrt(var_1)))
                idx_2 = int(random.gauss(mean_2, math.sqrt(var_2)))
                idx_1 = max(min(idx_1, self.height - 1), 0)
                idx_2 = max(min(idx_2, self.length - 1), 0)
                if self.__cells__[idx_1][idx_2].energy == 0:
                    self.__cells__[idx_1][idx_2].charge_energy(self.cell_energy)
                    to_active -= 1

        # all the version no regen are the same as the original but whith no regen

        if self.active == 0:
            return - 1 # This means all that the world is dead
        self.density = self.active/(self.length*self.height)
        self.compute_mean_energy()
        self.reset_position()
        return 0
    
    def __getitem__(self, idx) -> Cell:
        if type(idx) is not list and type(idx) is not tuple:
            print("Idx while accessing a cell must be in the format [i, j] or (i, j), hence list or tuple format.")
            raise WorldException
        if len(idx) != 2:
            print(f"Idx dimension must be exactly 2. Given : {len(idx)}.")
            raise WorldException
        return self.__cells__[idx[0]][idx[1]]
    
    def alive(self):
        return self.active
    
    def asList(self):
        # Return the idxs of the cell active as a list of tuples
        idxs = []
        for i in range (self.height):
            for j in range (self.length):
                if self.__cells__[i][j].energy > 0:
                    idxs.append((i, j))
        return idxs
    
    def __str__(self):
        s = ""
        for r in self.__cells__:
            for c in r:
                s += f"{c} "
            s+="\n"
        return s

    def get_neighbourhood_clip(self, center, radius):
        # This function return the clipped values of the neighbourhood
        min_y = max(0, center[0] - radius)
        min_x = max(0, center[1] - radius)
        max_y = min(self.height, center[0] + radius + 1)
        max_x = min(self.length, center[1] + radius + 1)
        return min_y, min_x, max_y, max_x
    
    def get_neighbourhood(self, center, radius):
        # This function return the clipped neighbourhood
        min_y, min_x, max_y, max_x = self.get_neighbourhood_clip(center, radius)
        return [[c for c in r[min_x:max_x]] for r in self.__cells__[min_y : max_y]] 

    def get_neighbourhood_information(self, center, radius):
        # This function return the clipped neighbourhood information
        min_y, min_x, max_y, max_x = self.get_neighbourhood_clip(center, radius)
        return [[i for i in r[min_x:max_x]] for r in self.__information_layer__[min_y : max_y]]    

    def get_neighbourhood_position(self, center, radius):
        # This function work on the position layer
        min_y, min_x, max_y, max_x = self.get_neighbourhood_clip(center, radius)
        return [[i for i in r[min_x:max_x]] for r in self.__position_layer__[min_y : max_y]]   
    
    # This methods work on the information layer
    def get_information(self):
        return self.__information_layer__
    
    def get_position(self):
        return self.__position_layer__
    
    def write_communication(self, communication):
        # The communication is a block of vectors (or None) passed by some decisional processes
        # They must be added in the right position of the information layer
        min_y, min_x, max_y, max_x, block = communication
        for i in range (min_y, max_y): # We will check on this values (maybe add a +1 is needed)
            for j in range (min_x, max_x):
                self.__information_layer__[i][j].write(block[i-min_y][j-min_x])

    def process_information(self):
        # This is the processing work 
        for r in self.__information_layer__:
            for info in r:
                info.process()

    def print_information(self):
        for i, r in enumerate(self.__information_layer__):
            for j, inf in enumerate(r):
                print(f"{self.__information_layer__[j][i]} ", end="")
            print("")

    def write_position(self, position):
        i, j = position[0], position[1]
        self.__position_layer__[i][j] = True
    
    def reset_information(self):
        self.__information_layer__ = [[Information() for l in range (self.length)] for h in range (self.height)]
    
    def reset_position(self):
        self.__position_layer__ = [[False for l in range (self.length)] for h in range (self.height)]
    
    def __str__(self):
        s = ""
        for i, r in enumerate(self.__cells__):
            for j, cel in enumerate(r):
                s += f"{self.__cells__[j][i]} "
            s += "\n"
        return s
    
class Individual():

    def __init__(self, max_age = 100, birth_energy = 20, max_energy = 30, social_param = [1, 0, 0], position = [0, 0], radius = 4, maturity = 0.18, energy_needed = 0.6, extra_energy = 0.2, mutation_rate = 0.1, idx = 0, energy_requested = 0.5):
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
        self.maturity = maturity # For now we set as follow
        self.dead = False
        self.radius = radius # THIS IS IMPORTANT
        self.energy_needed = energy_needed  # THIS IS AN IMPORTANT PARAMETER TO TWEAK. It is the minimum quantity of energy requested (ratio) in the adult time while eating
        self.extra_energy = extra_energy  # THIS IS AN IMPORTANT PARAMETER TO TWEAK. It is the extra quantity of energy requested (ratio) in the adult time while eating
        self.mutation_rate = mutation_rate 
        self.energy_requested = energy_requested # THIS IS THE ENERGY A YOUNG INDIVIDUAL REQUEST EVERY TIME HE EAT
        self.idx = idx

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
    
    def communicate(self, pop, world : World, selfish, altruistic, normal):
        # This function is the function where the individual communicate information with the others 
        # writing on the information layers of the world
        # The process will in fact think at it 
        actual_communication = 0
        # SAMPLE PROCESS
        sample = random.uniform(0, 1)
        if sample < self.selfishness_param:
            actual_communication = selfish.communicate(self, pop, world)
        elif sample < self.altruism_param:
            actual_communication = altruistic.communicate(self, pop, world)
        else:
            actual_communication = normal.communicate(self, pop, world)

        world.write_communication(actual_communication)
        
        world.write_position(self.position) # We try to separate the vectors from the position
        
    def action(self, pop, world : World, selfish, altruistic, normal):
        # We will rework probably this a bit
        if self.dead == True: # This is not the right way to do but no matter now
            return 'Rest'
        # DECISION PROCESS
        actual_decision = "Rest"
        # SAMPLE PROCESS
        sample = random.uniform(0, 1)
        if sample < self.selfishness_param:
            actual_decision = selfish.decision(self, pop, world)
        elif sample < self.altruism_param:
            actual_decision = altruistic.decision(self, pop, world)
        else:
            actual_decision = normal.decision(self, pop, world)
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
        mutation_1 = 1 + random.uniform(-self.mutation_rate, self.mutation_rate)
        mutation_2 = 1 + random.uniform(-self.mutation_rate, self.mutation_rate)
        mutation_3 = 1 + random.uniform(-self.mutation_rate, self.mutation_rate)
        son_social_param = [self.selfishness_param * mutation_1, self.altruism_param * mutation_2, self.normality_param * mutation_3] # just multiplying
        son_social_param_sum = sum(son_social_param)
        son_social_param = [s_p/son_social_param_sum for s_p in son_social_param] # normalize
        # SON RADIUS
        son_radius = self.radius
        # SON MATURITY
        son_maturity = self.maturity
        # SON ENERGY PARAMETERS
        son_energy_needed = self.energy_needed
        son_extra_energy = self.extra_energy
        # SON MUTATION PARAM
        son_mutation_rate = self.mutation_rate
        # AGE MUTATION
        age_mutation = random.uniform(1 - self.mutation_rate, 1 + self.mutation_rate)
        son_max_age = int(age_mutation*self.max_age)
        # BIRTH POSITION
        directions = { 1 : [0, 1], 2 : [0, -1], 3 : [-1, 0], 4 : [1, 0] }
        r_dir = random.randint(1, 4)
        son_position = [self.position[0] + directions[r_dir][0] , self.position[1] + directions[r_dir][1]] # weshould check if this is valid
        # BIRTH ENERGY
        son_energy = int(self.energy*0.25)
        # SON IDX
        son_idx = self.idx
        # SON ENERGY REQUESTED
        son_energy_requested = self.energy_requested * (1 + random.uniform(-self.mutation_rate, self.mutation_rate))
        # MAX ENERGY 
        energy_mutation = random.uniform(0.9, 1.1)
        son_max_energy = self.max_energy * energy_mutation
        son = Individual(max_age=son_max_age, birth_energy=son_energy, max_energy=son_max_energy, position=son_position, social_param=son_social_param, radius=son_radius, maturity=son_maturity, energy_needed=son_energy_needed, extra_energy=son_extra_energy, mutation_rate=son_mutation_rate, idx = son_idx, energy_requested = son_energy_requested) # We should implement a lot of think here, don't worry for now
        self.energy = int(self.energy*0.75) # This parameter is to tweak
        pop.birth(son)

    def pollute(self):
        pass

    def get_color(self):
        # NORMAL BLUE, ALTRUISTIC GREEN, SELFISH RED 
        # YOUNG LIGHT, ADULT DARK
        young_color = (51, 255, 255) # The default is set for the normal
        adult_color = (51, 51, 255) # The default is set for the normal
        # SELFISH ONE
        if self.selfishness_param > self.altruism_param and self.selfishness_param > self.normality_param:
            young_color = (255, 51, 255)
            adult_color = (255, 51, 51)
        # ALTRUISTIC ONE 
        if self.altruism_param > self.selfishness_param and self.altruism_param > self.normality_param:
            young_color = (51, 255, 51)
            adult_color = (0, 204, 0)
        if self.age < self.max_age * self.maturity:
            return young_color
        return adult_color

class Population():

    def __init__(self, initial_population):
        # For now the processes stay here
        self.cell_side = CELL_SIDE
        self.__individuals__ = initial_population
        self.selfish_process = SelfishProcess()
        self.altruistic_process = AltruisticProcess()
        self.normal_process = NormalProcess()
        self.dead = 0
        self.born = 0
        self.mean_energy = 0
        self.mean_parameters = [0, 0, 0]
        self.heritage = [p.idx for p in initial_population]

    def __getitem__(self, idx):
        return self.__individuals__[idx]

    def birth(self, newOne):
        self.__individuals__.append(newOne)
    
    def death(self, individual):
        # We will try if this actually work
        self.__individuals__.remove(individual)
    
    def compute_mean_energy(self):
        # This compute the average energy of the population
        self.mean_energy = 0
        for ind in self.__individuals__:
            self.mean_energy += ind.energy
        self.mean_energy = 0 if len(self.__individuals__) == 0 else self.mean_energy/len(self.__individuals__)

    def compute_mean_parameter(self):
        self.mean_parameters = [0, 0, 0]
        for ind in self.__individuals__:
            self.mean_parameters[0] += ind.selfishness_param
            self.mean_parameters[1] += ind.altruism_param
            self.mean_parameters[2] += ind.normality_param
        for i in range (3):
            self.mean_parameters[i] = 0 if len(self.__individuals__) == 0 else self.mean_parameters[i]/len(self.__individuals__)

    def update(self, world : World):
        world.reset_information()
        self.born = 0
        for i in range (len(self.__individuals__)):
            # WE RIDEFINE AS FOLLOW : the communication can be altruistic selfish etc etc the action is "always the same"
            self.__individuals__[i].communicate(self, world, self.selfish_process, self.altruistic_process, self.normal_process)
        world.process_information()
        for i in range (len(self.__individuals__)):
            self.__individuals__[i].action(self, world, self.selfish_process, self.altruistic_process, self.normal_process)
            if self.__individuals__[i].last_action == "Reproduce":
                self.born += 1

        Dead = []
        for i in range (len(self.__individuals__)):
            ind = self.__individuals__[i].update(world.costs)
            if ind != None:
                Dead.append(ind)
        for i in range (len(Dead)):
            self.death(Dead[i])

        # compute the number of dead at each step
        self.dead = len(Dead)
        
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

        self.dead += len(Dead)

        self.compute_mean_energy()
        self.compute_mean_parameter()

        self.heritage = [p.idx for p in self.__individuals__]

        if len(self.__individuals__) == 0:
            return -1 # This means the population is all dead
        
        return 0

    def alive(self):
        return len(self.__individuals__)
        
if __name__ == "__main__":
    pass