import numpy as np
from state import next_state, solved_state
from location import next_location, solved_location


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
                        print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                              expand_count, "\nSearch depth: ", limit, "\n")
                        return np.array(new_node[0])

            fringe = new_fringe
            explore_count += 1

        print("Could not find the answer")


    elif method == 'A*':
        fringe = [([], init_state, init_location, 0 + calculate_heuristic(init_location))]
        count = 0
        while True:
            count += 1
            print(count)

            target_node = fringe[0]
            for node in fringe:
                new_f = node[3]
                if target_node[3] > new_f:
                    target_node = node

            for i in range(1, 12 + 1):
                actions = list.copy(target_node[0])
                actions.append(i)
                new_location = next_location(target_node[2], i)
                new_node = (
                    actions, next_state(target_node[1], i), new_location,
                    len(actions) + calculate_heuristic(new_location))
                fringe.append(new_node)

                print("\n\ntarget_node:\n", target_node[0])


                if np.array_equal(new_node[1], solved_state()):
                    return np.array(new_node[0])

            fringe.remove(target_node)


    elif method == 'BiBFS':
        ...

    else:
        return []


def calculate_heuristic(location):
    target_location = solved_location()
    h = 0
    h += abs(int(location[0, 0, 0]) - int(target_location[0, 0, 0]))
    h += abs(int(location[0, 0, 1]) - int(target_location[0, 0, 1]))
    h += abs(int(location[0, 1, 0]) - int(target_location[0, 1, 0]))
    h += abs(int(location[0, 1, 1]) - int(target_location[0, 1, 1]))
    h += abs(int(location[1, 0, 0]) - int(target_location[1, 0, 0]))
    h += abs(int(location[1, 0, 1]) - int(target_location[1, 0, 1]))
    h += abs(int(location[1, 1, 0]) - int(target_location[1, 1, 0]))
    h += abs(int(location[1, 1, 1]) - int(target_location[1, 1, 1]))
    return h / 4


if __name__ == '__main__':
    a = solved_location()
    print(type(a))
    print(a[0, 0, 1])
    print(abs(a[0, 1, 0] - 5 - a[0, 0, 1]))
