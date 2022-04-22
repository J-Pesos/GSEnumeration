# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:42:47 2021

@author: joaquin

edited by miguel 01/12/2022
generation depth is in prespective of the individuals
-1 top (parent) -> down (child)
"""
import networkx as nx ###Necessary for creating node networks and reading edgelists.
import itertools ###Used to iterate to make a list readable.
import pandas as pd ###Used to create a data frame from list of dictionaries.
import numpy as np ###Used to create a data array.
import argparse ###Used to make user defined inputs.

#Initlaize parser object to read in user input via the command line.
parser = argparse.ArgumentParser()

def load_args():

    #MG - Change -f to -n to represent a networkx_file.
    parser.add_argument('-n','--networkx', type=str, required=True)
    parser.add_argument('-gd','--generation', type=int)
    parser.add_argument('-me','--meioses', type=int)
    parser.add_argument('-t','--type', type=str)
    parser.add_argument('-o', '--output', type=str)
    
    return parser.parse_args()

def full_list_predecessors(source): 
    '''A function which creates a list of predecessors for each source (individual).'''
    p = []
    p.append((list(di_family.predecessors(source)))) ###Appends list of predecessors of source individual from directional node network.
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
    p.append((list(di_family.successors(source)))) ###Appends list of predecessors of source individual from directional node network.
    if len(p[0]) >= 1: ### If there is at least one child returned.
        for child in range(len(p[0])): #Iterate through all sucessors to find their children.
            p.append(full_list_successors(p[0][child])) ###Append children to the list so we can then run the recursive loop to find their children.
    p = list(itertools.chain(*p)) ###Translate the p into a list we can use.
        
    return p

def relative_typeless(path): 
    ''''Defines a function which returns a non-gendered relationship between the source individual and target ID's.'''
    relation = ""
    for edge in range(0, len(path) - 1):
        relative1 = str(path[edge])
        relative2 = str(path[edge + 1])
        if relative2 in list(di_family.predecessors(relative1)):
            relation = relation + "p"
        if relative2 in list(di_family.successors(relative1)):
            relation = relation + "c"
    return relation ###Relation in terms of parent and child edges.

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

def identify_relation_statistics(dir_fam, undir_fam):

    fam_list = np.array(dir_fam.nodes) ###Gets list of nodes in family pedigree networkx
    fam_list = np.sort(fam_list.astype(int)).astype(str) ###Sorts the list of nodes to order lowest-> highest

    meioses_array = np.zeros((len(fam_list) + 1, len(fam_list) + 1), dtype=object)  ###Creates two arrays in which to place info for generation depth and meioses events.
    meioses_array.fill(9999) ###Default value of unfilled cell is a nonsense number.
    meioses_array[0, 0] = 'ID'
    meioses_array[0, 1:len(fam_list) + 1] = fam_list
    meioses_array[1:len(fam_list) + 1, 0] = fam_list

    generationdepth_array = np.zeros((len(fam_list) + 1, len(fam_list) + 1), dtype=object)
    generationdepth_array.fill(9999)
    generationdepth_array[0, 0] = 'ID'
    generationdepth_array[0, 1:len(fam_list) + 1] = fam_list
    generationdepth_array[1:len(fam_list) + 1, 0] = fam_list

    # half_full_sib_array = np.zeros((len(fam_list) + 1, len(fam_list) + 1), dtype=object)
    # half_full_sib_array[0,0] = 'ID'
    # half_full_sib_array[0, 1:len(fam_list) + 1] = fam_list
    # half_full_sib_array[1:len(fam_list) + 1, 0] = fam_list


    # for node1_idx in range(0, len(fam_list)):
    #     for node2_idx in range(node1_idx + 1, len(fam_list)):

    #         indiv1 = fam_list[node1_idx]  ###Gets raw node for first individual based off index
    #         indiv2 = fam_list[node2_idx]  ###Gets raw node for second individual based off index
    #         #print(indiv1, indiv2)

    #         ###Idenitfy meioses count between a pair of individuals.
    #         me = 0
    #         meioses_array[node1_idx+1][node2_idx+1] = me  ###Inputting value into matrix
    #         meioses_array[node2_idx+1][node1_idx+1] = me  ###Inputting value into matrix

    #         ### identify generation depth between a pair of individuals
    #         gd = 0
    #         generationdepth_array[node1_idx+1][node2_idx+1] = gd  ###Inputting value into matrix
    #         generationdepth_array[node2_idx+1][node1_idx+1] = gd  ###Inputting value into matrix

    #         ### idenitfy half, full sibling status between a pair of individuals
    #         rel_status = 'NA'
    #         half_full_sib_array[node1_idx+1][node2_idx+1] = rel_status  ###Inputting value into matrix
    #         half_full_sib_array[node2_idx+1][node1_idx+1] = rel_status  ### Inputting value into matrix

    #code to clean the matricies before inputting
    return (meioses_array, generationdepth_array)

def unknown_or_half(id1, id2): ###Assesses whether two individuals are actually half siblings or have an unknown relationship.
    pred_id1 = full_list_predecessors(id1) ###Store predecessors of id1.
    pred_id2 = full_list_predecessors(id2) ###Store predecessors of id2.
    #print('Predecessors 1: ', pred_id1)
    #print('Predecessors 2: ', pred_id2)
    for pred in pred_id1[::-1]: ###Iterates through predecessor list in reverse to find common ancestor with greatest GD.
        if pred in pred_id2[::-1]:
            common_pred = pred ###Common ancestor with greatest GD.
            break
    #print('Common ancestor: ', common_pred)
    successors = full_list_successors(common_pred) ###Creates a list of successors to common ancestor.
    #print('Successors: ', successors)
    for succ in successors:
        if succ in pred_id1 and succ not in pred_id2:
            child_1 = succ ###child_1 is the first successor that is ancestor to id1 but not id2.
            #print('Child 1: ', child_1)
            break
        else:
            child_1 = id1
    for succ in successors:
        if succ in pred_id2 and succ not in pred_id1:
            child_2 = succ ###child_2 is the first successor that is ancestor to id2 but not id1.
            #print('Child 2: ', child_2)
            break
        else:
            child_2 = id2
    child_1_parents = list(di_family.predecessors(child_1))
    child_2_parents = list(di_family.predecessors(child_2))
    #print('Parents 1: ', child_1_parents, ' Parents 2: ', child_2_parents)
    if len(child_1_parents) == 2 and len(child_2_parents) == 2: ###Checks to make sure there are at least two parent individuals.
        if child_1_parents != child_2_parents: ###Check to see if parents are shared. If they are not, it is a half relationship.
            return 'half'
    else: ###Otherwise unknown.
        return 'unknown'

if __name__ == '__main__':

    user_args = load_args() #Load in user arguments
    
    nx_prefix = user_args.networkx.split('.txt')[0] ###Store prefix of input file.
    out_prefix = user_args.output.split('.csv')[0] ###Store prefix of user desired output file.

    glob_coordinates = [] ###Creates a global variable to store coordinates_input variable once it is generated.
    
    #Load in family as a directed/undirected graph node based pedigree.
    family = nx.read_edgelist(user_args.networkx, create_using=nx.Graph())
    di_family = nx.read_edgelist(user_args.networkx, create_using=nx.DiGraph())

    #### Start function here
    meioses_file, generation_file = identify_relation_statistics(family, di_family)
    #print(meioses_file)
    #print(generation_file)
    #print(half_sib_file)

    family_list = list(family.nodes)
    family_list.sort(key=int)
    family_pred = []
    
    node_index = 0
    for current_node in family_list:  ###Combines all functions to generate 2 data matrices of relationship features.
        s = str(current_node)
        source_pred = full_list_predecessors(s)
        source_succ = full_list_successors(s)
        me_list = []  ###Creates an empty list of meioses events between source and target.
        gd_list = []  ###Creates an empty list of generation depth between source and target.
        for node in family_list[node_index + 1:]:  ###Loops through each individual in the node network, never evaluating an individual against themself.
            t = str(node)  ###Target individual as a string.
            target_pred = full_list_predecessors(t)  ###Generates a list of predecessors for target individual.
            common_pred = [node for node in target_pred if node in source_pred]  ###Compares predecessors of target individual and source individual.
            if len(common_pred) >= 1 or t in source_pred:  ###If common predecessors are greater than or equal to 1, or target is source's predecessor.
                path = list(nx.all_shortest_paths(family, source=s, target=t))
                if len(path) == 1:  ###If there is only one path from source to target, generate values for GD and ME.
                    relation = relative_typeless(path[0]) # function to find the relative type ppc
                    me = add_meioses_count(relation) # get meises count
                    gd = add_generation_depth(relation) # get generation depth
                    meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = me
                    generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = gd
                else:  ###If both paths are present, append both.
                    relation1 = relative_typeless(path[0])
                    relation2 = relative_typeless(path[1])
                    me_1 = add_meioses_count(relation1)
                    gd_1 = add_generation_depth(relation1)
                    me_2 = add_meioses_count(relation2)
                    meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = (me_1, me_2)
                    generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = gd_1
            elif t in source_succ:  ###If target is source's successor.
                path = list(nx.all_shortest_paths(family, source=s, target=t))
                if len(path) == 1:  ###If there is only one path from source to target, generate values for GD and ME.
                    relation = relative_typeless(path[0])
                    me = add_meioses_count(relation)
                    gd = add_generation_depth(relation)
                    meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = me
                    generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = gd
                else:  ###If both paths are present, append both.
                    relation1 = relative_typeless(path[0])
                    relation2 = relative_typeless(path[1])
                    me_1 = add_meioses_count(relation1)
                    gd_1 = add_generation_depth(relation1)
                    me_2 = add_meioses_count(relation2)
                    meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = (me_1, me_2)
                    generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = gd_1
            elif s == t:  ###If the source individual is the target individual.
                me = 0
                gd = 0
                meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = me
                generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = gd
            else:
                meioses_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = 'NA'
                generation_file[family_list.index(current_node) + 1, family_list.index(node) + 1] = 'NA'
        node_index += 1 ###Increase index value to compare novel nodes against each other.
    ###Convert array into dataframes.
    generationdepth_df = pd.DataFrame(generation_file)

    ####--------------------------- Array of Half vs Full relationships.------------------------------------------
    half_full_sib_file = meioses_file.copy()  ###Creates a deep copy of meioses_file to evaluate half vs. full relationships.

    for horizontal in range(1, len(family_list) + 1):
        for vertical in range(1, len(family_list) + 1):
            if type(half_full_sib_file[horizontal][vertical]) == tuple:
                half_full_sib_file[horizontal][vertical] = 'full'
            elif half_full_sib_file[horizontal][vertical] == 'NA':
                continue
            elif half_full_sib_file[horizontal][vertical] == 0:
                continue
            elif abs(generation_file[horizontal][vertical]) == meioses_file[horizontal][vertical]:
                half_full_sib_file[horizontal][vertical] = 'direct'
            elif len(list(di_family.predecessors(family_list[horizontal - 1]))) == 1: ###If number of direct successors for ind1 is only one.
                half_full_sib_file[horizontal][vertical] = 'unknown'
            elif len(list(di_family.predecessors(family_list[vertical - 1]))) == 1: ###If number of direct successors for ind2 is only one.
                half_full_sib_file[horizontal][vertical] = 'unknown'
            else:
                half_full_sib_file[horizontal][vertical] = unknown_or_half(family_list[horizontal - 1], family_list[vertical - 1]) ###Assesses whether two individuals are actually half siblings or have an unknown relationship.

    halfful_df = pd.DataFrame(half_full_sib_file)  ###Convert new array into dataframes.
    
    halfful_df.to_excel('half_full.xlsx', index=True)  ###Save halfull dataframe to xlsx file.

    ###-------------------------- Convert tuples to singular integers for meioses events.--------------------------
    for horizontal in range(1, len(family_list) + 1):
        for vertical in range(1, len(family_list) + 1):
            if type(meioses_file[horizontal][vertical]) == tuple:
                meioses_file[horizontal][vertical] = meioses_file[horizontal][vertical][1]
                
    meioses_df = pd.DataFrame(meioses_file)

    meioses_df.to_excel('meioses_events.xlsx', index=True)  ###Save dataframe to xlsx file.
    generationdepth_df.to_excel('generation_depth.xlsx', index=True)

    find_relationship()
    
    ###-------------------------- Assemble all relationship info into one matrix. ----------------------------------
    summary_matrix = np.zeros((len(family_list)*len(family_list), 5), dtype=object) ###Create summary matrix.
    
    column_names = ['Indiv1','Indiv2','relationship type','generation depth','meioses events'] ###Define column for data frame.
    
    row = 0
    for ID1 in range(0, len(family_list)): ###Populate summary matrix with data taken from other matrices.
        for ID2 in range(ID1 + 1, len(family_list)):
            summary_matrix[row][0] = family_list[ID1]
            summary_matrix[row][1] = family_list[ID2]
            summary_matrix[row][2] = half_full_sib_file[ID1 + 1][ID2 + 1]
            summary_matrix[row][3] = generation_file[ID1 + 1][ID2 + 1]
            summary_matrix[row][4] = meioses_file[ID1 + 1][ID2 + 1]
            row += 1
    
    summary_matrix = np.delete(summary_matrix, np.where(summary_matrix[:,2:5] == 'NA'), axis = 1) ###Remove rows with NA.
    summary_matrix = np.delete(summary_matrix, np.where(summary_matrix[:,0:2] == 0), axis = 1) ###Remove excess rows where IDs are '0' and '0'.
    
    summary_df = pd.DataFrame(summary_matrix) ###Convert array to dataframe with column names.
    summary_df.columns = column_names
    
    if type(user_args.output) == str:
        summary_df.to_csv(user_args.output, sep='\t', index=False) ###Save summary dataframe to csv file using output argument.
    else:
        summary_df.to_csv(nx_prefix + '_pairwise_relationships.csv', sep='\t', index = False) ###If no output name provided create csv using default networkx file name.