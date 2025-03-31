"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""

class ActionHandler():

    def __init__(self):
        self.status = "ON"

    def legitimacy(self, action, individual, world):
        x_lim = world.length
        y_lim = world.height
        x = individual.position[1]
        y = individual.position[0]
        split_actions = action.split("_")
        if split_actions[0] == 'Move':
            new_x = x - 1 if split_actions[1] == 'W' else x 
            new_x = new_x + 1 if split_actions[1] == 'E' else new_x
            new_y = y + 1 if split_actions[1] == 'S' else y
            new_y = new_y - 1 if split_actions[1] == 'N' else new_y
            return not( new_y < 0 or new_y > y_lim - 1 or new_x < 0 or new_x > x_lim - 1 )# we just check if the space is possible, not if the space is occupied. 
        if split_actions[0] == 'Rest':
            return True # Someone can always rest for now
        if split_actions[0] == 'Reproduce': 
            maturity_flag = individual.age > individual.maturity
            space_flag = self.legitimacy("Move_W", individual, world) and self.legitimacy("Move_N", individual, world) and self.legitimacy("Move_S", individual, world) and self.legitimacy("Move_E", individual, world) # We check if an individual has a free neighbourhood
            energy_flag = individual.energy >= individual.max_energy*individual.energy_needed # Having enough food
            food_flag = not tuple(individual.position) in world.asList() # Not on food
            pace_flag = world.get_information()[y][x].value.norm() < 0.1 # Enough distance from others -> it can be achieved by measuring the magnitude of the information vector
            return maturity_flag and space_flag and energy_flag and food_flag and pace_flag  # We check that an individual is mature, is not in on a border and has free space, has enough energy and is not on a food
        if split_actions[0] == 'Eat':
            food_flag = tuple(individual.position) in world.asList() # We check if we are on an energy cell
            not_just_eaten_flag = individual.last_action.split("_")[0] != "Eat" # We check that it hasn't just eat
            return food_flag and not_just_eaten_flag
                
        return False # Default (why not?)

if __name__ == "__main__":
    pass
