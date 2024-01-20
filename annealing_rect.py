#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:44:21 2020

@author: aravind
"""
from polygon_intersection import get_rectangle,RotatedRect
from polygon_intersection import do_polygons_intersect,point_to_line_dist
import math

#            Remove z coordinate

wall_x = 20
wall_y = 20
rows, cols = (5, 5) 
M = 20
#M_arr = [[0,5,5,5,5],[5,0,5,5,5],[5,5,0,5,5],[5,5,5,0,5],[5,5,5,5,0]]


class ObjectClass:
  def __init__(self,a,b,is_fixed,M,classid):
    self.classid = classid
    self.a = a
    self.b = b
    self.M = M
    self.is_fixed = is_fixed
        
        
class Object(ObjectClass) :
  def __init__(self,theta,x,y,z,oid,classid,M,is_fixed,a,b):
    super(Object,self).__init__(a,b,is_fixed,M,classid)
    self.theta = theta
    self.x = x
    self.y = y
    self.z = math.inf
    self.oid = oid

  def get_distance(self,o2):
      return math.sqrt((self.x-o2.x)**2 + (self.y-o2.y)**2) # + (self.z-o2.z)**2)



def get_cost_C1(o1,o2):
    d12 = o1.get_distance(o2)
    bb1 = 0.5*math.sqrt(o1.a**2 + o1.b**2)
    bb2 = 0.5*math.sqrt(o2.a**2 + o2.b**2)
    a = get_rectangle(o1.x,o1.y,o1.a,o1.b,o1.theta)
    b = get_rectangle(o2.x,o2.y,o2.a,o2.b,o2.theta)
    r1 = RotatedRect(o1.x,o1.y,o1.a,o1.b,o1.theta)
    r2 = RotatedRect(o1.x,o1.y,o1.a,o1.b,o1.theta)
    
    if do_polygons_intersect(a, b):
        return r1.intersection(r2).area
    
    return 0

def get_cost_C2(o1,o2,alpha):
    d12 = o1.get_distance(o2)
    bb1 = 0.5*math.sqrt(o1.a**2 + o1.b**2)
    bb2 = 0.5*math.sqrt(o2.a**2 + o2.b**2)
    if (bb1+bb2 > d12):
        return ((bb1+bb2)/(d12+0.001))*alpha
    
    if ((bb1+bb2 <d12) and (d12 < M)):
        return 0;
    
    return (d12/(bb1+bb2))*alpha

def get_cost_C3(all_obj,o1,o2):
    bb1 = 0.5*math.sqrt(o1.a**2 + o1.b**2)
    bb2 = 0.5*math.sqrt(o2.a**2 + o2.b**2)
    x = (o1.x + o2.x)/2
    y = (o1.y + o2.y)/2
    #z = (o1.z + o2.z)/2
    cost = 0
    
    for obj in all_obj:
        bb = 0.5*math.sqrt(obj.a**2 + obj.b**2)
        if(obj != o1 and obj != o2):
            cost += max(0,bb+(bb2+ bb1 +o1.get_distance(o2))/2. -
                    math.sqrt((x-obj.x)**2 + (y-obj.y)**2 )) # (z-obj.z)**2))
    return cost
"""
def get_cost_C4(o1):
    a = get_rectangle(o1.x,o1.y,o1.a,o1.b,o1.theta)
    sum = 0
    for point in a:
        if point[0] > wall_x:
            sum += (point[0]-wall_x)**2
        if point[1] > wall_y:
            sum += (point[1]-wall_y)**2
        if point[0] <0:
            sum += (-point[0])**2
        if point[1] <0:
            sum += (-point[1])**2
        
    return sum
"""
def get_cost_C5(o1):
    a = get_rectangle(o1.x,o1.y,o1.a,o1.b,o1.theta)
    min_dist = math.inf
    for point in a:
        min_dist = min(min_dist,min(abs(wall_x - point[0]),min(abs(wall_y-point[1]),min(abs(point[0]),abs(point[1])))))
            
    return min_dist**2 /1000.


def get_cost_C6(o1):
    return ((min(abs(o1.theta),abs(o1.theta-90)))**2)/1000.


def get_overall_cost(all_obj,alpha):
    cost = 0
    for i in range(len(all_obj)):
        for j in range(i+1,len(all_obj)):
            cost += get_cost_C1(all_obj[i],all_obj[j]) + get_cost_C2(all_obj[i],all_obj[j],alpha) + get_cost_C3(all_obj,all_obj[i],all_obj[j])+get_cost_C5(all_obj[i])+ get_cost_C6(all_obj[i])
    return cost


if __name__=='__main__':

    chair1 = Object(0,19,19,0,1,1,20,False,2,3)
    chair2 = Object(45,20,20,4,2,1,20,False,3,3)
    chair3 = Object(0,10,10,2,3,1,20,False,2,4)

    all_obj = [chair1,chair2,chair3]
    print(get_cost_C1(chair1,chair2))
    print(get_cost_C2(chair1,chair2,2))
    print(get_cost_C3(all_obj,chair1,chair2))
    print(get_cost_C5(chair2))
    print(get_cost_C6(chair2))
    
    print(get_overall_cost(all_obj,2))
    
    