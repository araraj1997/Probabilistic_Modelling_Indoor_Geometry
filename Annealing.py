#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:48:19 2019

@author: aravind
"""
import math
#            Remove z coordinate

wall_x = 50
wall_y = 50
rows, cols = (5, 5) 

M_arr = [[0,5,5,5,5],[5,0,5,5,5],[5,5,0,5,5],[5,5,5,0,5],[5,5,5,5,0]]


class ObjectClass:
  def __init__(self,radius,is_fixed,M,classid):
    self.classid = classid
    self.M = M
    self.is_fixed = is_fixed
    self.radius = radius
        
        
class Object(ObjectClass) :
  def __init__(self,theta,x,y,z,oid,classid,M,is_fixed,radius,dw = 5,aw = 10):
    super(Object,self).__init__(radius,is_fixed,M,classid)
    self.theta = theta
    self.x = x
    self.y = y
    self.z = math.inf
    self.dw = dw
    self.aw = aw
    self.oid = oid

  def get_distance(self,o2):
      return math.sqrt((self.x-o2.x)**2 + (self.y-o2.y)**2) # + (self.z-o2.z)**2)



def get_cost_C1(o1,o2):
    d12 = o1.get_distance(o2)
    r1 = o1.radius
    r2 = o2.radius
    
    return max(0,r1+r2-d12)

def get_cost_C2(o1,o2,alpha):
    d12 = o1.get_distance(o2)
    r1 = o1.radius
    r2 = o2.radius
    M = M_arr[o1.oid-1][o2.oid-1]
    if (r1+r2 > d12):
        return ((r1+r2)/(d12+0.001))*alpha
    
    if ((r1+r2 <d12) and (d12 < M)):
        return 0;
    
    return (d12/(r1+r2))*alpha

def get_cost_C3(all_obj,o1,o2):
    r1 = o1.radius
    r2 = o2.radius
    x = (o1.x + o2.x)/2
    y = (o1.y + o2.y)/2
    z = (o1.z + o2.z)/2
    cost = 0
    
    for obj in all_obj:
        if(obj != o1 and obj != o2):
            cost += max(0,obj.radius+(r2+ r1 +o1.get_distance(o2))/2 -
                    math.sqrt((x-obj.x)**2 + (y-obj.y)**2 )) # (z-obj.z)**2))
    return cost

def get_cost_C4(o1):
    return ((min(abs(wall_x - o1.x),min(abs(wall_y - o1.y),min(abs(o1.x),abs(o1.y)))))**2)/100.

def get_cost_C5(o1):
    return ((min(abs(o1.theta),abs(o1.theta-90)))**2)/100.


def get_overall_cost(all_obj,alpha):
    cost = 0
    for i in range(len(all_obj)):
        for j in range(i+1,len(all_obj)):
            cost += get_cost_C1(all_obj[i],all_obj[j]) + get_cost_C2(all_obj[i],all_obj[j],alpha) + get_cost_C3(all_obj,all_obj[i],all_obj[j])+ get_cost_C4(all_obj[i]) + get_cost_C5(all_obj[i])
    return cost


if __name__=='__main__':

    chair1 = Object(0,2,0,0,1,1,20,False,2)
    chair2 = Object(0,2,3,4,2,1,20,False,3)
    chair3 = Object(0,1,2,2,3,1,20,False,2)

    all_obj = [chair1,chair2,chair3]
    print(chair2.radius)
    
    print(get_overall_cost(all_obj,2))
    
    
    
    
    