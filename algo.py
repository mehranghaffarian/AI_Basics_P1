import numpy as np
from state import next_state, solved_state
from location import next_location


def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.
 
    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.
 
    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .++
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == 'Random':
        return list(np.random.randint(1, 12 + 1, 10))

    elif method == 'IDS-DFS':
        fringe = [([], init_state)]
        for limit in range(1, 10):
            new_nodes = []
            for node in fringe:
                if np.array_equal(node[1], solved_state()):
                    return np.array(node[0])
                for i in range(1, 12 + 1):
                    print("\n\n", fringe, "\n\n")
                    t = (node[0].append(i), next_state(node[1], i))
                    new_nodes.append(t)
            fringe = new_nodes
        return np.array([])


    elif method == 'A*':
        ...

    elif method == 'BiBFS':
        ...

    else:
        return []
