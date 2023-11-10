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
        expand_count = 0
        explore_count = 0
        fringe = [([], init_state)]
        for limit in range(1, 10):
            new_fringe = []
            for node in fringe:
                for i in range(1, 12 + 1):
                    actions = list.copy(node[0])
                    actions.append(i)
                    new_node = (actions, next_state(node[1], i))
                    new_fringe.append(new_node)
                    expand_count += 1

                    if np.array_equal(new_node[1], solved_state()):
                        print("\n", "Number of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ", expand_count, "\nSearch depth: ", limit, "\n")
                        return np.array(new_node[0])

                    # if 11 == actions[0] and 7 in actions and 9 in actions and 1 in actions and 6 in actions:
                    #     print("\nnode:\n", node, "\nactions:\n", actions, "\nnew_node:\n", new_node)
            fringe = new_fringe
            explore_count += 1
        # second = next_state(init_state, 11)
        # third = next_state(second, 7)
        # fourth = next_state(third, 9)
        # fifth = next_state(fourth, 1)
        # sixth = next_state(fifth, 6)
        # print(np.array_equal(sixth, solved_state()), "\n\n")
        # print("\n\n", sixth)
        # print("\n\n", solved_state())
        print("Could not find the answer")


    elif method == 'A*':
        ...

    elif method == 'BiBFS':
        ...

    else:
        return []


if __name__ == '__main__':
    a = []
    b = list.copy(a)
    b.append(1)
    print(a)
    print(b)
