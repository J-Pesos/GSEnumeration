# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:42:47 2021

@author: joaqu
"""
import networkx as nx ###Necessary for creating node networks and reading edgelists.
import itertools ###Used to iterate to make a list readable.
import matplotlib.pyplot as plt ###Used for reading graphs.
import pandas as pd ###Used to create a data frame from list of dictionaries.
import numpy as np ###Used to create a data array.

magana = nx.read_edgelist("magana_relations.txt", create_using = nx.Graph())
di_magana = nx.read_edgelist("magana_relations.txt", create_using = nx.DiGraph())

nx.draw(di_magana,with_labels=True, font_weight='bold') ###Creates visual of node network.
plt.show()

print(list(magana.nodes))
magana_list = list(magana.nodes)
magana_list.sort(key = int)
print(magana_list)

def full_list_predecessors(source): 
    '''A function which creates a list of predecessors for each source (individual).'''
    p = []
    p.append((list(di_magana.predecessors(source)))) ###Appends list of predecessors of source individual from directional node network.
    if len(p[0]) == 2: ###If there are two direct parents, append them to the list so we can then run the recursive loop to find their parents.
        p.append(full_list_predecessors(p[0][0]))
        p.append(full_list_predecessors(p[0][1]))
    elif len(p[0]) == 1: ###If there is one direct parent, append them to the list so we can then run the recursive loop to find their parents.
        p.append(full_list_predecessors(p[0][0]))
    
    p = list(itertools.chain(*p)) ###Translate the p into a list we can use.
        
    return p

def full_list_successors(source): 
    '''A function which creates a list of sucesssors for each source (individual).'''
    p = []
    p.append((list(di_magana.successors(source)))) ###Appends list of predecessors of source individual from directional node network.
    if len(p[0]) >= 1: ### If there is at least one child returned.
        for child in range(len(p[0])): #Iterate through all sucessors to find their children.
            p.append(full_list_successors(p[0][child])) ###Append children to the list so we can then run the recursive loop to find their children.
            print(p)
    p = list(itertools.chain(*p)) ###Translate the p into a list we can use.
        
    return p

magana_pred = []

for id in magana_list: 
    '''For each other ID in the list of nodes, creates shortest paths between source and target ID.'''
    s = str(id)
    id_pred = full_list_predecessors(s) ###id_pred is a list of all predecessors of the source individual ID being evaluated.
    id_pred.sort(key = int) ###Sorts the list of predecessors by numerical ID.
    n = [s] ###n is a list of the ID of the individual as a string.
    
    for node in range (0, len(magana_list)):
        t = str(magana_list[node]) ###t is the target individual.
        pred = full_list_predecessors(t) ###Generates a list of predecessors for target individual.
        pred.sort(key = int) ###Sorts list of predecessors by numerical ID.
        common_pred = [node for node in pred if node in id_pred] ###Creates a list of target predecessors also shared with source individual.
        common_pred.sort(key = int) ###Sorts list of common predecessors by numerical ID.
        if len(common_pred) >= 1 or t in id_pred or s in pred: ###If length of common predecessors is greater than 1, or target is source predecessor, or source is target predecessor.
            path = nx.shortest_path(magana, source = str(id), target = t) ###Creates the shortest list between source predecessor and target.
            num_edges = len(path) - 1
            n.append(num_edges)
        else:
            n.append(0)
    magana_pred.append(n) ###Appends list of lists of relationships per each target individual.    
              
print(magana_pred)

def relative_typeless(path): 
    ''''Defines a function which returns a non-gendered relationship between the source individual and target ID's.'''
    relation = ""
    for edge in range(0, len(path) - 1):
        relative1 = str(path[edge])
       #print(relative1)
        relative2 = str(path[edge + 1])
       #print(relative2)
        if relative2 in list(di_magana.predecessors(relative1)):
            relation = relation + "p"
        if relative2 in list(di_magana.successors(relative1)):
            relation = relation + "c"
    print(t, "is", str(path[0]) + "'s", relation)
    return relation ###Relation in terms of parent and child edges.
    
id_pred = full_list_predecessors(str(magana_list[0])) ###Assigns the variable id_pred to the full list of predecessors for individual 1.
id_pred.sort(key = int)
print(id_pred)

meioses_array = np.zeros((len(magana_list) + 1,len(magana_list) + 1), dtype = object) ###Creates two arrays in which to place info for generation depth and meioses events.
generationdepth_array = np.zeros((len(magana_list) + 1,len(magana_list) + 1), dtype = object)

meioses_array[0, 0] = 'ID' ###Labels the first cell (first row, first column) as 'ID' to compare individuals.
generationdepth_array[0,0] = 'ID'

cell = 1 ###Populates the first row and column with the specific IDs of each individual in the family.
for id in magana_list:
    meioses_array[0, cell] = id
    meioses_array[cell, 0] = id
    generationdepth_array[0, cell] = id
    generationdepth_array[cell, 0] = id
    cell += 1

def add_meioses_count(path): 
    '''Counts and lists the generation difference between two individuals defined by the relation local variable.'''
    meioses_events = 0
    for edge in path:
        meioses_events += 1
    return meioses_events

def add_generation_depth(path): 
    '''Counts and lists the generation difference between two individuals defined by the relation local variable.'''
    depth = 0
    for edge in path:
        if edge == 'p':
            depth += 1
        elif edge == 'c':
            depth -= 1
    return depth

for current_node in magana_list: ###Combines all functions to generate 2 data matrices of relationship features.
    s = str(current_node)
    source_pred = full_list_predecessors(s)
    source_succ = full_list_successors(s)
    me_list = [] ###Creates an empty list of meioses events between source and target.
    gd_list = [] ###Creates an empty list of generation depth between source and target.
    for node in magana_list: ###Loops through each individual in the node network.
        t = str(node) ###Target individual as a string.
        target_pred = full_list_predecessors(t) ###Generates a list of predecessors for target individual.
        common_pred = [node for node in target_pred if node in source_pred] ###Compares predecessors of target individual and source individual. 
        #target_succ = full_list_successors(t)
        #common_succ = [node for node in target_succ if node in source_succ] ###Compares successors of source individual and target individual.
        if len(common_pred) >= 1 or t in source_pred: ###If common predecessors are greater than or equal to 1, or target is source's predecessor.
            path = list(nx.all_shortest_paths(magana, source = s, target = t))
            if len(path) == 1: ###If there is only one path from source to target, generate values for GD and ME.
                relation = relative_typeless(path[0])
                me = add_meioses_count(relation)
                gd = add_generation_depth(relation)
                meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = me
                generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = gd
            else: ###If both paths are present, append both.
                relation1 = relative_typeless(path[0])
                relation2 = relative_typeless(path[1])
                me_1 = add_meioses_count(relation1)
                gd_1 = add_generation_depth(relation1)
                me_2 = add_meioses_count(relation2)
                #gd_2 = add_generation_depth(relation2)
                meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = (me_1,me_2)
                generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = gd_1
        elif t in source_succ: ###If target is source's successor.
            path = list(nx.all_shortest_paths(magana, source = s, target = t))
            if len(path) == 1: ###If there is only one path from source to target, generate values for GD and ME.
                relation = relative_typeless(path[0])
                me = add_meioses_count(relation)
                gd = add_generation_depth(relation)
                meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = me
                generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = gd
            else: ###If both paths are present, append both.
                relation1 = relative_typeless(path[0])
                relation2 = relative_typeless(path[1])
                me_1 = add_meioses_count(relation1)
                gd_1 = add_generation_depth(relation1)
                me_2 = add_meioses_count(relation2)
                #gd_2 = add_generation_depth(relation2)
                meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = (me_1,me_2)
                generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = gd_1
        elif s == t: ###If the source individual is the target individual.
            me = 0
            gd = 0
            meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = me
            generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = gd
        else:
            meioses_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = 'NA'
            generationdepth_array[magana_list.index(current_node) + 1, magana_list.index(node) + 1] = 'NA'

meioses_df = pd.DataFrame(meioses_array) ###Convert arrays into dataframes.
generationdepth_df = pd.DataFrame(generationdepth_array)

meioses_df.to_excel('meioses_events.xlsx', index = True) ##Save dataframe to xlsx file.
generationdepth_df.to_excel('generation_depth.xlsx', index = True)

####--------------------------- Array of Half vs Full relationships.------------------------------------------
halffull_array = meioses_array.copy() ###Creates a deep copy of meioses_array to evaluate half vs. full relationships.

for horizontal in range(1, len(magana_list) + 1):
    for vertical in range(1, len(magana_list) + 1):
        if type(halffull_array[horizontal][vertical]) == tuple:
            halffull_array[horizontal][vertical] = 'full'
        #elif halffull_array[horizontal][vertical] == 1 and (generationdepth_array[horizontal][vertical] == 1 or generationdepth_array[horizontal][vertical] == -1):
            #halffull_array[horizontal][vertical] = 'full'
        elif halffull_array[horizontal][vertical] == 'NA':
            continue
        elif halffull_array[horizontal][vertical] == 0:
            continue
        elif generationdepth_array[horizontal][vertical] == abs(meioses_array[horizontal][vertical]):
            halffull_array[horizontal][vertical] = 'direct'
        else:
            halffull_array[horizontal][vertical] = 'half'

####--------------------------- Find parent/child relationships.----------------------------------------------

generation_parent = np.where(generationdepth_array == 1) ###Finds all coordinates where generation depth of 1 exists.
print(generation_parent)

print(generation_parent[0]) ###Row index values where GD = 1.
print(generation_parent[1]) ###Column index values where GD = 1.

gd_parent_coord = list(zip(generation_parent[0], generation_parent[1])) ###Zips two index arrays into coordinates.
print(gd_parent_coord)

for coord in gd_parent_coord: ###Print coordinates line by line.
    print(coord)

me_parent = np.where(meioses_array == 1) ###Finds all coordinates where meioses event of 1 exists.

print(me_parent[0]) ###Row index values where ME = 1.
print(me_parent[1]) ###Column index values where ME = 1.

me_coord = list(zip(me_parent[0], me_parent[1])) ###Zips two index arrays into coordinates.
print(me_coord)

for coord in me_coord: ###Print coordinates line by line.
    print(coord)

parent_coordinates = set(gd_parent_coord) - ( set(gd_parent_coord) - set(me_coord) ) ###Creates a set of coordinates where GD = 1 and ME = 1.

parent_coordinates = list(parent_coordinates) ###Converts coordinates of parents from set to list.

generation_child = np.where(generationdepth_array == -1) ###Finds all coordinates where generation depth of -1 exists.
print(generation_child)

gd_child_coord = list(zip(generation_child[0], generation_child[1])) ###Zips two index arrays into coordinates.

child_coordinates = set(gd_child_coord) - ( set(gd_child_coord) - set(me_coord) ) ###Creates a set of coordinates where GD = -1 and ME = 1.

child_coordinates = list(child_coordinates) ###Converts coordinates of children from set to list.

coord_index = 0 ###Converts parent_coordinates (child, parent) to a list of corresponding ID's found in original magana text file.
for coord in parent_coordinates:
    parent_coordinates[coord_index] = ( magana_list[coord[0] - 1], magana_list[coord[1] - 1] )
    coord_index += 1

coord_index = 0 ###Converts child_coordinates (parent, child) to a list of corresponding ID's found in original magana text file.
for coord in child_coordinates:
    child_coordinates[coord_index] = ( magana_list[coord[0] - 1], magana_list[coord[1] - 1] )
    coord_index += 1

child_coordinates_df = pd.DataFrame(child_coordinates, columns = ['parent ID', 'child ID']) ###Creates data frame from list of child_coordinate tuples.

magana_original = pd.read_csv('magana_relations.txt', sep = '\t', header = None) ###Import original magana text file as a dataframe.
magana_original.columns = ['parent ID', 'child ID'] ###Name columns of original data frame.
#magana_original = magana_original.drop(columns = '{}') ###Drops unnecessary column.

child_coordinates_df = child_coordinates_df.astype(int) ###Convert all columns of DataFrame to int64 for merging.
magana_original = magana_original.astype(int)

parent_child_validation = pd.merge(child_coordinates_df, magana_original, how='left', indicator='Exist') ###Merges child coordinates and original txt dfs and creates a separate column if each row is present in both dataframes.
parent_child_validation['Exist'] = np.where(parent_child_validation.Exist == 'both', True, False)

###--------------------------- Find any relationship.----------------------------------------------

def find_relationship():
    '''Conducts a search across two matrices, meioses_array and generationdepth_array, to find all instances of a specific relationship.'''
    gd_input = input('Enter generation depth: ')
    gd_input = int(gd_input)
    print('You have selected', gd_input, 'generation depth.')
    
    
    me_input = input('Enter number/tuple of meioses events: ')
    me_input = int(me_input)
    print('You have selected', me_input, 'number of meioses events.')
    
    full_half_input = input('Enter half or full: ')
    full_half_input = str(full_half_input)
    print('You have selected', full_half_input, 'relationships.')
    
    generation_input = np.where(generationdepth_array == gd_input) ###Finds all coordinates where input generation depth exists.
    print(generation_input)
    
    print(generation_input[0]) ###Row index values where GD = input.
    print(generation_input[1]) ###Column index values where GD = input.
    
    gd_input_coord = list(zip(generation_input[0], generation_input[1])) ###Zips two index arrays into coordinates.
    print(gd_input_coord)
    
    for coord in gd_input_coord: ###Print coordinates line by line.
        print(coord)
    
    meioses_input = np.where(meioses_array == me_input) ###Finds all coordinates where meioses event of input exists.
    
    print(meioses_input[0]) ###Row index values where ME = input.
    print(meioses_input[1]) ###Column index values where ME = input.
    
    me_input_coord = list(zip(meioses_input[0], meioses_input[1])) ###Zips two index arrays into coordinates.
    print(me_input_coord)
    
    for coord in me_input_coord: ###Print coordinates line by line.
        print(coord)
    
    coordinates_input = set(gd_input_coord) - ( set(gd_input_coord) - set(me_input_coord) ) ###Creates a set of coordinates where GD = input and ME = input.
    
    coordinates_input = list(coordinates_input) ###Converts coordinates of parents from set to list.
    
    coord_index = 0 ###Converts coordinates_input (relative1, relative2) to a list of corresponding ID's found in original magana text file.
    for coord in coordinates_input:
        coordinates_input[coord_index] = ( magana_list[coord[0] - 1], magana_list[coord[1] - 1] )
        coord_index += 1
    
    print(coordinates_input)
    print('There are', len(coordinates_input), 'relationships.')

find_relationship()