# -*- coding: utf-8 -*-
###Enumerates a all possible relationships found in a family node network.
import networkx as nx #!Necessary for creating node networks and reading edgelists.
import random
import itertools
import csv #!Used to import csv data.
import os
import matplotlib.pyplot as plt #!Used for reading graphs.
import pandas as pd #!Used to create a data frame from list of dictionaries.
import numpy as np #!Used to create a data array.

#rohlfs = nx.read_edgelist("rohlfs_relations.txt", create_using = nx.Graph()) #!Imports relationships as non-directional node network.
#di_rohlfs = nx.read_edgelist("rohlfs_relations.txt", create_using = nx.DiGraph()) #!Imports relationships as directional node network.
magana = nx.read_edgelist("magana_relations.txt", create_using = nx.Graph())
di_magana = nx.read_edgelist("magana_relations.txt", create_using = nx.DiGraph())

#nx.draw(di_rohlfs,with_labels=True, font_weight='bold') #!Creates visual of node network.
#plt.show() ###Shows visual.
nx.draw(di_magana,with_labels=True, font_weight='bold') #!Creates visual of node network.
plt.show()

#nx.info(rohlfs) #!Provides information on node network, # of nodes (individuals) and # of edges (parent-child relationships).
nx.info(magana)

#print(list(rohlfs.nodes)) #!Prints list of all individual ID's.
print(list(magana.nodes))
magana_list = list(magana.nodes)
magana_list.sort(key = int)
print(magana_list)

#attrs = {}
#with open('rohlfs_profiles.txt', 'r') as txt_file:
    #txt_reader = csv.reader(txt_file, delimiter='\t') #!Reads tab delimited file and removes tabs. Make sure columns are separated by tabbed spaces.
    #for line in txt_reader:
        #attrs.update( {line[0]: {'alive' : line[2], 'birth_year': line[4]}} ) #!Creates attributes dictionary with values [alive: ' ', birth_year: ' ']

attrs = {}
with open('magana_profiles.txt', 'r') as txt_file:
    txt_reader = csv.reader(txt_file, delimiter='\t') #!Reads tab delimited file and removes tabs. Make sure columns are separated by tabbed spaces.
    for line in txt_reader:
        attrs.update( {line[0]: {'birthplace' : line[2], 'birth_year': line[3]}} )
        
#nx.set_node_attributes(rohlfs, attrs)
#print(list(rohlfs.nodes(data = True)))
nx.set_node_attributes(magana, attrs)
print(list(magana.nodes(data = True)))

# =============================================================================
# def full_list_predecessors(source): #!A function which creates a list of predecessors for each source (individual).
#     p = []
#     p.append((list(di_rohlfs.predecessors(source)))) #!Appends list of predecessors of source individual from directional node network.
#     if len(p[0]) == 2: #!If there are two direct parents, append them to the list so we can then run the recursive loop to find their parents.
#         p.append(full_list_predecessors(p[0][0]))
#         p.append(full_list_predecessors(p[0][1]))
#     elif len(p[0]) == 1: #!If there is one direct parent, append them to the list so we can then run the recursive loop to find their parents.
#         p.append(full_list_predecessors(p[0][0]))
#     
#     p = list(itertools.chain(*p)) #!Translate the p into a list we can use.
#         
#     return p
# =============================================================================

def full_list_predecessors(source): #!A function which creates a list of predecessors for each source (individual).
    p = []
    p.append((list(di_magana.predecessors(source)))) #!Appends list of predecessors of source individual from directional node network.
    if len(p[0]) == 2: #!If there are two direct parents, append them to the list so we can then run the recursive loop to find their parents.
        p.append(full_list_predecessors(p[0][0]))
        p.append(full_list_predecessors(p[0][1]))
    elif len(p[0]) == 1: #!If there is one direct parent, append them to the list so we can then run the recursive loop to find their parents.
        p.append(full_list_predecessors(p[0][0]))
    
    p = list(itertools.chain(*p)) #!Translate the p into a list we can use.
        
    return p

#pred57 = full_list_predecessors('57') #!Generates a list of predecessors for individual 57.
#print(pred57)
pred1 = full_list_predecessors('1')
pred1.sort(key = int)
print(pred1)
    

# =============================================================================
# #rohlfs_pred = [[]]
# magana_pred = []
# 
# #for number in range(1,59): #!Generates a list of lists where the first entry is each individual ID.
#     #rohlfs_pred[0].append(i)
# for number in range(1, len(magana_list) + 1): #!Generates a list of lists where the first entry is each individual ID.
#     magana_pred.append([number])
# 
# #print(rohlfs_pred)
# print(magana_pred)
# =============================================================================

# =============================================================================
# for id in list(rohlfs.nodes): #For each other ID in the list of nodes, creates shortest paths between source and target ID.
#     s = str(id)
#     id_pred = full_list_predecessors(str(id)) #!id_pred is a list of all predecessors of the source individual ID being evaluated.
#     n = [s] #n is a list of the ID of the indivudal as a string.
#     
#     for node in range (0, len(list(rohlfs.nodes))):
#         t = str(list(rohlfs.nodes)[node]) #!t is the target individual.
#         pred = full_list_predecessors(t) #!Generates a list of predecessors for target individual.
#         common_pred = [node for node in pred if node in id_pred] #!Creates a list of target predecessors also shared with source individual.
#         if len(common_pred)>=1 or t in id_pred or s in pred: #!If length of common predecessors is greater than 1, or target is source predecessor, or source is target predecessor.
#             path = nx.shortest_path(rohlfs, source = str(id), target = t) #!Creates the shortest list between source predecessor and target.
#             num_edges = len(path) - 1
#             n.append(num_edges)
#         else:
#            n.append(0)
#     rohlfs_pred.append(n) #Appends list of lists of relationships per each target individual.
# =============================================================================
 
#! Create a numpy array of 0s of size big enough to cross reference individuals by ID.
# generation_depth_array = np.zeros((len(magana_list),len(magana_list), dtype = int)))
# meioses_array = np.zeros((len(magana_list),len(magana_list), dtype = int))
# print(generation_depth_array)
# print(meioses_array)
magana_pred = []

for id in magana_list: #!For each other ID in the list of nodes, creates shortest paths between source and target ID.
    s = str(id)
    id_pred = full_list_predecessors(s) #!id_pred is a list of all predecessors of the source individual ID being evaluated.
    id_pred.sort(key = int) #!Sorts the list of predecessors by numerical ID.
    n = [s] #!n is a list of the ID of the individual as a string.
    
    for node in range (0, len(magana_list)):
        t = str(magana_list[node]) #!t is the target individual.
        pred = full_list_predecessors(t) #!Generates a list of predecessors for target individual.
        pred.sort(key = int) #!Sorts list of predecessors by numerical ID.
        common_pred = [node for node in pred if node in id_pred] #!Creates a list of target predecessors also shared with source individual.
        common_pred.sort(key = int) #!Sorts list of common predecessors by numerical ID.
        if len(common_pred) >= 1 or t in id_pred or s in pred: #!If length of common predecessors is greater than 1, or target is source predecessor, or source is target predecessor.
            path = nx.shortest_path(magana, source = str(id), target = t) #!Creates the shortest list between source predecessor and target.
            num_edges = len(path) - 1
            n.append(num_edges)
        else:
           n.append(0)
    magana_pred.append(n) #!Appends list of lists of relationships per each target individual.    
              
#print(rohlfs_pred)
print(magana_pred)

# =============================================================================
# profiles = []
# with open('rohlfs_profiles.txt') as x: #Creates a list of lists of profiles for each individual sorted by ID.
#     for line in x:
#        profiles.append(line.split())
# =============================================================================
profiles = []
with open('magana_profiles.txt') as x: #!Creates a list of lists of profiles for each individual sorted by ID.
    for line in x:
       profiles.append(line.split())
       
