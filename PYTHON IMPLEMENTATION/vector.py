import math
import random
class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def norm(self):
        if self.x == 0 and self.y == 0:
            return 0
        return math.sqrt(self.x*self.x + self.y*self.y)
    
    def rotate(self, theta_degrees): # This is done to rotate the vector (anti clockwise)
        # We use a matrix  multiplication
        theta = math.radians(theta_degrees)
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        x_new = self.x * cos_theta - self.y * sin_theta
        y_new = self.x * sin_theta + self.y * cos_theta

        return Vector(x_new, y_new)
    
    def closer_orientation(self):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        if self.norm() == 0:
            return Vector(0, 0) # Special case
        # Normalized vector
        vx, vy = self.x/self.norm(), self.y/self.norm()
        return max(directions, key=lambda d: vx * d[0] + vy * d[1])

    def __mul__(self, c): # This is the vector by costant multiplication
        return Vector(self.x*c, self.y*c)
    
    def __add__(self, v): # This is the vector plus vector addiction
        if v == None:
            return self
        return Vector(self.x+v.x, self.y + v.y)
    
    def __str__(self):
        return f"({format(self.x, ".2f")}, {format(self.y, ".2f")})"

def vector_sum(vectors):
    s = Vector(0, 0)
    for v in vectors:
        if isinstance(v, Vector):
            s += v
    if s.norm() == 0:
        return s
    return s * (1/s.norm())

def translate_direction(dir):
    translate = {(1, 0) : "S", (0, 1) : "E", (-1, 0) : "N", (0, -1) : "W"}
    return translate[dir]

if __name__ == "__main__":
    v = Vector(1.2828272, 3.28292892)
    print(v)