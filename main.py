import math
import utils
from utils import v_sub, v_add, v_mul, v_div, v_array_sum, agent_degree_rotation
import sys
import pygame as pyg
from operator import neg
from Agent import *
from Obstacle import *
from random import randrange

#init variables
agent_array = []
obstacle_array = []
speed_adjustment = 0

#CONSTANTS
# Blue:0 Red:1
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

def computeAlignment(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < ALIGNMENT_RADIUS and t == i%2:
            compute_vel = v_add(compute_vel,agent.vel)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return utils.limit(compute_vel,0.05)

def computeCohesion(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < COHESION_RADIUS and t == i%2:
            compute_vel = v_sub(agent.pos,myAgent.pos)
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    compute_vel = v_div(compute_vel,neighbors_cnt)

    return utils.limit(compute_vel, 0.05)

def computeSeperation(myAgent,t):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for i in range(len(agent_array)):
        agent = agent_array[i]
        if agent != myAgent and myAgent.distanceFrom(agent) < SEPERATION_RADIUS and t == i%2:
            temp_vel = v_sub(myAgent.pos,agent.pos)
            temp_vel = utils.getUnitVector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distanceFrom(agent)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def computeObscatleDodge(myAgent):
    compute_vel = (0,0)
    neighbors_cnt = 0

    for obs in obstacle_array:
        if obs.distanceFrom(myAgent) < OBSTACLE_DOGDGE_RADIUS:
            temp_vel = v_sub(myAgent.pos,obs.pos)
            temp_vel = utils.getUnitVector(temp_vel)
            compute_vel = v_add(compute_vel, v_div(temp_vel,myAgent.distanceFrom(obs)))
            neighbors_cnt+=1

    if neighbors_cnt == 0:
        return compute_vel

    return v_div(compute_vel,neighbors_cnt)

def check_agent_inbound():
    for agent in agent_array:
        if agent.pos[0] > WIDTH:
            agent.pos = (0,agent.pos[1])
        if agent.pos[0] < 0:
            agent.pos = (WIDTH,agent.pos[1])
        if agent.pos[1] > HEIGHT:
            agent.pos = (agent.pos[0],0)
        if agent.pos[1] < 0:
            agent.pos = (agent.pos[0],HEIGHT)

def agent_update():
    global agent_array
    temp_agent_array = []

    for i in range(len(agent_array)):
        agent = agent_array[i]
        temp_vel = (0,0)
        cohesion_v = computeCohesion(agent,i%2)
        alignment_v = computeAlignment(agent,i%2)
        seperation_v = computeSeperation(agent,i%2)
        obstacle_dodge_v = computeObscatleDodge(agent)

        v_array = [agent.vel,
                   utils.v_mul(cohesion_v,COHESION_WEIGHT[i%2]),
                   utils.v_mul(alignment_v,ALIGNMENT_WEIGHT[i%2]),
                   utils.v_mul(seperation_v,SEPERATION_WEIGHT[i%2]),
                   utils.v_mul(obstacle_dodge_v, OBSTACLE_DOGDGE_WEIGHT)
                   ]


        temp_vel = utils.v_array_sum(v_array)
        temp_vel = utils.v_mul(temp_vel,FPS)

        a = Agent(agent.pos, temp_vel)
        if i%2:
            a.vel = utils.limit(temp_vel, DEFAULT_SPEED + 6 + speed_adjustment)
        else:
            a.vel = utils.limit(temp_vel, DEFAULT_SPEED + speed_adjustment)
        # utils.change_vel_if_zero(a)
        a.updatePos()
        temp_agent_array.append(a)

    agent_array = temp_agent_array

def randomize_position():
    for agent in agent_array:
        agent.pos = randrange(0,WIDTH,1), randrange(0,HEIGHT,1)

def clear_all_item():
    global agent_array, obstacle_array
    agent_array = []
    obstacle_array = []

def adjust_speed(type):
    global speed_adjustment
    if type:
        speed_adjustment += 1
    else:
        speed_adjustment -= 1

    if speed_adjustment > MAX_SPEED:
        speed_adjustment = MAX_SPEED
    elif speed_adjustment < MIN_SPEED:
        speed_adjustment = MIN_SPEED


#pygame variables
WIDTH = 1500
HEIGHT = 800
TITLE = "FLOCKING"
FPS = 60
BACKGROUND = (0,0,0)
AGENT_COLOR = [(116,175,173),(222,27,26)]
OBSTACLE_COLOR = (250,250,250)
TEXT_COLOR = (255,255,255)
TRI_BASE = [12,10,]
TRI_HEIGHT = [18,15]
MAX_AGENT_COUNT = 60

pyg.init()
clock = pyg.time.Clock()

screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption(TITLE)

def make_agent_inbound():
    for agent in agent_array:
        agent.pos = agent.pos[0] % WIDTH, agent.pos[1] % HEIGHT

def draw_text():
    font = pyg.font.SysFont("consolas",16)
    text_array = [
                  font.render("Clock FPS: {}".format(int(clock.get_fps())),20,TEXT_COLOR),
                  font.render("Clock Ticks: {}".format(pyg.time.get_ticks()),10,TEXT_COLOR),
                  font.render("Agent Count: {}".format(len(agent_array)),20,TEXT_COLOR),
                  font.render("Obstacle Count: {}".format(len(obstacle_array)),20,TEXT_COLOR),
                  font.render("Red Agent Speed: {}".format(DEFAULT_SPEED + speed_adjustment + 6),20,TEXT_COLOR),
                  font.render("Blue Agent Speed: {}".format(DEFAULT_SPEED + speed_adjustment),20,TEXT_COLOR)
                 ]

    #display "Agents Reached Max" when agent count reaches max
    if MAX_AGENT_COUNT == len(agent_array):
        text_array[2] = font.render("Agent Count: {} (Agents Reached Max)".format(len(agent_array)),20,TEXT_COLOR)

    for i in range(len(text_array)):
        text = text_array[i]
        screen.blit(text,(2,3 + i*15))

def draw_agent():
    agent_array_size = len(agent_array)

    for i in range(agent_array_size):
        agent = agent_array[i]
        make_agent_inbound()
        pointlist = utils.boid_pointlist(TRI_BASE[i%2],TRI_HEIGHT[i%2])
        surface = pyg.Surface((TRI_BASE[i%2], TRI_HEIGHT[i%2]), pyg.SRCALPHA).convert_alpha()
        pyg.draw.polygon(surface,AGENT_COLOR[i%2],pointlist, 0)
        rotate = pyg.transform.rotate(surface,-agent_degree_rotation(agent))
        center = v_sub(agent.pos,(TRI_BASE[i%2] / 2, TRI_HEIGHT[i%2] / 2))
        screen.blit(rotate, center)

def draw_obstacle():
    for obs in obstacle_array:
        #pyg.draw.circle(screen,OBSTACLE_COLOR,obs.pos,obs.radius,0)
        pyg.draw.rect(screen, OBSTACLE_COLOR, (obs.pos[0], obs.pos[1], obs.radius, obs.radius), 0)

def run():

    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif pyg.key.get_pressed()[pyg.K_c]:
                clear_all_item()
            elif pyg.key.get_pressed()[pyg.K_r]:
                randomize_position()
            elif pyg.key.get_pressed()[pyg.K_UP]:
                adjust_speed(1)
            elif pyg.key.get_pressed()[pyg.K_DOWN]:
                adjust_speed(0)
            elif pyg.mouse.get_pressed()[0] and MAX_AGENT_COUNT > len(agent_array):
                # append new agent
                agent_array.append(Agent(pyg.mouse.get_pos()))
            elif pyg.mouse.get_pressed()[2]:
                # append new obstacle
                obstacle_array.append(Obstacle(pyg.mouse.get_pos()))

        screen.fill(BACKGROUND)
        draw_agent()
        draw_obstacle()
        draw_text()
        agent_update()
        pyg.display.update()
        clock.tick(FPS)

run()
