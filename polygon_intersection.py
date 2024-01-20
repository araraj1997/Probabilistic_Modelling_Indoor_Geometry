#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 11:32:09 2020

@author: aravind
"""

#%%
import numpy as np
import math
import shapely
from shapely import geometry

def point_to_line_dist(point, line):
    """Calculate the distance between a point and a line segment.

    To calculate the closest distance to a line segment, we first need to check
    if the point projects onto the line segment.  If it does, then we calculate
    the orthogonal distance from the point to the line.
    If the point does not project to the line segment, we calculate the 
    distance to both endpoints and take the shortest distance.

    :param point: Numpy array of form [x,y], describing the point.
    :type point: numpy.core.multiarray.ndarray
    :param line: list of endpoint arrays of form [P1, P2]
    :type line: list of numpy.core.multiarray.ndarray
    :return: The minimum distance to a point.
    :rtype: float
    """
    # unit vector
    unit_line = line[1] - line[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)

    # compute the perpendicular distance to the theoretical infinite line
    segment_dist = (
        np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
        np.linalg.norm(unit_line)
    )

    diff = (
        (norm_unit_line[0] * (point[0] - line[0][0])) + 
        (norm_unit_line[1] * (point[1] - line[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + line[0][0]
    y_seg = (norm_unit_line[1] * diff) + line[0][1]

    endpoint_dist = min(
        np.linalg.norm(line[0] - point),
        np.linalg.norm(line[1] - point)
    )

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]  # line point 1 x
    lp1_y = line[0][1]  # line point 1 y
    lp2_x = line[1][0]  # line point 2 x
    lp2_y = line[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        return -1


def get_min_distance(a,b):
    min1 = math.inf
    for point1 in a:
        for point2 in b:
            min1 = min(min1,math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))
    min2 = math.inf
    for point in a:
        line1 = np.array([b[0],b[1]])
        line2 = np.array([b[1],b[2]])
        line3 = np.array([b[2],b[3]])
        line4 = np.array([b[3],b[1]])
        
        if(point_to_line_dist(point, line1)!= -1):
            d1 = point_to_line_dist(point, line1)
        else:
            d1 = math.inf
        if(point_to_line_dist(point, line2)!= -1):
            d2 = point_to_line_dist(point, line2)
        else:
            d2 = math.inf
        if(point_to_line_dist(point, line3)!= -1):
            d3 = point_to_line_dist(point, line3)
        else:
            d3 = math.inf
        if(point_to_line_dist(point, line4)!= -1):
            d4 = point_to_line_dist(point, line4)
        else:
            d4 = math.inf
        
        min2 = min(min2,min(d1,min(d2,min(d3,d4))))
        
    min3 = math.inf
    
    for point in b:
        line1 = np.array([a[0],a[1]])
        line2 = np.array([a[1],a[2]])
        line3 = np.array([a[2],a[3]])
        line4 = np.array([a[3],a[1]])
        
        if(point_to_line_dist(point, line1)!= -1):
            d1 = point_to_line_dist(point, line1)
        else:
            d1 = math.inf
        if(point_to_line_dist(point, line2)!= -1):
            d2 = point_to_line_dist(point, line2)
        else:
            d2 = math.inf
        if(point_to_line_dist(point, line3)!= -1):
            d3 = point_to_line_dist(point, line3)
        else:
            d3 = math.inf
        if(point_to_line_dist(point, line4)!= -1):
            d4 = point_to_line_dist(point, line4)
        else:
            d4 = math.inf
        
        min3 = min(min3,min(d1,min(d2,min(d3,d4))))
    
    return min(min1,min(min2,min3))
    
#%%
def get_rectangle(cx,cy,a,b,theta):
    theta = math.radians(theta)
    rect = [[-a/2,-b/2],[a/2,-b/2],[-a/2,b/2],[a/2,b/2]]
    new_rect = []
    for points in rect:
        new_rect.append([points[0]*math.cos(theta)-points[1]*math.sin(theta)+cx,
                         points[0]*math.sin(theta)+points[1]*math.cos(theta)+cy])
    
    return new_rect

#print(get_rectangle(1,3,1,2,45))

#%%      
        
    
def do_polygons_intersect(a, b):
    """
 * Helper function to determine whether there is an intersection between the two polygons described
 * by the lists of vertices. Uses the Separating Axis Theorem
 *
 * @param a an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @param b an ndarray of connected points [[x_1, y_1], [x_2, y_2],...] that form a closed polygon
 * @return true if there is any intersection between the 2 polygons, false otherwise
    """
    polygons = [a, b];
    minA, maxA, projected, i, i1, j, minB, maxB = None, None, None, None, None, None, None, None

    for i in range(len(polygons)):

        # for each polygon, look at each edge of the polygon, and determine if it separates
        # the two shapes
        polygon = polygons[i];
        for i1 in range(len(polygon)):

            # grab 2 vertices to create an edge
            i2 = (i1 + 1) % len(polygon);
            p1 = polygon[i1];
            p2 = polygon[i2];

            # find the line perpendicular to this edge
            normal = { 'x': p2[1] - p1[1], 'y': p1[0] - p2[0] };

            minA, maxA = None, None
            # for each vertex in the first shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            for j in range(len(a)):
                projected = normal['x'] * a[j][0] + normal['y'] * a[j][1];
                if (minA is None) or (projected < minA): 
                    minA = projected

                if (maxA is None) or (projected > maxA):
                    maxA = projected

            # for each vertex in the second shape, project it onto the line perpendicular to the edge
            # and keep track of the min and max of these values
            minB, maxB = None, None
            for j in range(len(b)): 
                projected = normal['x'] * b[j][0] + normal['y'] * b[j][1]
                if (minB is None) or (projected < minB):
                    minB = projected

                if (maxB is None) or (projected > maxB):
                    maxB = projected

            # if there is no overlap between the projects, the edge we are looking at separates the two
            # polygons, and we know there is no overlap
            if (maxA < minB) or (maxB < minA):
                print("polygons don't intersect!")
                return False;

    return True


class RotatedRect:
    def __init__(self, cx, cy, w, h, angle):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.angle = angle

    def get_contour(self):
        w = self.w
        h = self.h
        c = geometry.box(-w/2.0, -h/2.0, w/2.0, h/2.0)
        rc = shapely.affinity.rotate(c, self.angle)
        return shapely.affinity.translate(rc, self.cx, self.cy)

    def intersection(self, other):
        return self.get_contour().intersection(other.get_contour())