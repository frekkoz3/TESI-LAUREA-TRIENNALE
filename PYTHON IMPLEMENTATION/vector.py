import math
class Vector():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def norm(self):
        if self.x == 0 and self.y == 0:
            return 0
        return math.sqrt(self.x*self.x + self.y*self.y)
    
    def __mul__(self, c): # This is the vector by costant multiplication
        return Vector(self.x*c, self.y*c)
    
    def __add__(self, v): # This is the vector plus vector addiction
        if v == None:
            return self
        return Vector(self.x+v.x, self.y + v.y)
    
    def __str__(self):
        return f"({format(self.x, ".2f")}, {format(self.y, ".2f")})"

if __name__ == "__main__":
    v = Vector(1.2828272, 3.28292892)
    print(v)