print(profiles)
       
attrs = {} 
for d in range(1, len(profiles)): #!Creates a dictionary in which subject ID's are the key and the values are their gender.
    attrs.update( {str(d): {'gender' : profiles[d][1]}} )

print(attrs)

# =============================================================================
# nx.set_node_attributes(rohlfs, attrs)
# print(list(rohlfs.nodes(data = True))) #A list of subject ID's and a dictionary of their attributes.
# =============================================================================
nx.set_node_attributes(magana, attrs)
list(magana.nodes(data = True)) #!A list of subject ID's and a dictionary of their attributes.

# =============================================================================
# def relative_type(path): #Defines a function which returns a gendered relationship between the source individual and target ID's.
#     relation = ""
#     for x in range(0, len(path)-1): #Creates a loop that runs the length of depth between source and target individual -1.
#         relative1 = str(path[x]) #Source individual to compare relative2 against.
#         #print(relative1)
#         relative2 = str(path[x+1]) #Relative to determine relative1 against.
#         #print(relative2)
#         if relative2 in list(di_rohlfs.predecessors(relative1)):
#             if rohlfs.nodes[relative2]['gender'] == 'female':
#                 relation = relation + "mother"
#             elif rohlfs.nodes[relative2]['gender'] == 'male': 
#                 relation = relation + "father" 
#             else: 
#                 relation = relation + "parent"
#         if relative2 in list(di_rohlfs.successors(relative1)):
#             relation = relation + "child"
#     print(t, "is 57's", relation)
#     return relation #Returns a composite relation.
# =============================================================================
def relative_type(path): #!Defines a function which returns a gendered relationship between the source individual and target ID's.
    relation = ""
    for x in range(0, len(path)-1): #!Creates a loop that runs the length of depth between source and target individual -1.
        relative1 = str(path[x]) #!Source individual to compare relative2 against.
        #print(relative1)
        relative2 = str(path[x+1]) #!Relative to determine relative1 against.
        #print(relative2)
        if relative2 in list(di_magana.predecessors(relative1)):
            if magana.nodes[relative2]['gender'] == 'Female':
                relation = relation + "m"
            elif magana.nodes[relative2]['gender'] == 'Male': 
                relation = relation + "f" 
            else: 
                relation = relation + "p"
        if relative2 in list(di_magana.successors(relative1)):
            relation = relation + "c"
    print(t, "is", str(path[0]) + "'s", relation)
    return relation #!Returns a composite relation.

# =============================================================================
# def relative_typeless(path): #Defines a function which returns a non-gendered relationship between the source individual and target ID's.
#     relation = ""
#     for x in range(0, len(path)-1):
#         relative1 = str(path[x])
#        # print(relative1)
#         relative2 = str(path[x+1])
#        # print(relative2)
#         if relative2 in list(di_rohlfs.predecessors(relative1)):
#             relation = relation + "parent"
#         if relative2 in list(di_rohlfs.successors(relative1)):
#             relation = relation + "child"
#     print(t, "is 57's", relation)
#     return relation
# =============================================================================
def relative_typeless(path): #!Defines a function which returns a non-gendered relationship between the source individual and target ID's.
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
    return relation #!Relation in terms of parent and child edges.
    
#id_pred = full_list_predecessors(str(57)) #Assigns the variable id_pred to the full list of predecessors for individual 57.
id_pred = full_list_predecessors(str(1))
id_pred.sort(key = int)
print(id_pred)

