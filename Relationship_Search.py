# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:03:31 2022

@author: joaquin
"""
import networkx as nx ###Necessary for creating node networks and reading edgelists.
import itertools ###Used to iterate to make a list readable.
import pandas as pd ###Used to create a data frame from list of dictionaries.
import numpy as np ###Used to create a data array.
import argparse ###Used to make user defined inputs.

parser = argparse.ArgumentParser()

def load_args():

    parser.add_argument('-gd','--generation', type=int)
    parser.add_argument('-me','--meioses', type=int)
    parser.add_argument('-t','--type', type=str)
    parser.add_argument('-o', '--output', type=str)
    
    return parser.parse_args()
    
generation_file = pd.read_excel('generation_depth.xlsx', header = 0, index_col= 0)
meioses_file = pd.read_excel('meioses_events.xlsx', header = 0, index_col = 0)
half_full_sib_file = pd.read_excel('half_full.xlsx', header = 0, index_col = 0)

def find_relationship(): ###Returns number of relationships defined by command input.
    '''Conducts a search across two matrices, meioses_file and generation_file, to find all instances of a specific relationship.'''
    gd_input = user_args.generation
    print('You have selected', gd_input, 'generation depth.')
    
    me_input = user_args.meioses
    print('You have selected', me_input, 'number of meioses events.')
    
    fh_input = user_args.type
    print('You have selected', fh_input, 'relationships.')
    
    generation_input = np.where(generation_file == gd_input) ###Finds all coordinates where input generation depth exists.
    
    gd_input_coord = list(zip(generation_input[0], generation_input[1])) ###Zips two index arrays into coordinates.
    
    meioses_input = np.where(meioses_file == me_input) ###Finds all coordinates where meioses event of input exists.
    
    me_input_coord = list(zip(meioses_input[0], meioses_input[1])) ###Zips two index arrays into coordinates.
    
    full_half_input = np.where(half_full_sib_file == fh_input) ###Finds all coordinates where relationship full/half input exists.
    
    fh_input_coord = list(zip(full_half_input[0], full_half_input[1])) ###Zips two index arrays into coordinates.
    
    coordinates_input = set.intersection(set(gd_input_coord), set(me_input_coord), set(fh_input_coord)) ###Creates a set of coordinates where GD = input, FH = input, and ME = input.
    
    coordinates_input = list(coordinates_input) ###Converts coordinates of parents from set to list.
    
    coord_index = 0 ###Converts coordinates_input (relative1, relative2) to a list of corresponding ID's found in original family text file.
    for coord in coordinates_input:
        coordinates_input[coord_index] = ( family_list[coord[0] - 1], family_list[coord[1] - 1] )
        coord_index += 1
    
    global glob_coordinates
    glob_coordinates = coordinates_input ###Creates global variable of coordinates for relationships.
    print(coordinates_input)
    
    print('There are', len(coordinates_input), 'relationships.') ###Enumerates the number of relationships found.
    
    if len(coordinates_input) != 0: ###Informs the user that coordinates of relationships (if found) are available in a separate file.
        if type(user_args.output) == str:
            print('Relationships have been written to ' + out_prefix + '_returned_relationships.txt')
        else:
            print('Your results have been written to ' + nx_prefix + '_returned_relationships.txt')
    
    if type(user_args.output) == str:
        with open(out_prefix + '_returned_relationships.txt', 'w') as output_file: ###Writes out relationship IDs to a text file.
            for coord in coordinates_input:
                output_file.write(str(coord) + '\n')
        output_file.close()
    else:
        with open(nx_prefix + '_returned_relationships.txt', 'w') as output_file: ###Writes out relationship IDs to a text file.
            for coord in coordinates_input:    
                output_file.write(str(coord) + '\n')
        output_file.close()
    
def find_relationship_looped():
    '''Conducts a search across two matrices, meioses_file and generation_file, to find all instances of a specific relationship.'''
    gd_input = input('Enter generation depth: ')
    gd_input = int(gd_input)
    print('You have selected', gd_input, 'generation depth.')
    
    
    me_input = input('Enter number of meioses events: ')
    me_input = int(me_input)
    print('You have selected', me_input, 'number of meioses events.')
    
    fh_input = input('Enter half, full, direct, or NA: ')
    fh_input = str(fh_input)
    print('You have selected', fh_input, 'relationships.')
    
    generation_input = np.where(generation_file == gd_input) ###Finds all coordinates where input generation depth exists.
    
    gd_input_coord = list(zip(generation_input[0], generation_input[1])) ###Zips two index arrays into coordinates.
    
    meioses_input = np.where(meioses_file == me_input) ###Finds all coordinates where meioses event of input exists.
    
    me_input_coord = list(zip(meioses_input[0], meioses_input[1])) ###Zips two index arrays into coordinates.
    
    full_half_input = np.where(half_full_sib_file == fh_input) ###Finds all coordinates where relationship full/half input exists.
    
    fh_input_coord = list(zip(full_half_input[0], full_half_input[1])) ###Zips two index arrays into coordinates.
    
    coordinates_input = set.intersection(set(gd_input_coord), set(me_input_coord), set(fh_input_coord)) ###Creates a set of coordinates where GD = input, FH = input, and ME = input.
    
    coordinates_input = list(coordinates_input) ###Converts coordinates of parents from set to list.
    
    coord_index = 0 ###Converts coordinates_input (relative1, relative2) to a list of corresponding ID's found in original family text file.
    for coord in coordinates_input:
        coordinates_input[coord_index] = ( family_list[coord[0] - 1], family_list[coord[1] - 1] )
        coord_index += 1
    
    global glob_coordinates 
    glob_coordinates = coordinates_input ###Creates global variable of coordinates for relationships.
    print(coordinates_input)
    
    print('There are', len(coordinates_input), 'relationships.') ###Enumerates the number of relationships found.
    
    if len(coordinates_input) != 0: ###Informs the user that coordinates of found relationships are available in a separate file.
        if type(user_args.output) == str:
            print('Relationships have been written to ' + out_prefix + '_returned_relationships.txt')
        else:
            print('Your results have been written to ' + nx_prefix + '_returned_relationships.txt')
            
    if type(user_args.output) == str:
        with open(out_prefix + '_returned_relationships.txt', 'w') as output_file: ###Writes out relationship IDs to a text file.
            for coord in coordinates_input:
                output_file.write(str(coord) + '\n')
        output_file.close()
    else:
        with open(nx_prefix + '_returned_relationships.txt', 'w') as output_file: ###Writes out relationship IDs to a text file.
            for coord in coordinates_input:    
                output_file.write(str(coord) + '\n')
        output_file.close()
    
if __name__ == '__main__':

    user_args = load_args() #Load in user arguments
    
    nx_prefix = user_args.networkx.split('.txt')[0] ###Store prefix of input file.
    out_prefix = user_args.output.split('.csv')[0] ###Store prefix of user desired output file.
    
    family = nx.read_edgelist(user_args.networkx, create_using=nx.Graph())
    
    family_list = list(family.nodes)
    family_list.sort(key=int)
    
    glob_coordinates = []
    
    find_relationship()
    
    i = 0
    while i < 10:
        find_relationship_looped()