"""
Coursera Algorithmic Thinking Project2
Implementation of BFS-Visited Algorithm
"""

from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph and the start node and returns
    the set consisting of all nodes that are visited by a BFS
    that starts at start node.

    Parameters
    ----------
    ugraph: dict
    a dictionary that represents an undirected graph

    start_node: int
    the index of the start node

    Returns
    -------
    visited: set
    a set of all visited nodes
    """
    visited = []
    visited.append(start_node)
    bigq = deque([])
    bigq.append(start_node)
    while len(bigq) > 0:
        nodej = bigq.popleft()
        for neighbor in ugraph[nodej]:
            if neighbor not in visited:
                visited.append(neighbor)
                bigq.append(neighbor)
    return set(visited)


def cc_visited(ugraph):
    """
    Takes the undirected graph and returns a list of sets,
    where each set consists of all the nodes (and nothing else)
    in a connected component, and there is exactly one set in the
    list for each connected component in ugraph and nothing else.

    Parameters
    ----------
    ugraph: dict
    a dictionary representing the undirected graph

    Returns
    -------
    connected: list of sets
    a list of sets containing connected components
    """
    remaining_nodes = set(ugraph.keys())
    connected = []
    while len(remaining_nodes) > 0:
        nodei = list(remaining_nodes)[0]
        visited = set(bfs_visited(ugraph, nodei))
        connected.append(visited)
        remaining_nodes = remaining_nodes.difference(visited)
    return connected


def largest_cc_size(ugraph):
    """
    Takes the undirected graph and returns the size (an integer)
    of the largest connected component in ugraph

    Parameters
    ----------
    ugraph: dict
    a dictionary representing the undirected graph

    Returns
    -------
    largest_size: int
    the size of the largest connected component in the graph
    """
    connected = cc_visited(ugraph)
    largest_size = 0
    for component in connected:
        if len(component) > largest_size:
            largest_size = len(component)
    return largest_size


def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph, a list of nodes and iterates
    through the nodes in attack_order. For each node in the list,
    the function removes the given node and its edges from the graph
    and then computes the size of the largest connected component
    for the resulting graph.

    Parameters
    ----------
    ugraph: dict
    a dictionary that represents an undirected graph

    attack_order: list
    a list representing the order of nodes to be removed

    Returns
    -------
    resilience: list
    a list whose k + 1 th entry is the size of the largest connected
    component in the graph after the removal of the first k nodes in
    attack order. The first entry (indexed by zero) is the size
    of the largest connected component in the original graph.
    """
    resilience = []
    resilience.append(largest_cc_size(ugraph))
    for node in attack_order:
        ugraph.pop(node)
        for remainingnode in ugraph:
            if node in ugraph[remainingnode]:
                ugraph[remainingnode].remove(node)
        resilience.append(largest_cc_size(ugraph))
    return resilience
