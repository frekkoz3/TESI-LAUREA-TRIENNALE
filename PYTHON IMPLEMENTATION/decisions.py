from abc import ABC, abstractmethod
from action_handler import *
from common import *
import random
import math

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
        # We have to develop a simple rule model to implement a "selfish decision process"
        action = random.choice(list(POSSIBILITIES.keys()))
        while not self.action_checker.legitimacy(action, individual, population, world):
            action = random.choice(list(POSSIBILITIES.keys()))
        # POSITION OF THE INDIVIDUAL AND FOOD POSITION
        pos = individual.position
        food = world.asList()
        # EAT IF POSSIBLE
        if tuple(pos) in list(food) and individual.energy < individual.max_energy/2:
            to_eat = individual.max_energy - individual.energy
            return f"Eat_{to_eat}"
        # IF OVER A FOOD STAY THERE
        elif tuple(pos) in food and individual.energy >= individual.max_energy/2:
            return "Rest"
        # SEARCH FOR THE CLOSEST FOOD
        else:
            food_distance = [abs(pos[0] - w[0]) + abs(pos[1] - w[1]) for w in food]
            min_idx = min(enumerate(food_distance), key=lambda x: x[1])[0]
            food_to_eat = food[min_idx]
            print(f"{food_to_eat} at distance {food_distance[min_idx]}")
            x_dist = pos[1] - food_to_eat[1]
            y_dist = pos[0] - food_to_eat[0]
            x_direction = 'W' if x_dist > 0 else 'E'
            y_direction = 'N' if y_dist > 0 else 'S'
            direction = x_direction if x_dist != 0 else y_direction
            return f"Move_{direction}"

class AltruisticProcess(DecisionalProcess):

    def decision(self, individual, population, world):
        # We have to develop a simple rule model to implement a "altruistic decision process"
        action = random.choice(list(POSSIBILITIES.keys()))
        while not self.action_checker.legitimacy(action, individual, population, world):
            action = random.choice(list(POSSIBILITIES.keys()))
        return action
    
class NormalProcess(DecisionalProcess):

    def decision(self, individual, population, world):
        # We have to develop a simple rule model to implement a "normal decision process"
        action = random.choice(list(POSSIBILITIES.keys()))
        while not self.action_checker.legitimacy(action, individual, population, world):
            action = random.choice(list(POSSIBILITIES.keys()))
        return action

if __name__ == "__main__":
    pass


