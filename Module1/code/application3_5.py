"""
Code for Application question 3 - 5 of Module 1
"""

from DPATrial import DPATrial
from project1 import make_complete_graph, in_degree_distribution
from application1_2 import normalization, load_graph, CITATION_URL
from matplotlib import pyplot as plt


def dpa(n, m):
    """
    Implementation of DPA algorithm

    Parameters
    ----------
    n: int
    final number of nodes

    m: int
    number of existing nodes

    Returns
    -------
    graph: dict
    a dictionary representing a final directed graph
    """
    graph = make_complete_graph(m)
    dpa_helper = DPATrial(m)
    # run m to n - 1 trials
    for new_node in range(m, n):
        graph[new_node] = dpa_helper.run_trial(m)
    return graph


def question4_plot(n, m):
    """
    Code for plot of question 4

    Parameters
    ----------
    n: int
    input for dpa()

    m: int
    input for dpa()
    """
    in_degree_dist = in_degree_distribution(dpa(n, m))
    normalized_dist = normalization(in_degree_dist)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Log Normalized In-degrees Distribution of DPA Graph')
    plt.xlabel('Log of Number of In-degrees')
    plt.ylabel('Log of Normalized Distribution')
    plt.plot(normalized_dist.keys(), normalized_dist.values(),
             'ro', markersize=8)

    # compare with the citation graph
    
    # citation = load_graph(CITATION_URL)
    # citation_dist = normalization(in_degree_distribution(citation))
    # plt.plot(citation_dist.keys(), citation_dist.values(),
    #          'bo', markersize=8)
    # plt.show()


if __name__ == '__main__':
    question4_plot(27770, 13)