# =============================================================================
# all_relations = []
# for node in rohlfs.nodes: #Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
#     t = str(node)
#     pred = full_list_predecessors(t)
#     common_pred= [node for node in pred if node in id_pred]
#     if len(common_pred)>=1 or t in id_pred:
#         path = list(nx.all_shortest_paths(rohlfs, source = "57", target = t))
#         print(path)
#         if len(path) == 1: 
#             #relative_type(path[0])
#             all_relations.append(relative_type(path[0]))
#         else: 
#             all_relations.append(relative_type(path[0]))
#             all_relations.append(relative_type(path[1]))
# =============================================================================
all_relations = []
for node in magana.nodes: #Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
    t = str(node)
    pred = full_list_predecessors(t)
    common_pred= [node for node in pred if node in id_pred]
    if len(common_pred) >= 1 or t in id_pred:
        path = list(nx.all_shortest_paths(magana, source = "1", target = t))
        print(path)
        if len(path) == 1: 
            #relative_type(path[0])
            all_relations.append(relative_type(path[0]))
        else: 
            all_relations.append(relative_type(path[0]))
            all_relations.append(relative_type(path[1]))
            
# =============================================================================
# all_relations_typeless = []
# for node in rohlfs.nodes: #Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
#     t = str(node) #Loops through easch individual in the node network.
#     pred = full_list_predecessors(t) #Generates a list of predecessors for each individual.
#     common_pred = [node for node in pred if node in id_pred] #Compares predecessors of target individual and source individual.
#     if len(common_pred)>=1 or t in id_pred:
#         path = list(nx.all_shortest_paths(rohlfs, source = '57', target = t))
#         print(path)
#         if len(path) == 1: 
#             all_relations_typeless.append(relative_typeless(path[0]))
#         else: 
#             all_relations_typeless.append(relative_typeless(path[0]))
#             all_relations_typeless.append(relative_typeless(path[1]))
# =============================================================================
all_relations_typeless = []
for node in magana_list: #!Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
    t = str(node) #!Loops through each individual in the node network.
    print(t)
    pred = full_list_predecessors(t) #!Generates a list of predecessors for each individual.
    print(pred)
    common_pred = [node for node in pred if node in id_pred] #!Compares predecessors of target individual and source individual.
    print(common_pred)
    if len(common_pred) >= 1 or t in id_pred: #!If common predecessors are greater than 1, or target is source's predecessor.
        path = list(nx.all_shortest_paths(magana, source = '1', target = t))
        print(path)
        if len(path) == 1: #!If there is only one path from source to target, append that one path. 
            all_relations_typeless.append([relative_typeless(path[0])])
        else:  #!If both paths are present, append both.
            all_relations_typeless.append([relative_typeless(path[0]), relative_typeless(path[1])])

relationship_count = { #Initializes a dictionary to keep count of the types of relationships per individual.
    'parent' : 0,
    'child' : 0,
    'full sibling' : 0,
    'half sibling' : 0,
    'avuncular' : 0,
    '1st cousin' : 0,
    '2nd cousin' : 0,
    '3rd cousin' : 0,
    '4th cousin' : 0,
    '5th cousin' : 0
    }

def add_relation_count(): #Defines the relationships returned by the relation local variable.
    for relation in all_relations_typeless:
        if relation == ['p']:
            relationship_count['parent'] += 1
        elif relation == ['c']:
            relationship_count['child'] += 1
        elif relation == ['pc']:
            relationship_count['half sibling'] += 1
        elif relation == ['pc', 'pc']:
            relationship_count['full sibling'] += 1
        elif relation == ['ppc'] or relation == ['ppc','ppc']:
            relationship_count['avuncular'] += 1
        elif relation == ['ppcc'] or relation == ['ppcc','ppcc']:
            relationship_count['1st cousin'] += 1
        elif relation == ['pppccc'] or relation == ['pppccc','pppccc']:
            relationship_count['2nd cousin'] += 1
        elif relation == 'ppppcccc':
            relationship_count['3rd cousin'] += 1
        elif relation == 'pppppccccc':
            relationship_count['4th cousin'] += 1
        elif relation == 'ppppppcccccc':
            relationship_count['5th cousin'] += 1
        else:
            continue

add_relation_count()

print(relationship_count)

meioses_count = {} #Initializes a dictionary to keep count of meioses events and generation depth per individual relationship.

def add_meioses_count(): #Counts and lists the generation difference between two individuals defined by the relation local variable.
    for relation in all_relations_typeless:
        count = 0
        for path in relation:
            count += 1
            edgelist = []
            meioses_count['# Meioses Events ' + str(count)] = 0
            meioses_count['Generation Depth ' + str(count)] = 0
            for edge in path:
                edgelist = edgelist + [edge]
                meioses_count['# Meioses Events ' + str(count)] += 1
                if edge == 'p':
                    meioses_count['Generation Depth ' + str(count)] += 1
                elif edge == 'c':
                    meioses_count['Generation Depth ' + str(count)] -= 1
                else:
                    continue
        print(edgelist)
        
add_meioses_count()

print(meioses_count)

#Begin relationship count for all individuals in pedigree.

# =============================================================================
# relationship_count = {
#     'parent' : 0,
#     'child' : 0,
#     'full sibling' : 0,
#     'half sibling' : 0,
#     'avuncular' : 0,
#     '1st cousin' : 0,
#     '2nd cousin' : 0,
#     '3rd cousin' : 0,
#     '4th cousin' : 0,
#     '5th cousin' : 0}
# =============================================================================

relationship_frequency = []
meioses_frequency = []

# =============================================================================
# for i in rohlfs.nodes:
#     all_relations_typeless = []
#     for node in rohlfs.nodes: #Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
#         t = str(node) #Loops through easch individual in the node network.
#         pred = full_list_predecessors(t) #Generates a list of predecessors for each individual.
#         common_pred = [node for node in pred if node in id_pred] #Compares predecessors of target individual and source individual.
#         if len(common_pred)>=1 or t in id_pred:
#             path = list(nx.all_shortest_paths(rohlfs, source = i, target = t))
#             print(path)
#             if len(path) == 1: 
#                 all_relations_typeless.append(relative_typeless(path[0]))
#             else: 
#                 all_relations_typeless.append(relative_typeless(path[0]))
#                 all_relations_typeless.append(relative_typeless(path[1]))
# 
#     add_relation_count()
# =============================================================================
for current_node in magana.nodes:
    relationship_count = {
        'ID' : str(current_node),
        'parent' : 0,
        'child' : 0,
        'full sibling' : 0,
        'half sibling' : 0,
        'avuncular' : 0,
        '1st cousin' : 0,
        '2nd cousin' : 0,
        '3rd cousin' : 0,
        '4th cousin' : 0,
        '5th cousin' : 0
    }
    meioses_count = {
        'ID' : str(current_node)
        }
    all_relations_typeless = []
    for node in magana.nodes: #Combines all functions to generate a list of lists comparing a source individual and their family member to determine their gendered relationship.
        t = str(node) #Loops through easch individual in the node network.
        pred = full_list_predecessors(t) #Generates a list of predecessors for each individual.
        common_pred = [node for node in pred if node in id_pred] #Compares predecessors of target individual and source individual.
        if len(common_pred)>=1 or t in id_pred:
            path = list(nx.all_shortest_paths(magana, source = current_node, target = t))
            print(path)
            if len(path) == 1: 
                all_relations_typeless.append([relative_typeless(path[0])])
            else: 
                all_relations_typeless.append([relative_typeless(path[0]),relative_typeless(path[1])])
#                all_relations_typeless.append(relative_typeless(path[1]))

    add_relation_count()
    print(relationship_count)
    relationship_frequency.append(relationship_count)
    add_meioses_count()
    print(meioses_count)
    meioses_frequency.append(meioses_count)
    

print(relationship_frequency)
print(meioses_frequency)

relationship_df = pd.DataFrame(relationship_frequency)

relationship_df.to_excel('Magana_Relationships.xlsx',
                         index = False
                         )

meioses_df = pd.DataFrame(meioses_frequency)

meioses_df.to_excel('Magana_Meioses.xlsx',
                         index = False
                         )