"""
Coursera Algorithmic Thinking part 1
Module 1 Project 1 - Degree distributions for graphs

Content:
Representing directed graphs and computing degree distributions

"""

# Define three constants of graphs
EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes and returns a dictionary corresponding
    to a complete directed graph with the specified number of nodes.
    A complete graph contains all possible edges subject to the
    restriction that self-loops are not allowed.
    
    Parameters
    ----------
    num_nodes: int
    the number of nodes in the graph

    Returns
    -------
    graph: dict
    a dictionary corresponding to the complete graph
    """

    graph = {}
    for curr_node in range(num_nodes):
        adjacenty_list = [node for node in range(num_nodes)
                          if node != curr_node]
        graph[curr_node] = set(adjacenty_list)
    return graph


def compute_in_degrees(digraph):
    """
    Takes a directed graph and computes
    the in-degrees for the nodes in the graph.

    Parameters
    ----------
    digraph: dict
    a dictionary representing a directed graph

    Returns
    -------
    in_degrees: dict
    a dictionary with the same set of keys as digraph
    whose corresponding values are the number of edges
    whose head matches a particular node.
    """

    in_degrees = dict.fromkeys(digraph)
    for node in in_degrees:
        in_degrees[node] = 0
    for node in digraph:
        for head in list(digraph[node]):
            in_degrees[head] += 1
    return in_degrees


def in_degree_distribution(digraph):
    """
    Takes a directed graph and computes the unnormalized
    distribution of the in-degrees of the graph.

    Parameters
    ----------
    digraph: dict
    a dictionary representing a directed graph

    Returns
    -------
    in_degree_dist: dict
    a dictionary whose keys correspond to in-degrees of nodes in the graph.
    The value associated with each particular in-degree is the number of nodes
    with that in-degree. In-degrees with no corresponding nodes in the graph
    are not included.
    """

    computed_degrees = compute_in_degrees(digraph)
    in_degree_dist = {}
    for node in computed_degrees:
        in_degree = computed_degrees[node]
        if in_degree in in_degree_dist:
            in_degree_dist[in_degree] += 1
        else:
            in_degree_dist[in_degree] = 1
    return in_degree_dist

