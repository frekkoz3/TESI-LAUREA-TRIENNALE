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
            new_x = x + 1 if split_actions[1] == 'W' else x 
            new_x = new_x - 1 if split_actions[1] == 'E' else new_x
            new_y = y + 1 if split_actions[1] == 'S' else y
            new_y = new_y - 1 if split_actions[1] == 'N' else new_y
            return new_y > 0 and new_y < y_lim and new_x > 0 and new_x < x_lim # we just check if the space is possible, not if the space is occuped. 
        if split_actions[0] == 'Rest':
            return True # Someone can always rest for now
        if split_actions[0] == 'Reproduce':
            return individual.age > individual.maturity and individual.age < individual.senility # We just check if an individual is in the right age 
        if split_actions[0] == 'Eat':
            return tuple(individual.position) in world.asList() # We check if we are on an energy cell
        if split_actions[0] == 'Pollute':
            return True # To implement the pollute mechanic
                
        return False # Default (why not?)

if __name__ == "__main__":
    pass
