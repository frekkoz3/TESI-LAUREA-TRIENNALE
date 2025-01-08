from abc import ABC, abstractmethod
import random

POSSIBILITIES = {'Move_N' : 1, 'Move_W' : 1, 'Move_S' : 1, 'Move_E' : 1, 'Rest' : 0.1, 'Eat_1' : 0.1, 'Reproduce' : 5, 'Pollute' : 0.2}

class DecisionalProcess(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def decision(self, individual = None, population = None, world = None):
        # There are 5 possible action:
        # 1. Move (telling N, E, S, W)
        # 2. Rest 
        # 3. Eat
        # 4. Reproduce
        # 5. Pollute
        pass

class SelfishProcess(DecisionalProcess):

    def decision(self, individual = None, population = None, world = None):
        # We have to develop a simple rule model to implement a "selfish decision process"
        return random.choice(list(POSSIBILITIES.keys()))

class AltruisticProcess(DecisionalProcess):

    def decision(self, individual = None, population = None, world = None):
        # We have to develop a simple rule model to implement a "altruistic decision process"
        return random.choice(list(POSSIBILITIES.keys()))
    
class NormalProcess(DecisionalProcess):

    def decision(self, individual = None, population = None, world = None):
        # We have to develop a simple rule model to implement a "normal decision process"
        return random.choice(list(POSSIBILITIES.keys()))

if __name__ == "__main__":
    print(POSSIBILITIES.keys())
    np = NormalProcess()
    print(np.decision())


