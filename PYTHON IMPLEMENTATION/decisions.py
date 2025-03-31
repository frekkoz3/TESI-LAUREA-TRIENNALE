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

POSSIBILITIES = ['Move_N', 'Move_W', 'Move_S', 'Move_E', 'Rest', 'Eat_1', 'Reproduce']

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
                    distance = 1 if (v.x == 0 and v.y == 0) else (abs(i - actual_pos[0]) + abs(j -actual_pos[1])) # Manhattan Distance
                    communication[i][j] += v*(1/pow(distance, 2)) # This is the vector pointing away from us multiplied by the inverse of the distance from us
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
        for i in range (0, max_y-min_y + 1): # DANGER POSITION WRITTEN IN THE INFORMATION LAYER
            for j in range (0, max_x - min_x + 1):
                if (i, j) in [(actual_pos[0] - 1, actual_pos[1]), (actual_pos[0] + 1, actual_pos[1]), (actual_pos[0], actual_pos[1] - 1), (actual_pos[0], actual_pos[1] + 1)]:
                    v = Vector(i - actual_pos[0], j - actual_pos[1])
                    communication[i][j] = v*((2*individual.radius -1)*(2*individual.radius -1)) # This is the vector pointing away from us with the norm equal to the maximum of point into the neighborhood
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
        maturity = individual.maturity # MATURITY PARAM : WHEN DOES AN INDIVIDUAL BECOME MATURE ENOUGH TO BE AN ADULT?
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

        # Search for food :
        food = []
        for i in range (0, max_y - min_y):
            for j in range (0,max_x - min_x):
                if seen[i][j].energy > 0: # This means there is a food available
                    food.append([i, j])

        def random_movement(available_action):
            movements = ["Move_N", "Move_W", "Move_S", "Move_E", "Rest"] # Choose one random among of them that lead to a safe place
            random.shuffle(movements)
            for a in movements:
                if a in available_action:
                    return a
            return "Rest"
        
        def basic_logic(available_action, direction_vector, act, rotate = False):
            if direction_vector == (0, 0):
                act = random_movement(available_action)
            else:
                if rotate:
                    direction_vector = direction_vector.rotate(180).closer_orientation() # does to prevent numerical error
                better_direction = translate_direction(direction_vector)
                if f"Move_{better_direction}" in available_action: # If we can we take it if not amen
                    act = f"Move_{better_direction}"
            return act

        act = random_movement(available_action) # default
        # to see what happens if we assing rest action at the (0, 0)

        direction_vector = info[actual_pos[0]][actual_pos[1]].value.closer_orientation()

        if individual.age < maturity:
            # THE YOUNG INDIVIDUAL IS GREEDY FOR FOOD BUT IT IS CAREFUL of the other -> we need a layer where we put all of this
            # FIRST THING FIRST : if it is on food and can actually eat, he eat
            if "Eat_1" in available_action: # Now he can eat
                to_eat = (individual.max_energy - individual.energy) * individual.energy_requested # He asks for a portion of what he need to fullfill
                act = f"Eat_{to_eat}"
            else: # If there is food we follow the information field
                act = basic_logic(available_action, direction_vector, act)

        else: # Adult time
            energy = individual.energy
            max_energy = individual.max_energy
            energy_need = individual.energy_needed # THIS IS AN IMPORTANT PARAMETER TO TWEAK. It is the minimum quantity of energy requested (ratio) 
            extra_energy = individual.extra_energy # THIS PARAMETERS TELLS US HOW MUCH EXTRA ENERGY WE TAKE for searching peace
            if "Reproduce" in available_action:
                    act = "Reproduce"
            elif energy < max_energy * energy_need: # If we need to eat we gonna find it
                if "Eat_1" in available_action:
                    to_eat = max_energy * (energy_need + extra_energy) - energy 
                    act = f"Eat_{to_eat}"
                else:
                    act = basic_logic(available_action, direction_vector, act)
            else: # If we need space we are gonna seek it
                act = basic_logic(available_action, direction_vector, act, rotate=True)

        # TO BREAK THE LOOP WE INSERT THIS LITTLE PROBABILITY OF RANDOM MOVEMENT (1%)
        if act.split("_")[0] == "Move":
            if random.uniform(0, 1) < 0.01:
                act = random_movement(available_action)

        return act 

class SelfishProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        # A selfish individual will communicate the opposite when is finding food. If it is alone he will communicate the normal.
        # Using only the field to communicate seems to lead to difficulty but we have an idea. We must modify only the
        # Minimum amount of information field necessary. It means that he will modify only the field that he does not need
        min_y, min_x, max_y, max_x, communication = super().communicate(individual, population, world)

        if self.code == 'F':

            communication = [[v.rotate(180) if isinstance(v, Vector) else v for v in c ] for c in communication] # rotation of 180 degrees 
            
            # Now we set to normal the one needed to go to the food
            pos = individual.position
            r = individual.radius
            rotated = [[False for j in range (0, max_x - min_x + 1)] for i in range (0, max_y - min_y + 1)] # We ned this to track what we already rotate back to normal
            actual_pos = [pos[0] - min_y, pos[1] - min_x]
            seen = world.get_neighbourhood(pos, r) 
            for i in range (0, max_y - min_y):
                for j in range (0,max_x - min_x):
                    if seen[i][j].energy > 0: # We find so the position of the food
                        # We define the corners of the rectangle containing food and individual at the two opposite corners
                        min_i = min(actual_pos[0], i)
                        min_j = min(actual_pos[1], j)
                        max_i = max(actual_pos[0], i)
                        max_j = max(actual_pos[1], j)
                        # We reset to normal the value (only once)
                        for y in range(min_i, max_i + 1):
                            for z in range(min_j, max_j + 1):
                                if not rotated[y][z]:
                                    communication[y][z] = communication[y][z].rotate(180) if isinstance(communication[y][z], Vector) else communication[y][z]
                                    rotated[y][z] = True

        return min_y, min_x, max_y, max_x, communication

    def decision(self, individual, population, world):
        dec = super().decision(individual, population, world)
        pos = individual.position
        r = individual.radius
        # Compute how many there are
        others = world.get_neighbourhood_position(pos, r)
        others_count = 0
        for r in others:
            for o in r:
                if o:
                    others_count += 1

        # A selfish individual will eat more of what he need when see others in the zone
        if dec.split("_")[0] == "Eat" and others_count > 1:  
            unit = float(dec.split("_")[1])
            unit *= 1.5
            dec = f"Eat_{unit}"

        return dec

class AltruisticProcess(DecisionalProcess):
    
    def communicate(self, individual, population, world):
        # An altruistic bro will communicate his position when is not finding food. If it is finding food he will communicate the food position
        min_y, min_x, max_y, max_x, communication = super().communicate(individual, population, world)
        if self.code == 'NF':
            communication = [[v.rotate(random.uniform(180, 180)) if isinstance(v, Vector) else v for v in c ] for c in communication] # rotation of 90 degrees 
        return min_y, min_x, max_y, max_x, communication

    def decision(self, individual, population, world):
        dec = super().decision(individual, population, world)
        pos = individual.position
        r = individual.radius
        # Compute how many there are
        others = world.get_neighbourhood_position(pos, r)
        others_count = 0
        for r in others:
            for o in r:
                if o:
                    others_count += 1

        # An altruistic individual will eat less of what he need when see others in the zone
        if dec.split("_")[0] == "Eat" and others_count > 1:  
            unit = float(dec.split("_")[1])
            unit *= 0.75
            dec = f"Eat_{unit}"

        return dec
    
class NormalProcess(DecisionalProcess):

    def communicate(self, individual, population, world):
        return super().communicate(individual, population, world)

    def decision(self, individual, population, world):
        return super().decision(individual, population, world)

if __name__ == "__main__":
    pass


