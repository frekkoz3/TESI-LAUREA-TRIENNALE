"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
from abc import ABC, abstractmethod
from action_handler import *
import random

debug = False

POSSIBILITIES = ['Move_N', 'Move_W', 'Move_S', 'Move_E', 'Rest', 'Eat_1', 'Reproduce', 'Pollute']

class DecisionalProcess(ABC):

    def __init__(self):
        self.action_checker = ActionHandler()

    @abstractmethod
    def decision(self, individual, population, world):
        # There are 5 possible action:
        # 1. Move (telling N, E, S, W)
        # 2. Rest 
        # 3. Eat
        # 4. Reproduce
        # 5. Pollute (To think how to implement)
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


