"""
Implementation for application 3
"""
from project3 import (fast_closest_pair, slow_closest_pair,
                      hierarchical_clustering, kmeans_clustering)
from matplotlib import pyplot as plt
from random import randint
from alg_cluster import Cluster
from alg_project3_viz import load_data_table, DATA_3108_URL
from alg_clusters_matplotlib import plot_clusters
from time import time


def gen_random_clusters(num_clusters):
    """
    Creates a list of clusters where each cluster
    in this list corresponds to one randomly generated
    point in the square with corners (+-1, +-1)

    Parameters
    ----------
    num_clusters: int
    the number of the clusters to generate


    Returns
    -------
    clusters: list
    the list of clusters generated
    """
    clusters = []
    for _ in range(num_clusters):
        new_cluster = Cluster(set([]), randint(-1, 1), randint(-1, 1), 0, 0)
        clusters.append(new_cluster)
    return clusters


def question1_plot():
    """
    Generate the plot for question 1
    """
    runtime_slow = []
    runtime_fast = []

    clusters = []
    for size in range(2, 201):
        clusters.append(gen_random_clusters(size))

    # count runtime
    for cluster_list in clusters:
        slow_start = time()
        slow_closest_pair(cluster_list)
        slow_end = time()
        runtime_slow.append(slow_end - slow_start)

        fast_start = time()
        fast_closest_pair(cluster_list)
        fast_end = time()
        runtime_fast.append(fast_end - fast_start)

    xs = [_ for _ in range(2, 201)]
    plt.title('Running Times Comparison (Implemented in Desktop Python)')
    plt.xlabel('sizes of random clusters')
    plt.ylabel('running times (seconds)')
    for runtime in [runtime_slow, runtime_fast]:
        plt.plot(xs, runtime)
    legend_texts = ['slow_closest_pair', 'fast_closest_pair']
    plt.legend(legend_texts, loc='upper left')
    plt.show()


def question2_plot():
    """
    Generate the plot for question 2
    """
    data_table = load_data_table(DATA_3108_URL)

    singleton_list = []
    for line in data_table:
        cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
        singleton_list.append(cluster)
    cluster_list = hierarchical_clustering(singleton_list, 15)
    plot_clusters(data_table, cluster_list, True)


def question3_plot():
    """
    Generate the plot for question 3
    """
    data_table = load_data_table(DATA_3108_URL)

    singleton_list = []
    for line in data_table:
        cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
        singleton_list.append(cluster)
    cluster_list = kmeans_clustering(singleton_list, 15, 5)
    plot_clusters(data_table, cluster_list, True)


question3_plot()
