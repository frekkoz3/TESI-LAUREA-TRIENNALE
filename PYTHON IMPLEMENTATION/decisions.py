"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from abc import ABC
from action_handler import *
import random
import math
from vector import *

debug = False

POSSIBILITIES = ['Move_N', 'Move_W', 'Move_S', 'Move_E', 'Rest', 'Eat_1', 'Reproduce', 'Pollute']

class DecisionalProcess(ABC):

    def __init__(self):
        self.action_checker = ActionHandler()

    def communicate(self, individual, population, world):
        r = 2 # the radius is a parameter to tweak guys!
        pos = individual.position
        min_y, min_x, max_y, max_x = world.get_neighbourhood_clip(pos, radius = r) 
        seen = world.get_neighbourhood(pos, radius = r)
        foods = []
        for i in range (0, max_y - min_y):
            for j in range (0, max_x - min_x):
                if seen[i][j].energy > 0:
                    foods.append((i, j))           
        if foods == []: # if there is no food we just can't communicate anything
            return min_y, min_x, max_y, max_x, []
        communication = [[Vector(0, 0) for j in range (0, max_x - min_x)] for i in range (0, max_y - min_y)]

        for i in range (0, max_y-min_y):
            for j in range (0, max_x - min_x):
                for f in foods:
                    communication[i][j] += Vector(f[0] - i, f[1] - j) # This is the vector pointing to the food
                communication[i][j] *= 1/(len(foods)) # We use the mean

        # We fix at the end some special position
        for f in foods:
            communication[f[0]][f[1]] = Vector(0, 0) # here there is some food
        communication[pos[0]-min_y][pos[1]-min_x] = float("inf") # here we have an individual

        return min_y, min_x, max_y, max_x, communication


    def decision(self, individual, population, world):
        act = "Rest" # default
        """
         There are 5 possible action:
         1. Move (telling N, E, S, W)
         2. Rest 
         3. Eat
         4. Reproduce
         5. Pollute (To think how to implement)
         AN INDIVIDUAL CAN BE YOUNG OR ADULT. THEY HAVE TWO DIFFERENT BEHAVIOUR. 
         THE YOUNGS AIM FOR THE FOOD
         THE ADULTS (are talking) AIM FOR THE REPRODUCTION 
         we could add the old individual who can't reproduce and just want to be chill so have a different goal (peace for example)
        """
        maturity = 0.18 # MATURITY PARAM : WHEN DOES AN INDIVIDUAL BECOME MATURE ENOUGH TO BE AN ADULT? 
        if individual.age < individual.max_age * maturity:
            # THE YOUNG INDIVIDUAL IS GREEDY FOR FOOD BUT IT IS CAREFUL of the other -> we need a layer where we put all of this
            return act
        else:
            pass
        pass

class SelfishProcess(DecisionalProcess):

    def decision(self, individual, population, world):
        act = "Rest"
        # POSITION OF THE INDIVIDUAL AND FOOD POSITION
        pos = individual.position
        food = world.asList()
        if len(list(food)) == 0:
            act= 'Rest'
        # EAT IF POSSIBLE
        elif tuple(pos) in list(food) and individual.energy < individual.max_energy/2:
            to_eat = individual.max_energy - individual.energy
            act = f"Eat_{to_eat}"
        # IF OVER A FOOD STAY THERE
        elif tuple(pos) in list(food) and individual.energy >= individual.max_energy/2:
            act = "Rest"
        # SEARCH FOR THE CLOSEST FOOD
        else:
            food_distance = [abs(pos[0] - f[0]) + abs(pos[1] - f[1]) for f in food]
            min_idx = min(enumerate(food_distance), key=lambda x: x[1])[0]
            food_to_eat = food[min_idx]
            x_dist = pos[1] - food_to_eat[1]
            y_dist = pos[0] - food_to_eat[0]
            x_direction = 'W' if x_dist > 0 else 'E'
            y_direction = 'N' if y_dist > 0 else 'S'
            direction = x_direction if x_dist != 0 else y_direction
            act = f"Move_{direction}"
        if debug:
            print(f"{individual.position} - {individual.energy} : {act}")
        return act

class AltruisticProcess(DecisionalProcess):

    def decision(self, individual, population, world):
        # We have to develop a simple rule model to implement a "altruistic decision process"
        possible_action = []
        for a in POSSIBILITIES:
            if self.action_checker.legitimacy(a, individual, world):
                possible_action.append(a)
        action = random.choice(possible_action)
        return action
    
class NormalProcess(DecisionalProcess):

    def decision(self, individual, population, world):
        # We have to develop a simple rule model to implement a "altruistic decision process"
        possible_action = []
        for a in POSSIBILITIES:
            if self.action_checker.legitimacy(a, individual, world):
                possible_action.append(a)
        action = random.choice(possible_action)
        return action

if __name__ == "__main__":
    pass


