"""
Implementation for application 3
"""
from project3 import (fast_closest_pair, slow_closest_pair,
                      hierarchical_clustering, kmeans_clustering)
from matplotlib import pyplot as plt
from random import randint
from alg_cluster import Cluster
from alg_project3_viz import (load_data_table, DATA_3108_URL,
                              DATA_111_URL, DATA_290_URL, DATA_896_URL)
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


def question5_plot():
    """
    Generate the plot for question 5
    """
    data_table = load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
        singleton_list.append(cluster)
    cluster_list = hierarchical_clustering(singleton_list, 9)
    plot_clusters(data_table, cluster_list, True)


def question6_plot():
    """
    Generate the plot for question 6
    """
    data_table = load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
        singleton_list.append(cluster)
    cluster_list = kmeans_clustering(singleton_list, 9, 5)
    plot_clusters(data_table, cluster_list, True)


def compute_distortion(cluster_list, data_table):
    """
    Implementation of compute_distortion for question 7

    Parameter
    ---------
    cluster_list: list
    the list of clustering results

    data_table: list of sets
    the data table


    Returns
    -------
    distortion: int
    the summation of distortion
    """
    errlist = []
    for cluster in cluster_list:
        errlist.append(cluster.cluster_error(data_table))
    distortion = sum(errlist)
    # print distortion
    return distortion


def question7(url, num_clusters):
    data_table = load_data_table(url)
    singleton_list = []
    for line in data_table:
        cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
        singleton_list.append(cluster)

    # cluster_list = hierarchical_clustering(singleton_list, num_clusters)
    cluster_list = kmeans_clustering(singleton_list, num_clusters, 5)
    print compute_distortion(cluster_list, data_table)


def question10_plot():
    urls = [DATA_111_URL, DATA_290_URL, DATA_896_URL]
    sizes = range(6, 21)
    data_sizes = [111, 290, 896]
    for url, data_size in zip(urls, data_sizes):
        data_table = load_data_table(url)
        singleton_list = []

        for line in data_table:
            cluster = Cluster(set([line[0]]), line[1],
                              line[2], line[3], line[4])
            singleton_list.append(cluster)

        # hierarchical clustering
        clusters = singleton_list
        distortion_hier = []
        while len(clusters) > 6:
            pair = fast_closest_pair(clusters)
            idx1, idx2 = pair[1], pair[2]
            clusters[idx1].merge_clusters(clusters[idx2])
            clusters.pop(idx2)
            if len(clusters) in sizes:
                distortion = compute_distortion(clusters, data_table)
                distortion_hier.append(distortion)

        # k-means
        distortion_kmeans = []
        for size in sizes:
            singleton_list = []
            for line in data_table:
                cluster = Cluster(set([line[0]]), line[1],
                                  line[2], line[3], line[4])
                singleton_list.append(cluster)
            c = kmeans_clustering(singleton_list, size, 5)
            distortion = compute_distortion(c, data_table)
            distortion_kmeans.append(distortion)
        plt.plot(sizes, distortion_hier[::-1])
        plt.plot(sizes, distortion_kmeans)
        legend_texts = ['hierarchical clustering',
                        'k-means clustering (5 iterations)']
        plt.legend(legend_texts, loc='upper right')
        plt.title('Distortion with %d county data' % (data_size))
        plt.xlabel('Size of Clusters')
        plt.ylabel('Distortion')
        plt.show()


if __name__ == '__main__':
    question10_plot()