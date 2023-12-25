#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 03:14:56 2023

@author: Ben Kamis

Description: The magnitude of the electrostatic force throughout a plane
             due to randomly placed and randomly charged point charges
"""

import random
import matplotlib.pyplot as plt

def matrix_maker(N):
    ''' Generates a NxN matrix of zeroes '''
    
    matrix = []
    row = []
    for i in range(N):
        row.append(0)
    
    for i in range(N):
        matrix.append(row)
        
    return matrix

def point_maker(P, N):
    ''' Makes a list of P points with coordinates from 0 to N and a charge component '''
    
    points = []
    for i in range(P):
        # Establishes X and Y coordinates of a new random point (may be duplicates)
        coords = random.sample(range(1, N + 1), 2)
        # Establishes a charge that can be either -1 or 1
        charge = (random.sample(range(0, 2), 1)[0] - 0.5) * 2
        # Generates a list of the coordinates of a point and its charge
        coords.append(charge)
        # Appends the point charge to the list of all point charges
        points.append(coords)
        
    return points

def coulomb_potential(x_dist, y_dist, charge):
    ''' Calculates the Force at a point due to Coulomb's Law '''
    
    k = 100 # Realistically this would be Coulomb's Constant, but here k is used
            # as a scaling factor to make the points on the graph a reasonable size
            
    # For the point at the charge, the distance is set to be 0.6 as an arbitrary scaling factor
    if x_dist == 0 and y_dist == 0:
        F = k * charge / 0.6
    # For all other points, the distance actually matters
    else:
        F = k * charge / (x_dist ** 2 + y_dist ** 2)    
    return F

def distance_calc(matrix, charges):
    ''' Using the coordinates of each charge, calculates the distance from that charge
        to all points in the NxN matrix plane '''
    
    lst_of_lsts = []
        
    for P in charges:
        for x in range(len(matrix)):
            # Each inner list in the list of lists matrix is small_lst
            small_lst = []
            for y in range(len(matrix[x])):
                x_dist = x - P[0]
                y_dist = y - P[1]
                # The force due to each point is calculated here!
                force = coulomb_potential(x_dist, y_dist, P[2])
                small_lst.append(force)
            # Each small_lst is appended, this matrix is the whole force field
            # for each point
            lst_of_lsts.append(small_lst)
    # lst_of_lsts is a NxP matrix where each value is the charge "felt" at each point
    # in each row of the NxN location matrix
    return lst_of_lsts

def matrix_subdivider(mat, N):
    ''' Separates NxNxP matrices into a PxNxN matrix of points '''
    big_mat = []
    while len(mat) > 0: # Generates mat1, an NxN matrix
        mat1 = []
        while len(mat1) < N:
            # As each NxN matrix is taken from the NxNxP matrix, it is appended to the
            # "big (NxNxN) matrix" and removed from the NxNxP
            mat1.append(mat[0])
            mat.pop(0)
        big_mat.append(mat1)
    
    return big_mat

def matrix_adder(big_mat, matrix):
    ''' The P NxN matrices re added together, item by item, until there is
        only one NxN matrix which represents the sum of all forces 
        at all points in the plane from all charges present '''
    while len(big_mat) > 1:
        # X and Y are each NxN matrices of charge rows
        X = big_mat[0]
        # Matrices are removed from the big matrix list as they are added together
        big_mat.pop(0)
        Y = big_mat[0]
        big_mat.pop(0)
        result = matrix
        # This mini equation adds the points from one NxN matrix to another NxN matrix
        result = [[X[i][j] + Y[i][j] for j in range(len(X[0]))] for i in range(len(X))]
        # Two matrices are removed and summed, the sum is appended back into the big matrix
        # This decreases the length of the big matrix by 1 for every loop iteration
        big_mat.append(result)
    
    return big_mat

def plotter(matrix, charge_matrix):
    ''' Plots the points of the NxN matrix '''
    # Generating the x axis of the graph
    x = []
    for i in range(len(charge_matrix)):
        x.append(i)
    
    # Turns the matrix (list of lists) of charges into an N-long list of lists
    # where each inner list is the x coord, y coord, and charge
    full_lst = []
    x = 0
    y = 0
    for lst in charge_matrix[0]:
        for charge in lst:
            # The color of each point charge is red if positive and blue if negative
            if charge > 0:
                color = "red"
            elif charge == 0:
                # The color if charge = 0 does not matter, because the size will be 0 too
                color = "black"
            else:
                color = "blue"
            point = [x, y, charge, color]
            full_lst.append(point)
            y += 1
        y = 0
        x += 1
        
    plt.title("Forces experienced in a plane due to randomly placed charges")
    for i in full_lst:
        # Each point in the graph is in the NxN matrix. The points are plotted at all
        # integer locations in the plane. The size of each point corresponds to how
        # strongly positive or negative it is. The color is as defined above
        plt.scatter(i[0], i[1], s = abs(i[2]), c = i[3])
    
def main():
    
    N = int(input("How large of a plane? ")) # Number of rows and columns in the square matrix
    matrix = matrix_maker(N)
    
    P = int(input("How many point charges? ")) # Number of point charges to generate
    charges = point_maker(P, N)
    
    '''
    One could set custom charges here. These charges may have any x and y
    coordinates (even not within the matrix) and any float input as the charge.
    If setting charges manually, the "P" input does not matter, as it will
    be overwritten.
    '''
    
    # Some examples:
    # charges = [[round(N/4), round(N/2), -1.0], [round(3*N/4), round(N/2), -1.0], [round(N/2), round(N/2), 2.2]]
    # charges = [[round(N/4), round(N/4), -1], [round(N/4), round(3*N/4), -1], [round(3*N/4), round(N/4), -1], [round(3*N/4), round(3*N/4), -1], [round(N/2), round(N/2), 5]]
    
    charge_matrices = distance_calc(matrix, charges)
    charge_matrices_lst = matrix_subdivider(charge_matrices, N)
    charge_matrix = matrix_adder(charge_matrices_lst, matrix)
    
    plotter(matrix, charge_matrix)

if __name__ == "__main__":
        main()