#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:58:55 2020

@author: aravind
"""

from annealing_rect import ObjectClass
from annealing_rect import Object,get_overall_cost
import matplotlib as mpl
#theta,x,y,z,oid,classid,M,is_fixed,radius,dw = 5,aw = 10)

bed1 = Object(0,10,10,2,4,2,20,False,4,3)
bed2 = Object(0,10,10,12,5,2,20,False,4,2)
chair1 = Object(0,10,10,14,1,1,20,False,6,5)
chair2 = Object(0,10,10,4,2,1,20,False,2,4)
chair3 = Object(0,10,10,2,3,1,20,False,2,6)
table1 = Object(0,10,10,2,3,3,20,False,5,6)
table2 = Object(0,10,10,2,3,3,20,False,3,5)


all_obj = [bed1,bed2,chair1,chair2,chair3,table1,table2]

print(get_overall_cost(all_obj,2))

print(bed1.get_distance(bed2))
import numpy.random as rn
import copy
import math
import matplotlib.pyplot as plt  # to plot
import matplotlib.patches as patches
import random

import numpy as np

intervaltheta = (0,180)
interval = (0,20)
def f(all_obj_new):
    """ Function to minimize."""
    return get_overall_cost(all_obj_new,2)

def clip(a,b,x):
    """ Force x to be in the interval."""
    bb = 0.5*math.sqrt(a**2+b**2)
    low, high = (bb,20-bb)
    return max(min(x, high), low)
def cliptheta(x):
    """ Force x to be in the interval."""
    a, b = intervaltheta
    return max(min(x, b), a)

def cost_function(x):
    """ Cost of x = f(x)."""
    return f(x)
def random_neighbour(state,T, fraction=1):
    """Move a little bit x, from the left or the right."""
    new_states = copy.copy(state)
    d = dict(enumerate(state))
    keys = random.sample(list(d), 3)
    for i in keys:
        amplitude= (max(interval) - min(interval)) * T/2
        amplitudetheta = (max(intervaltheta) - min(intervaltheta)) * T/2
        delta_x = (-amplitude/2.) + amplitude * rn.random_sample()
        delta_y = (-amplitude/2.) + amplitude * rn.random_sample()
        deltatheta = (-amplitudetheta/2.) + amplitudetheta * rn.random_sample()
        new_state = copy.copy(state[i])
        new_state.x = clip(state[i].a,state[i].b,state[i].x + delta_x)
        new_state.y = clip(state[i].a,state[i].b,state[i].y + delta_y)
        new_state.theta = cliptheta(state[i].theta + deltatheta)
        new_states[i] = new_state
        
    return new_states
        
    
def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        # print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temperature)
        # print("    - Acceptance probabilty = {:.3g}...".format(p))
        return p
def temperature(fraction):
    """ Example of temperature dicreasing as the process goes on."""
    return max(0.01, min(1, 1 - fraction))


def display_state(state):
    fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
    ax = plt.gca()
    ax.cla()
    ax.set_xlim((-5, 25))
    ax.set_ylim((-5, 25))
    border = patches.Rectangle((0,0), 20, 20, fc='white', ec='red', linewidth=1)
    ax.add_patch(border)
    for s in state:
        print(s.x,s.y)
        if s.classid == 1:
            rect = patches.Rectangle((s.x-s.a/2.,s.y-s.b/2.), s.a, s.b, fc='blue', ec='black', linewidth=1)
            t2 = mpl.transforms.Affine2D().rotate_deg_around(s.x,s.y,s.theta) + ax.transData
            rect.set_transform(t2)
        elif s.classid == 2:
            rect = plt.Rectangle((s.x-s.a/2.,s.y-s.b/2.), s.a, s.b, fc='red', ec='black',linewidth=1)
            t2 = mpl.transforms.Affine2D().rotate_deg_around(s.x,s.y,s.theta) + ax.transData
            rect.set_transform(t2)
        else:
            rect = plt.Rectangle((s.x-s.a/2.,s.y-s.b/2.), s.a, s.b, fc='green', ec='black',linewidth=1)
            t2 = mpl.transforms.Affine2D().rotate_deg_around(s.x,s.y,s.theta) + ax.transData
            rect.set_transform(t2)
        ax.add_patch(rect)
    #plt.axis('equal')
    plt.show()
   
def annealing(all_obj,
              random_neighbour,
              acceptance,
              temperature,
              maxsteps=100,
              debug=True):
    """ Optimize the black-box function 'cost_function' with the simulated annealing algorithm."""
    state = all_obj
    
    cost = get_overall_cost(all_obj,2)
    states, costs = [state], [cost]
    for step in range(maxsteps):
        fraction = step / float(maxsteps)
        T = temperature(fraction)
        new_state = random_neighbour(state, T,fraction)
        new_cost = get_overall_cost(new_state,2)
        if debug: print("Step #{:>2}/{:>2} : T = {:>4.3g}, state = {:>4.3g}, cost = {:>4.3g}, new_state = {:>4.3g}, new_cost = {:>4.3g} ...".format(step, maxsteps, T, state, cost, new_state, new_cost))
        if acceptance_probability(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
            #display_state(state)    
            # print("  ==> Accept it!")
        # else:
        #    print("  ==> Reject it...")
    return state, cost_function(state), states, costs


state,cost,states,costs = annealing(all_obj, random_neighbour, acceptance_probability, temperature, maxsteps=5000, debug=False)
print("Initial State:")
for i in range(len(all_obj)):
    print("x = {:>4.3g},y = {:>4.3g},z = {:>4.3g},theta = {:>4.3g}".format(all_obj[i].x,all_obj[i].y,all_obj[i].z,all_obj[i].theta))
print("Initial Cost = {:>4.3g}".format(get_overall_cost(all_obj,2)))
print("Final State:")
for i in range(len(state)):
    print("x = {:>4.3g},y = {:>4.3g},z = {:>4.3g},theta = {:>4.3g}".format(state[i].x,state[i].y,state[i].z,state[i].theta))
print("Final Cost = {:>4.3g}".format(cost))

all_x = []
all_x1 = []
all_x2 = []
all_y = []
all_y1 = []
all_y2 = []

all_theta = []

for i in range(len(states)):
    all_x.append(states[i][0].x)
    all_x1.append(states[i][1].x)
    all_x2.append(states[i][2].x)
    all_y.append(states[i][0].y)
    all_y1.append(states[i][1].y)
    all_y2.append(states[i][2].y)
    all_theta.append(states[i][0].theta)
    #display_state(states[i])
    
def see_annealing(states, costs):
    plt.figure()
    plt.suptitle("Evolution of states and costs of the simulated annealing")
    plt.subplot(121)
    plt.plot(all_x, 'r')
    plt.plot(all_x1,'b')
    plt.plot(all_x2,'g')
    plt.subplot(122)
    plt.plot(all_y, 'r')
    plt.plot(all_y1,'b')
    plt.plot(all_y2,'g')
    plt.figure()
    plt.plot(costs, 'r')
    plt.title("Costs")
    plt.show()

see_annealing(states, costs)
display_state(state) 
