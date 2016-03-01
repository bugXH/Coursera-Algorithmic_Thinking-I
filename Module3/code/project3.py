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
    dist, idx1, idx2 = float('inf'), -1, -1
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
        mid = (p[m - 1].horiz_center() + p[m].horiz_center()) / 2
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
    p = cluster_list
    s = [i for i in range(len(p))
         if math.fabs(p[i].horiz_center() - horiz_center) < half_width]
    p.sort(key=lambda cluster: cluster.vert_center())
    k = len(s)
    dist, idx1, idx2 = float('inf'), -1, -1
    for u in range(k - 2):
        for v in range(u + 1, min(u + 3, k - 1)):
            dist, idx1, idx2 = get_min((dist, idx1, idx2),
                                       pair_distance(p, s[u], s[v]))
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
    new_cluster_list: list
    a list of clusters whose length is num_clusters
    """
    new_cluster_list = cluster_list[:]

    while len(new_cluster_list) > num_clusters:
        dist, idx1, idx2 = fast_closest_pair(new_cluster_list)
        new_cluster_list[idx1].merge_clusters(new_cluster_list[idx2])
        del new_cluster_list[idx2]

    return new_cluster_list


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

    # position initial clusters at the location of
    # clusters with largest populations
    cluster_n = len(cluster_list)

    miu_k = sorted(cluster_list,
                   key=lambda c: c.total_population())[-num_clusters:]
    miu_k = [c.copy() for c in miu_k]

    # n: cluster_n
    # q: num_iterations
    for _ in xrange(num_iterations):
        cluster_result = [alg_cluster.Cluster(set([]), 0, 0, 0, 0)
                          for _ in range(num_clusters)]
        # put the node into closet center node

        for jjj in xrange(cluster_n):
            min_num_k = 0
            min_dist_k = float('inf')
            for num_k in xrange(len(miu_k)):
                dist = cluster_list[jjj].distance(miu_k[num_k])
                if dist < min_dist_k:
                    min_dist_k = dist
                    min_num_k = num_k

            cluster_result[min_num_k].merge_clusters(cluster_list[jjj])

        # re-computer its center node
        for kkk in xrange(len(miu_k)):
            miu_k[kkk] = cluster_result[kkk]

    return cluster_result

