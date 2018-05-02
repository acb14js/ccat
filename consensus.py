import kmedoids as km
from scipy import stats
import numpy as np
import bct
from itertools import combinations
import sys

def distance_matrix(connectivity_mx):
    print("Building distance matrix...")

    m, n, n = connectivity_mx.shape
    distance_mx = np.zeros((n, m, m))

    for i in range(n):
        print("Calculating node distance " + str(i))
        sel_node = connectivity_mx[:, i, :]

        correlation, _ = stats.spearmanr(sel_node, axis=1)
        distance_mx[i] = 1 - correlation

    return distance_mx

def consensus_matrix(distance_mx, ks):
    print("Building consensus matrix")

    n, m, m = distance_mx.shape
    
    cons_mx = np.zeros((ks-1, m, m))

    for k in range(2, ks):
        count = 1
        for node in distance_mx:
            print("Clustering for k = " + str(k) + " node " + str(count))

            _, clusters = km.kMedoids(node, k)

            for value in clusters.values():
                pairs = list(combinations(value, 2))
                for ij in pairs:
                    i, j = ij
                    cons_mx[k-2][i][j] += 1
                    cons_mx[k-2][j][i] += 1
            
            count += 1

        cons_mx[k-2] = cons_mx[k-2]/float(n)
        cons_mx[k-2] = cons_mx[k-2]/float(k)

    cons_mx = np.sum(cons_mx, axis=0)
    print("...built!")

    return cons_mx

def modularity_maximisation(consensus_mx):
    partition, _ = bct.community_louvain(consensus_mx)
    
    return partition
