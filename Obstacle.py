from math import sqrt
class Obstacle(object):

    def __init__(self,pos):
        self.pos = pos
        self.radius = 10

    def distanceFrom(self,other_agent):
        return sqrt((other_agent.pos[0] - self.pos[0])**2 + (other_agent.pos[1] - self.pos[1]) **2)
