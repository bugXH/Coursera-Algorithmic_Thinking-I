"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance
    between two clusters in a list

    Parameters
    ----------
    cluster_list: list
    list of clusters

    idx1: int
    index for a cluster

    idx2: int
    index for another cluster


    Returns
    -------
    (dist, idx1, idx2): tuple
    dist is distance between cluster_list[idx1] and cluster_list[idx2]
    """
    dist = cluster_list[idx1].distance(cluster_list[idx2])
    idx1 = min(idx1, idx2)
    idx2 = max(idx1, idx2)
    return (dist, idx1, idx2)


def get_min(tuple1, tuple2):
    """
    Compare the first element in both tuples and return the smaller one

    Parameters:
    tuple1: tuple
    (distance, index1, index2)

    tuple2: tuple
    another set of (distance, index1, index2)
    """
    if tuple1[0] <= tuple2[0]:
        return tuple1
    else:
        return tuple2


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Parameters
    ----------
    cluster_list: list
    the list of clusters


    Returns
    -------
    (dist, idx1, idx2): tuple
    where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    dist, idx1, idx2 = pair_distance(cluster_list, 0, 1), 0, 1
    for u in range(len(cluster_list)):
        for v in range(len(cluster_list)):
            if u != v:
                dist, idx1, idx2 = get_min((dist, idx1, idx2),
                                           pair_distance(cluster_list, u, v))
    return (dist, idx1, idx2)


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Parameters
    ----------
    cluster_list: list
    list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Returns
    -------
    (dist, idx1, idx2): tuple
    where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    p = cluster_list
    n = len(p)

    if n <= 3:
        (dist, idx1, idx2) = slow_closest_pair(p)
    else:
        m = n / 2
        pl = [p[i]
              for i in range(len(p)) if i < m]
        pr = [p[i]
              for i in range(len(p)) if i >= m]
        dl, il, jl = fast_closest_pair(pl)
        dr, ir, jr = fast_closest_pair(pr)
        dist, idx1, idx2 = get_min((dl, il, jl), (dr, ir + m, jr + m))
        mid = (p[m - 1].horiz_pos + p[m].horiz_pos) / 2
        dist, idx1, idx2 = get_min((dist, idx1, idx2),
                                   (closest_pair_strip(p, mid, dist)))

    return (dist, idx1, idx2)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Parameters
    ----------
    cluster_list:list
    a list of clusters produced by fast_closest_pair()

    horiz_center: float
    the horizontal position of the strip's vertical center line

    half_width: float
    the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)


    Returns
    -------
    (dist, idx1, idx2): tuple
    where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2]
    lie in the strip and have minimum distance dist.
    """

    return ()
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []

