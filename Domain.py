

from utils import v_sub, v_add, v_mul, v_div, v_array_sum, agent_degree_rotation, convert_to_unit_vector, limit
from Agent import DEFAULT_SPEED, Agent
from Obstacle import Obstacle
from random import randrange
import shared


# Blue Agent:0
# Red Agent:1
ALIGNMENT_WEIGHT = [10,4]
COHESION_WEIGHT = [5,3]
SEPERATION_WEIGHT = [5,8]
OBSTACLE_DOGDGE_WEIGHT = 180

ALIGNMENT_RADIUS = 200
COHESION_RADIUS = 170
SEPERATION_RADIUS = 30
OBSTACLE_DOGDGE_RADIUS = 70

MAX_SPEED = 25
MIN_SPEED = 1

def compute_alignment(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(shared.agent_array)):
        agent = shared.agent_array[i]
        if agent != myAgent and myAgent.distance_from(agent) < ALIGNMENT_RADIUS and t == i%2:
            compute_vel = v_add(compute_vel,agent.vel)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return limit(compute_vel,0.05)

def compute_cohesion(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(shared.agent_array)):
        agent = shared.agent_array[i]
        if agent != myAgent and myAgent.distance_from(agent) < COHESION_RADIUS and t == i%2:
            compute_vel = v_sub(agent.pos,myAgent.pos)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return limit(compute_vel, 0.05)

def compute_seperation(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(shared.agent_array)):
        agent = shared.agent_array[i]
        if agent != myAgent and myAgent.distance_from(agent) < SEPERATION_RADIUS and t == i%2:
            temp_vel = v_sub(myAgent.pos,agent.pos)
            temp_vel = convert_to_unit_vector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distance_from(agent)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def compute_obstacle_dodge(myAgent):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for obs in shared.obstacle_array:
        if obs.distance_from(myAgent) < OBSTACLE_DOGDGE_RADIUS:
            temp_vel = v_sub(myAgent.pos,obs.pos)
            temp_vel = convert_to_unit_vector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distance_from(obs)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def check_agent_inbound():
    for agent in shared.agent_array:
        if agent.pos[0] > shared.WIDTH:
            agent.pos = (0,agent.pos[1])
        if agent.pos[0] < 0:
            agent.pos = (shared.WIDTH,agent.pos[1])
        if agent.pos[1] > shared.HEIGHT:
            agent.pos = (agent.pos[0],0)
        if agent.pos[1] < 0:
            agent.pos = (agent.pos[0],shared.HEIGHT)

def agent_update():

    temp_agent_array = []

    for i in range(len(shared.agent_array)):
        agent = shared.agent_array[i]
        temp_vel = (0,0)
        cohesion_v = compute_cohesion(agent,i%2)
        alignment_v = compute_alignment(agent,i%2)
        seperation_v = compute_seperation(agent,i%2)
        obstacle_dodge_v = compute_obstacle_dodge(agent)

        v_array = [agent.vel,
                   v_mul(cohesion_v,COHESION_WEIGHT[i%2]),
                   v_mul(alignment_v,ALIGNMENT_WEIGHT[i%2]),
                   v_mul(seperation_v,SEPERATION_WEIGHT[i%2]),
                   v_mul(obstacle_dodge_v, OBSTACLE_DOGDGE_WEIGHT)
                   ]


        temp_vel = v_array_sum(v_array)
        temp_vel = v_mul(temp_vel,shared.FPS)

        a = Agent(agent.pos, temp_vel)
        if i%2:
            a.vel = limit(temp_vel, DEFAULT_SPEED + 6 + shared.speed_adjustment)
        else:
            a.vel = limit(temp_vel, DEFAULT_SPEED + shared.speed_adjustment)
        # change_vel_if_zero(a)
        a.update_pos()
        temp_agent_array.append(a)

    shared.agent_array = temp_agent_array

def randomize_position():
    for agent in shared.agent_array:
        agent.pos = randrange(0,shared.WIDTH,1), randrange(0,shared.HEIGHT,1)

def clear_all_item():
    shared.agent_array = []
    shared.obstacle_array = []

def adjust_speed(type):
    if type:
        shared.speed_adjustment += 1
    else:
        shared.speed_adjustment -= 1

    if shared.speed_adjustment > MAX_SPEED:
        shared.speed_adjustment = MAX_SPEED
    elif shared.speed_adjustment < MIN_SPEED:
        shared.speed_adjustment = MIN_SPEED
