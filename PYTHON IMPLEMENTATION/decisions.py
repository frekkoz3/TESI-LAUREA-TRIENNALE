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
        self.code = 'C'

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

        communication = [[Vector(0, 0) for j in range (0, max_x - min_x + 1)] for i in range (0, max_y - min_y + 1)]

        for i in range (0, max_y - min_y):
            for j in range (0, max_x - min_x):
                if seen[i][j].energy > 0:
                    foods.append((i, j))           

        if foods == []: # If there is no food we communicate to go away from us
            for i in range (0, max_y-min_y + 1):
                for j in range (0, max_x - min_x + 1):
                    v = Vector(i - actual_pos[0], j - actual_pos[1])
                    v = v*(1/v.norm()) if v.norm() != 0 else v
                    distance = 1 if (v.x == 0 and v.y == 0) else (abs(i - actual_pos[0]) + abs(j -actual_pos[1]))
                    communication[i][j] += v*(1/pow(distance, 2)) # This is the vector pointing to the food multiplied by the inverse of the distance from the food
                    #if i == actual_pos[0] and j == actual_pos[1]:
                     #   communication[i][j] = float("inf") # NOT NEEDED SINCE WE USE THE POSITION LAYER
            self.code = 'NF' # This is to remember then what to do 
            return min_y, min_x, max_y, max_x, communication # We communicate to go away from us (No Food found)

        for i in range (0, max_y-min_y + 1): # If there is food we communicate to go straigth there
            for j in range (0, max_x - min_x + 1):
                for f in foods:
                    v = Vector(f[0] - i, f[1] - j)
                    v = v*(1/v.norm()) if v.norm() != 0 else v
                    distance = 1 if (v.x == 0 and v.y == 0) else (abs(f[0] - i) + abs(f[1] - j))
                    communication[i][j] += v * (1/pow(distance, 2)) # This is the vector pointing to the food multiplied by the inverse of the distance from the food

        # We fix at the end some special position
        for f in foods:
            communication[f[0]][f[1]] = Vector(0, 0) # here there is some food
            # communication[actual_pos[0]][actual_pos[1]] = float("inf") # NOT NEEDED SINCE WE USE THE POSITION LAYER
    
        self.code = 'F'
        return min_y, min_x, max_y, max_x, communication

    def decision(self, individual, population, world):
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
        others = world.get_neighbourhood_position(pos, r)
        actual_pos = [pos[0] - min_y, pos[1] - min_x]
        # Available action
        available_action = []
        for a in POSSIBILITIES:
            if self.action_checker.legitimacy(a, individual, world):
                available_action.append(a)

        # Search for danger :
        # and load information count
        danger_pos = []
        information_count = 0
        for i in range (0, max_y - min_y):
            for j in range (0,max_x - min_x):
                if isinstance(info[i][j].value, Vector): # This is done to check before if food information are actually found
                    information_count += 1
                if others[i][j] and not (i == actual_pos[0] and j == actual_pos[1]): # This means there is an individual in that location
                    # We set as danger all possible position reachable from others individual.
                    # No matter if we set as danger an impossible position, no matter how the individual
                    # Will never reach it
                    danger_pos.append([i, j-1])
                    danger_pos.append([i-1, j])
                    danger_pos.append([i, j+1])
                    danger_pos.append([i+1, j])
                    danger_pos.append([i, j])

        # Search for food :
        food = []
        for i in range (0, max_y - min_y):
            for j in range (0,max_x - min_x):
                if seen[i][j].energy > 0: # This means there is a food available
                    food.append([i, j])

        def check_movement(actual_pos, movement, danger_pos):
            # This is done to check if a movement leads to a danger position
            direction = movement.split("_")[1]
            y, x = actual_pos[0], actual_pos[1]
            new_x = x - 1 if direction == 'W' else x 
            new_x = new_x + 1 if direction == 'E' else new_x
            new_y = y + 1 if direction == 'S' else y
            new_y = new_y - 1 if direction == 'N' else new_y
            return [new_y, new_x] not in danger_pos
        
        def random_movement(actual_pos, available_action, danger_pos):
            movements = ["Move_N", "Move_W", "Move_S", "Move_E"] # Choose one random among of them that lead to a safe place
            random.shuffle(movements)
            for a in movements:
                if a in available_action and check_movement(actual_pos, a, danger_pos):
                    return a
            return "Rest"
        
        def check_2_loop_movement(last_movement, movement): # Tells us if we are in a 2 length loop
            # This should be done with the vector lol
            movements = ["Move_N", "Move_W", "Move_S", "Move_E"]
            if not last_movement in movements or not movement in movements:
                return True # if one of the two is not a movement we are not in a loop for sure (not a 2 length)
            last_dir = last_movement.split("_")[1]
            dir = movement.split("_")[1]
            return (last_dir == 'N' and dir == 'S') or (last_dir == 'S' and dir == 'N') or (last_dir == 'E' and dir == 'W') or (last_dir == 'W' and dir == 'E')
  
        act = random_movement(actual_pos, available_action, danger_pos) # default -> this is done to prevent stall

        if individual.age < individual.max_age * maturity:
            # THE YOUNG INDIVIDUAL IS GREEDY FOR FOOD BUT IT IS CAREFUL of the other -> we need a layer where we put all of this
            # FIRST THING FIRST : if it is on food and can actually eat, he eat
            if actual_pos in food and individual.last_action.split("_")[0] != "Eat": # He can't eat if he actually have just eat
                to_eat = individual.max_energy - individual.energy
                act = f"Eat_{to_eat}"
                #individual.radius = int(world.base_radius * 1.5) # For a bit his radius will be greater
            elif actual_pos in food and individual.last_action.split("_")[0] == "Eat" : # He must move somewhere (gonna think if necessary)
                # Case where he just have eaten
                act = random_movement(actual_pos, available_action, danger_pos)
            elif len(food) == 0 and information_count == 0: # Case where no food information is found
                act = random_movement(actual_pos, available_action, danger_pos)
            elif isinstance(info[actual_pos[0]][actual_pos[1]].value, Vector):
                direction_vector = info[actual_pos[0]][actual_pos[1]].value.closer_orientation()
                if direction_vector[0] == 0 and direction_vector[1] == 0: # If we don't have a better one we go random
                    act = random_movement(actual_pos, available_action, danger_pos)
                else:
                    better_direction = translate_direction(direction_vector) # We translate the direction into a movement
                    if check_movement(actual_pos, f"Move_{better_direction}", danger_pos) and f"Move_{better_direction}" in available_action: # If we can we take it if not amen
                        act = f"Move_{better_direction}"
                    # Check if we are going into a loop of length 2
                    if check_2_loop_movement(individual.last_action, act):
                        act = random_movement(actual_pos, available_action, danger_pos)
            else: # This is the case where we know only about our position (and maybe someone else position)
            #elif len(food) == 0 and information_count > 0: # Now this is the case where we wanna eat and have information about it 
                # If we have information we compute the better direction where to go
                information_sum = vector_sum(info)
                # We find the closer direction
                direction_vector = information_sum.closer_orientation()
                if direction_vector[0] == 0 and direction_vector[1] == 0: # If we don't have a better one we go random
                    act = random_movement(actual_pos, available_action, danger_pos)
                else:
                    better_direction = translate_direction(direction_vector) # We translate the direction into a movement
                    if check_movement(actual_pos, f"Move_{better_direction}", danger_pos) and f"Move_{better_direction}" in available_action: # If we can we take it if not amen
                        act = f"Move_{better_direction}"
                    # Check if we are going into a loop of length 2
                    if check_2_loop_movement(individual.last_action, act):
                        act = random_movement(actual_pos, available_action, danger_pos)
            """"
            else: # This is the case where we see food
                food_distance = [abs(actual_pos[0] - f[0]) + abs(actual_pos[1] - f[1]) for f in food]
                min_idx = min(enumerate(food_distance), key=lambda x: x[1])[0]
                food_to_eat = food[min_idx]
                x_dist = actual_pos[1] - food_to_eat[1]
                y_dist = actual_pos[0] - food_to_eat[0]
                x_direction = 'W' if x_dist > 0 else 'E'
                y_direction = 'N' if y_dist > 0 else 'S'
                if x_dist == 0: # No movement needed on the x axis
                    x_direction = y_direction
                if y_dist == 0: # No movement needed on the y axis
                    y_direction = x_direction
                food_directions = [y_direction, x_direction]
                random.shuffle(food_directions) # This is done to not prioritize a verse (Vertical or Horizzontal)
                for dir in food_directions:
                    if check_movement(actual_pos, f"Move_{dir}", danger_pos):
                        act = f"Move_{dir}"
                        break"""
        else: # Adult time
            energy = individual.energy
            max_energy = individual.max_energy
            energy_need = 0.6 # THIS IS AN IMPORTANT PARAMETER TO TWEAK. It is the minimum quantity of energy requested (ratio) 
            if len(danger_pos) == 0 and energy >= max_energy*energy_need:
                if actual_pos in food:
                    act = random_movement(actual_pos, available_action, danger_pos=[])
                else:
                    act = "Reproduce"
            else:
                if energy < max_energy * energy_need: # In this case he's gonna search for the food. He's not scared of others
                    # WE NEED TO THINK ABOUT WHEN HE HAVE JUST REPRODUCED : he can't reproduce on the food and if he have just reproduced he can't go for food
                    # THEN WE HAVE TO THINK ABOUT THE CHILDREN : maybe we should add a relation between adult and son, that if our son is in our space we let him go for the food
                    act = random_movement(actual_pos, available_action, danger_pos)
                else: # This is the case where we are searching for peace
                    act = random_movement(actual_pos, available_action, danger_pos)
        return act 

class SelfishProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        # A selfish bro will communicate the opposite when is finding food. If it is alone he will communicate the normal.
        # Using only the field to communicate seems to lead to difficulty but we have an idea. We must modify only the
        # Minimum amount of information field necessary. It means that he will modify only the field that he does not need
        min_y, min_x, max_y, max_x, communication = super().communicate(individual, population, world)
        if self.code == 'F':
            communication = [[v.rotate(random.uniform(180, 180)) if isinstance(v, Vector) else v for v in c ] for c in communication] # rotation of 90 degrees 
        return min_y, min_x, max_y, max_x, communication

    def decision(self, individual, population, world):
        return super().decision(individual, population, world)

class AltruisticProcess(DecisionalProcess):
    
    def communicate(self, individual, population, world):
        # An altruistic bro will communicate the opposite when is not finding food. If it is finding food he will communicate the normal
        min_y, min_x, max_y, max_x, communication = super().communicate(individual, population, world)
        if self.code == 'NF':
            communication = [[v.rotate(random.uniform(180, 180)) if isinstance(v, Vector) else v for v in c ] for c in communication] # rotation of 90 degrees 
        return min_y, min_x, max_y, max_x, communication

    def decision(self, individual, population, world):
        return super().decision(individual, population, world)
    
class NormalProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        return super().communicate(individual, population, world)

    def decision(self, individual, population, world):
        return super().decision(individual, population, world)

if __name__ == "__main__":
    pass


