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
    return (cluster_list[idx1].distance(cluster_list[idx2]),
            min(idx1, idx2), max(idx1, idx2))


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
    dist, idx1, idx2 = float('inf'), -1, -1
    for idx_u in range(len(cluster_list)):
        for idx_v in range(len(cluster_list)):
            if idx_u != idx_v:
                dist, idx1, idx2 = min((dist, idx1, idx2),
                                       pair_distance(cluster_list, idx_u, idx_v))
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
    cluster_list.sort(key=lambda cluster: cluster.horiz_center())
    if len(cluster_list) <= 3:
        (dist, idx1, idx2) = slow_closest_pair(cluster_list)
    else:
        len_m = len(cluster_list) / 2
        set_pl = cluster_list[:len_m]
        set_pr = cluster_list[len_m:]
        dist_dl, idx_il, idx_jl = fast_closest_pair(set_pl)
        dist_dr, idx_ir, idx_jr = fast_closest_pair(set_pr)
        dist, idx1, idx2 = min((dist_dl, idx_il, idx_jl),
                               (dist_dr, idx_ir + len_m, idx_jr + len_m))
        mid = (cluster_list[len_m - 1].horiz_center() +
               cluster_list[len_m].horiz_center()) / 2
        dist, idx1, idx2 = min((dist, idx1, idx2),
                               (closest_pair_strip(cluster_list, mid, dist)))

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
    set_bigs = [i for i in range(len(cluster_list))
                if abs(cluster_list[i].horiz_center() - horiz_center) <
                half_width]
    len_k = len(set_bigs)
    set_bigs.sort(key=lambda i: cluster_list[i].vert_center())
    dist, idx1, idx2 = float('inf'), -1, -1
    for idx_u in range(len_k - 1):
        for idx_v in range(idx_u + 1, min(idx_u + 3, len_k - 1) + 1):
            dist_tmp = pair_distance(cluster_list,
                                     set_bigs[idx_u], set_bigs[idx_v])
            dist, idx1, idx2 = min((dist, idx1, idx2), dist_tmp)
    return (dist, idx1, idx2)


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Parameters
    ----------
    cluster_list: list
    a list of clusters

    num_clusters: int
    integer number of clusters


    Returns
    -------
    clusters: list
    a list of clusters whose length is num_clusters
    """
    clusters = cluster_list[:]

    while len(clusters) > num_clusters:
        pair = fast_closest_pair(clusters)
        idx1, idx2 = pair[1], pair[2]
        clusters[idx1].merge_clusters(clusters[idx2])
        clusters.pop(idx2)
    return clusters

######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Parameters
    ----------
    cluster_list: list
    a list of clusters

    num_clusters: int
    number of clusters

    num_iterations: int
    number of iterations


    Returns
    -------
    result: list
    a list of clusters whose length is num_clusters
    """
    clusters = cluster_list[:]
    len_n = len(clusters)
    mu_k = sorted(clusters,
                  key=lambda c: c.total_population())[-num_clusters:]
    mu_k = [c.copy() for c in mu_k]

    for _ in range(num_iterations):
        result = [alg_cluster.Cluster(set([]), 0, 0, 0, 0)
                  for _ in range(num_clusters)]

        for idx_j in range(len_n):
            min_num_k = 0
            min_dist_k = float('inf')
            for num_k in range(len(mu_k)):
                dist = clusters[idx_j].distance(mu_k[num_k])
                if dist < min_dist_k:
                    min_dist_k = dist
                    min_num_k = num_k

            result[min_num_k].merge_clusters(clusters[idx_j])

        for idx_k in range(len(mu_k)):
            mu_k[idx_k] = result[idx_k]

    return result

