import sys
import argparse
from pprint import pprint
import re

def find_more_common() :
    #iterate through all clusters and find the 2 clusters with the most in common
    #the 2 clusters with the most in common are the clusters with the smallest diffenrce
    #this is done by calling the appropriate method,based on the desired implementation
    #when done,return the 2 clusters as a list
    
    common = []
    min = 1000
    pos1 = 0
    pos2 = 1
    for i in range(len(clusters_distance)):
        for j in range(len(clusters_distance)):
            if  clusters_distance[i][j] < min : 
                if clusters_distance[i][j] != 0 :
                    if i != j:
                        min = clusters_distance[i][j]
                        pos1 = i
                        pos2 = j

    # pos1 < pos2 has to be true for our code to work, else we will mess the deletions
    if pos1 > pos2 :
        pos1, pos2 = pos2, pos1
    common.append(clusters[pos1])
    common.append(clusters[pos2])
    return common, pos1, pos2

def create_new_cluster(common, pos1, pos2) :
    
    cluster = [[0] for j in range(3)]
    string = "({})({})".format(common[0][0],common[1][0])
    cluster[0] = string
    cluster[1] = clusters_distance[pos1][pos2]
    
    pattern = r'\([\d\s]+\)'
    number = re.findall(pattern, cluster[0])
    cluster[2] = len(number)
    print(cluster[0], cluster[1], cluster[2])

    #end program when the last cluster has been created
    if cluster[2] == 10:
        sys.exit()
    
    return cluster

def update_clusters_distance(u, s, t, pos1, pos2) :
    #u is the cluster that has just been created
    #s is parent one, pos 1 its position in clusters and clusters_distance
    #t is parent two, pos2 its position in clusters and clusters_distance

    #first in order to update the clusters distance list, we have to delete the parents
    delete_clusters_distance()    


    #then we have to increase our clusters_distance rows by 1, to represent the new cluster and then append it to the list.
    new_cluster_row = [0 for i in range(len(clusters_distance) + 1)]
    clusters_distance.append(new_cluster_row)

    #then we have to do the same thing for the columns
    for column in clusters_distance:
        column.append(0)
    
    #then we have to initialise our constants.
    if implementation == 'single' or implementation == 'complete' :

        ai, aj, b, c = initialise_constants()
        for i in range(len(clusters_distance)):
            d = ai * clusters_distance[pos1][i] + aj * clusters_distance[pos2][i] + b * clusters_distance[pos1][pos2] + c * abs(clusters_distance[pos1][i] -  clusters_distance[pos2][i] )
            clusters_distance[-1][i] = d
    elif implementation == 'average' :

        try:
            ai = abs ( abs(s[2]) / abs(s[2]) + abs(t[2])  )
            aj = abs ( abs(t[2]) / abs(s[2]) + abs(t[2])  )
        except ZeroDivisionError:
            ai = 0
            aj = 0
        b = 0
        c = 0
        for i in range(len(clusters_distance)):
            d = ai * clusters_distance[pos1][i] + aj * clusters_distance[pos2][i] + b * clusters_distance[pos1][pos2] + c * abs(clusters_distance[pos1][i] -  clusters_distance[pos2][i])
            clusters_distance[-1][i] = d

    elif implementation == 'ward' :
    
        for i in range(len(clusters_distance)):
            try:
                ai = ( abs(s[2])    +   abs(clusters[i][2])  )  /  ( abs(s[2])  + abs(clusters[i][2])  + abs(t[2])    )
                aj = ( abs(t[2])    +   abs(clusters[i][2])  )  /  ( abs(s[2])  + abs(clusters[i][2])  + abs(t[2])    )
                b  = (-1) *  (  abs(clusters[i][1])  ) / ( abs(s[1])  + abs(clusters[i][1])  + abs(t[1]) )
            except ZeroDivisionError:
                ai = 0
                aj = 0
                b = 0
            
            c  = 0
            d = ai * clusters_distance[pos1][i] + aj * clusters_distance[pos2][i] + b * clusters_distance[pos1][pos2] + c * abs(clusters_distance[pos1][i] -  clusters_distance[pos2][i] )
            clusters_distance[-1][i] = d
    else :
        raise Exception('Wrong file method')


    return None

def delete_clusters_distance():
    #we now have to delete all rows and columns representing the cluster at pos1, and do the same exact thing for the cluster that pos2 represents.

    del clusters_distance[pos2]
    del clusters_distance[pos1]

    for i in clusters_distance:
        del i[pos2]
        del i[pos1]

    return None

def update_clusters(cluster) :
    #add the new cluster to the clusters list.
    #on column 0 we have its parents,
    #on column 1 its parents distance
    #and on column 2 their number

    clusters.append(cluster)

    #now we have to remove the 2 previous clusters from the clusters list
    #deletes the clusters at pos1,and pos2 that have been merged into the new cluster.
    del clusters[pos1]
    #we write -1  because if we dont, the numbers will be problematic because we have already deleted 1 row.
    del clusters[pos2 - 1]

def initialise_constants():
    #works only for single or complete!!!!!!!!
    if implementation == 'single' :
        ai = 1/2
        aj = 1/2
        b = 0
        c = -1/2
    elif implementation == 'complete' :
        ai = 1/2
        aj = 1/2
        b = 0
        c = 1/2
    elif implementation == 'average' :
        ai = 0
        aj = 0
        b = 0
        c = 0
        #content yet to be filled
    elif implementation == 'ward' :
        ai = 0
        aj = 0
        b = 0
        c = 0
        #content yet to be filled
    else :
        raise Exception("Wrong file method.")
    
    return ai, aj, b, c

#read the lines of the file and store them in a list as strings
implementation = sys.argv[1]
file = open(sys.argv[2])
str_numbers = file.read().split()

#make the strings into ints-clusters
data = []
for number in str_numbers :
    data.append(int(number))
file.close()

#create the initial  clusters 
#clusters is a list of clusters. each cluster has its children on the column 0.
#on column 1 it has the distance between its parents
#on column 2 it has the number of its children.

clusters = [[0 for i in range(0,3)] for j in data]
for i in range(len(data)) :
       clusters[i][0] = data[i]
clusters.sort()

#create a 2dimension list the contains the distance between every cluster i and every cluster j
number = len(clusters)
clusters_distance = [[0 for i in range(number)] for j in range(number) ]

#and initialise the first distance values
for i in range(len(clusters_distance)):
   for j in range(len(clusters_distance)) :
        clusters_distance[i][j] = abs(clusters[i][0] - clusters[j][0])

#initialise the constants based on the method
ai, aj, b, c = initialise_constants()

#start creating new clusters
while len(clusters) > 1 :

    #find the 2 clusters with the most in common as a list, and their positions
    two_more_common, pos1, pos2  = find_more_common()

    #create new cluster
    cluster = create_new_cluster(two_more_common, pos1, pos2)

    #remove previous clusters and append the new one to clusters_distance
    if len(clusters_distance) > 1  :
        update_clusters_distance(cluster, clusters[pos1], clusters[pos2], pos1, pos2)

    #then do the same thing for clusters
    update_clusters(cluster)