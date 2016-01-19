"""
Provided code for Application portion of Module 1

Imports physics citation graph

Code for Application question 1 & 2 of Module 1 
"""

# general imports
import urllib2
from matplotlib import pyplot as plt
from project1 import in_degree_distribution
from random import uniform

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def normalization(distribution):
    """
    normalize the in-degree distribution (summation is 1)

    Parameters
    ----------
    distribution: dict
    a dictionary representing the in-degree distribution

    Returns
    -------
    normalized: dict
    a dictionary representing the normalized in-degree distribution
    """
    summation = sum(distribution.values())
    normalized = {}
    for in_degree, dist_value in distribution.iteritems():
        normalized_value = float(dist_value) / summation
        normalized[in_degree] = normalized_value
    return normalized


def avg_outdegree(graph):
    """
    calculate the average out-degree for the given graph

    Parameters
    ----------
    graph: dict
    a dictionary representing a digraph

    Returns
    -------
    avg: float
    the average value of out-degree of the graph
    """
    summation = 0.0
    for node in graph:
        summation += len(graph[node])
    avg = summation / len(graph)
    return avg


def question1_plot():
    """
    Code for plot of question 1
    """
    citation_graph = load_graph(CITATION_URL)
    in_degree_dist = in_degree_distribution(citation_graph)
    normalized = normalization(in_degree_dist)
    plt.plot(normalized.keys(), normalized.values(), 'o', markersize=8)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Log of Normalized In-degree Distribution of Citation Graph')
    plt.xlabel('Log of Citations')
    plt.ylabel('Log of Normalized Distribution')
    plt.show()


def algorithm_ER(n, p):
    """
    Implementation of algorithm ER provided in Homework

    Parameters
    ----------
    n: int
    the number of nodes

    p: float:
    the probability of forming an edge

    Returns
    -------
    graph: dict
    a dictionary representing the graph
    """
    graph = {}
    for i in range(n):
        adjacency_list = []
        for j in range(n):
            if i != j:
                a = uniform(0, 1)
                if a < p:
                    adjacency_list.append(j)
        graph[i] = set(adjacency_list)
    return graph


def question2_plot():
    """
    Code for plot of question2
    """
    n = 1000
    probs = [0.2, 0.4, 0.6]
    legends = []
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Log Normalized In-degree Distribution '
              'for Different P based on 1000 Nodes')
    plt.xlabel('Log of Number of In-degrees')
    plt.ylabel('Log of Normalized Distribution')
    for p in probs:
        dist = in_degree_distribution(algorithm_ER(n, p))
        dist = normalization(dist)
        plt.plot(dist.keys(), dist.values(), 'o')
        legends.append('distribution of p=%s' % (p))
    plt.legend(legends, loc='upper left')
    plt.show()


if __name__ == '__main__':
    citation = load_graph(CITATION_URL)
    print avg_outdegree(citation)