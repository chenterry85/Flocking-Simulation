import math
from Agent import *
from operator import add, sub

def magnitude(vel):
    return math.sqrt(vel[0]**2 + vel[1]**2)

def getUnitVector(vel, desired_v_length=1):
    if magnitude(vel) == 0:
        return 0,0
    return vel[0]/magnitude(vel) * desired_v_length ,vel[1]/magnitude(vel) * desired_v_length

def limit(vel,limit):
    if magnitude(vel) > limit:
        return getUnitVector(vel,limit)
    else:
        return vel

def v_sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]

def v_add(v1,v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def v_mul(v,k):
    return v[0]*k, v[1]*k

def v_div(v,k):
    if k:
        return v[0]/k, v[1]/k
    else:
        return v[0] / 0.001, v[1] / 0.001

def v_array_sum(array):
    sum_v = (0,0)
    for v in array:
        sum_v = v_add(sum_v,v)
    return sum_v

def change_vel_if_zero(a):
    if a.vel[0] + a.vel[1] < 0.01:
        a.vel = (1.2,1.2)

def boid_pointlist(base, height):
    return  [(base/2 , 0),
            (0, height),
            (base/2 , 3 * height/4),
            (base ,height)]

def agent_degree_rotation(agent):
    return 90 + math.degrees(math.atan2(agent.vel[1], agent.vel[0]))
