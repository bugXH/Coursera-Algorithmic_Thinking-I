from UPATrial import UPATrial
from loadgraph import load_graph, NETWORK_URL, targeted_order
from itertools import combinations
from project2 import compute_resilience
from matplotlib import pyplot as plt
import random

"""
Code for Application questions of Module 2
"""


def er(num_nodes, p):
    """
    Takes the number of nodes and returns a dictionary corresponding
    to a complete directed graph with the specified number of nodes.
    A complete graph contains all possible edges subject to the
    restriction that self-loops are not allowed.

    The computer network has 1239 nodes and 3047 edges, p should be 0.004

    Parameters
    ----------
    num_nodes: int
    the number of nodes in the graph

    p: float
    the probability to add an edge

    Returns
    -------
    graph: dict
    a dictionary corresponding to the undirected graph
    """

    graph = {node: set() for node in range(num_nodes)}
    for node_i, node_j in combinations(range(num_nodes), 2):
        prob = random.uniform(0, 1)
        if prob < p:
            graph[node_i].add(node_j)
            graph[node_j].add(node_i)
    return graph


def upa(n, m):
    """
    Construct UPA graph

    Parameters
    ----------
    n: int
    final number of nodes

    m: int
    number of existing nodes

    The computer network has 1239 nodes and 3047 edges, m should be 5

    Returns
    -------
    graph: dict
    a dictionary representing a final undirected graph
    """
    graph = er(m, 1)
    upa_helper = UPATrial(m)
    # run m to n - 1 trials
    for new_node in range(m, n):
        added = upa_helper.run_trial(m)
        graph[new_node] = added
        for existed in added:
            graph[existed].add(new_node)
    return graph


def random_order(ugraph):
    """
    Takes a graph and returns a list of the nodes
    in the graph in some random order

    Parameters
    ----------
    ugraph: dict
    a dictionary representing the undirected graph

    Returns
    -------
    order: list
    a list of nodes in a random order
    """
    nodes = [node for node in ugraph.keys()]
    order = []
    while len(nodes) > 0:
        chosen_node = random.choice(nodes)
        order.append(chosen_node)
        nodes.remove(chosen_node)
    return order


def question1_plot():
    """
    plot for question 1
    """
    network_graph = load_graph(NETWORK_URL)
    p = 0.004
    m = 3
    er_graph = er(1239, 0.004)
    upa_graph = upa(1239, 3)

    graphs = [network_graph, er_graph, upa_graph]
    attack_orders = [random_order(graph) for graph in graphs]

    resiliences = [compute_resilience(graph, attack_order) for
                   graph, attack_order in zip(graphs, attack_orders)]

    removed_num = range(1239 + 1)
    for resil in resiliences:
        plt.plot(removed_num, resil)
    legend_text = ['Computer Network', 'ER Graph, p = %.3f' % (p),
                   'UPA Graph, m = %d' % (m)]
    plt.legend(legend_text, loc="upper right")
    plt.xlabel('the number of nodes removed')
    plt.ylabel('the size of the largest connect component')
    plt.title('Graph resiliences')
    plt.show()


if __name__ == '__main__':
    question1_plot()
