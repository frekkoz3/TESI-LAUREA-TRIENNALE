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
        """
            Here we share the information about the world we see.
            What we are actually shring it's a vector (from all the possible position we see)
            that point toward the food. In fact we share the sum of all the vectors pointing to 
            all the food we see (then we divide by the number of food we see to obtain the mean)
            Then this information wil be written on the information layer and there will be 
            added with all the others and create the actual information layer. This will be then 
            the thing we use to decide where to go. Note that, when we add the information together
            they are normalized (using a weighted sum and dividing by the sum of the weight). 
            Note: if we don't have any information to share we just share None. Our position is
            shared as an "infinite" magnitude vector (this is more a protocol). The food position
            is shared as a void vector that then will be seen as the best possible.
        """
        r = individual.radius # the radius is a parameter to tweak guys!
        pos = individual.position
        min_y, min_x, max_y, max_x = world.get_neighbourhood_clip(pos, radius = r) 
        actual_pos = [pos[0]-min_y, pos[1]-min_x] # This is the actual position in the neighbourhood
        seen = world.get_neighbourhood(pos, radius = r)
        foods = []
        for i in range (0, max_y - min_y):
            for j in range (0, max_x - min_x):
                if seen[i][j].energy > 0:
                    foods.append((i, j))           
        if foods == []: # if there is no food we just can't communicate anything
            return min_y, min_x, max_y, max_x, [pos]
        communication = [[Vector(0, 0) for j in range (0, max_x - min_x + 1)] for i in range (0, max_y - min_y + 1)]

        for i in range (0, max_y-min_y + 1):
            for j in range (0, max_x - min_x + 1):
                for f in foods:
                    communication[i][j] += Vector(f[0] - i, f[1] - j) # This is the vector pointing to the food
                communication[i][j] *= 1/(len(foods)) # We use the mean

        # We fix at the end some special position
        for f in foods:
            communication[f[0]][f[1]] = Vector(0, 0) # here there is some food
        
        communication[actual_pos[0]][actual_pos[1]] = float("inf") # here we have an individual
        
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
         we could add that the old individual who can't reproduce and just want to be chill so have a different goal (sociality for example)
        """
        maturity = 0.18 # MATURITY PARAM : WHEN DOES AN INDIVIDUAL BECOME MATURE ENOUGH TO BE AN ADULT?
        pos = individual.position
        r = individual.radius
        min_y, min_x, max_y, max_x = world.get_neighbourhood_clip(pos, r)
        seen = world.get_neighbourhood(pos, r) 
        info = world.get_neighbourhood_information(pos, r)
        actual_pos = [pos[0] - min_y, pos[1] - min_x]
        # Available action
        available_action = []
        for a in POSSIBILITIES:
            if self.action_checker.legitimacy(a, individual, world):
                available_action.append(a)

        # Search for danger :
        # and load information position
        danger_pos = []
        information_count = 0
        information_position = 0
        for i in range (0, max_y - min_y):
            for j in range (0,max_x - min_x):
                if isinstance(info[i][j], Vector): # This is done to check before if food information are actually found
                    information_count += 1
                    information_position.append([i, j])
                if info[i][j] == -float("inf"): # This means there is an individual in that location
                    # We set as danger all possible position reachable from others individual.
                    # No matter if we set as danger an impossible position, no matter how the individual
                    # Will never reach it
                    danger_pos.append([i, j-1])
                    danger_pos.append([i-1, j])
                    danger_pos.append([i, j+1])
                    danger_pos.append([i+1, j])
                    danger_pos.append([i, j])
        danger_pos = list(set(danger_pos)) 

        # Search for food :
        food = []
        for i in range (0, max_y - min_y):
            for j in range (0,max_x - min_x):
                if seen[i][j].energy > 0: # This means there is a food available
                    food.append([i, j])

        def random_movement(actual_pos, available_action, danger_pos):
            movements = ["Move_N", "Move_W", "Move_S", "Move_E"] # Choose one random among of them that lead to a safe place
            random.shuffle(movements)
            for a in movements:
                if a in available_action:
                    direction = a.split("_")[1]
                    y, x = actual_pos[0], actual_pos[1]
                    new_x = x - 1 if direction == 'W' else x 
                    new_x = new_x + 1 if direction == 'E' else new_x
                    new_y = y + 1 if direction == 'S' else y
                    new_y = new_y - 1 if direction == 'N' else new_y
                    next_position = [new_y, new_x]
                    if next_position not in danger_pos: # He don't goes where other can
                        return a
            return "Rest"

        def check_movement(actual_pos, movement, danger_pos):
            # This is done to check if a movement leads to a danger position
            direction = movement.split("_")[1]
            y, x = actual_pos[0], actual_pos[1]
            new_x = x - 1 if direction == 'W' else x 
            new_x = new_x + 1 if direction == 'E' else new_x
            new_y = y + 1 if direction == 'S' else y
            new_y = new_y - 1 if direction == 'N' else new_y
            return [new_y, new_x] not in danger_pos
        
        if individual.age < individual.max_age * maturity:
            # THE YOUNG INDIVIDUAL IS GREEDY FOR FOOD BUT IT IS CAREFUL of the other -> we need a layer where we put all of this
            # FIRST THING FIRST : if it is on food and can actually eat, he eat
            if actual_pos in food and individual.last_action.split("_")[0] != "Eat": # He can't eat if he actually have just eat
                to_eat = individual.max_energy - individual.energy
                act = f"Eat_{to_eat}"
            elif actual_pos in food and individual.last_action.split("_")[0] == "Eat" : # He must move somewhere
                # This cover 2 case : Case where he just have eaten and Case where no food information is found in the information field 
                # if he can't really move he stays there
                act = random_movement(actual_pos, available_action, danger_pos)
            elif len(food) == 0 and information_count == 0:
                act = random_movement(actual_pos, available_action, danger_pos)
            else: # Now this is the case where we wanna eat and have information about it 
                # If we have information we compute the better direction where to go (Not sure it actually works as it need)
                information_sum = vector_sum(info)
                # We find the closer direction
                direction_vector = information_sum.closer_orientation()
                if direction_vector.norm() == 0: # If we don't have a better one we go random
                    act = random_movement(actual_pos, available_action, danger_pos)
                else:
                    better_direction = translate_direction(direction_vector) # We translate the direction into a movement
                    if check_movement(actual_pos, f"Move_{better_direction}", danger_pos): # If we can we take it if not amen
                        act = f"Move_{better_direction}"
                if len(food) > 0: # We go for the food if possible (if we see something)
                    food_distance = [abs(actual_pos[0] - f[0]) + abs(actual_pos[1] - f[1]) for f in food]
                    min_idx = min(enumerate(food_distance), key=lambda x: x[1])[0]
                    food_to_eat = food[min_idx]
                    x_dist = actual_pos[1] - food_to_eat[1]
                    y_dist = actual_pos[0] - food_to_eat[0]
                    x_direction = 'W' if x_dist > 0 else 'E'
                    y_direction = 'N' if y_dist > 0 else 'S'
                    random_directions = [x_direction, y_direction]
                    random.shuffle(random_directions) # This is done to not prioritize a verse (Vertical or Horizzontal)
                    for dir in random_directions:
                        if check_movement(actual_pos, f"Move_{dir}", danger_pos):
                            act = f"Move_{dir}"
                            break            
            print(act)        
            return act
        else: # Adult time
            pass
        pass

class SelfishProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        min_y, min_x, max_y, max_x, communication = super().communicate(individual, population, world)
        communication = [[v.rotate(random.uniform(-90, 90)) if isinstance(v, Vector) else v for v in c ] for c in communication] # rotation of 90 degrees 
        return min_y, min_x, max_y, max_x, communication

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
    
    def communicate(self, individual, population, world):
        return super().communicate(individual, population, world)

    def decision(self, individual, population, world):
        return super().decision(individual, population, world)
    
class NormalProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        return super().communicate(individual, population, world)
    
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


