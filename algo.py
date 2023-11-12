import numpy as np
from state import next_state, solved_state
from location import next_location, solved_location
import heapq


def find_reverse_action(action):
    pre_action = (action + 6) % 12
    if pre_action == 0:
        pre_action = 12

    return pre_action


def resolve_actions(forward_actions, backward_actions):
    print("\n\nwhole actions:\n", forward_actions, backward_actions, "\n")
    for j in range(1, len(backward_actions) + 1):
        forward_actions.append(backward_actions[-1 * j])

    return np.array(forward_actions)


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
    # 4. you can use 'Set', 'Dictionary', 'OrderedD

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
        fringe = [(0 + calculate_heuristic(init_location), [], init_state, init_location)]
        explore_count = 0
        expand_count = 0
        while True:
            target_node = heapq.heappop(fringe)

            explore_count += 1
            for i in range(1, 12 + 1):
                actions = list.copy(target_node[1])
                actions.append(i)
                new_location = next_location(target_node[3], i)
                new_node = (
                    len(actions) + calculate_heuristic(new_location),
                    actions,
                    next_state(target_node[2], i),
                    new_location)

                expand_count += 1
                heapq.heappush(fringe, new_node)

                if np.array_equal(new_node[2], solved_state()):
                    print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                          expand_count, "\nSearch depth: ", len(new_node[1]), "\n")
                    return np.array(new_node[1])

        # fringe = [([], init_state, init_location, 0 + calculate_heuristic(init_location))]
        # explore_count = 0
        # expand_count = 0
        # while True:
        #     target_node = fringe[0]
        #     for node in fringe:
        #         new_f = node[3]
        #         if target_node[3] > new_f:
        #             target_node = node
        #
        #     explore_count += 1
        #     for i in range(1, 12 + 1):
        #         actions = list.copy(target_node[0])
        #         actions.append(i)
        #         new_location = next_location(target_node[2], i)
        #         new_node = (
        #             actions, next_state(target_node[1], i), new_location,
        #             len(actions) + calculate_heuristic(new_location))
        #
        #         expand_count += 1
        #         fringe.append(new_node)
        #
        #         if np.array_equal(new_node[1], solved_state()):
        #             print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
        #                   expand_count, "\nSearch depth: ", len(new_node[0]), "\n")
        #             return np.array(new_node[0])
        #
        #     fringe.remove(target_node)

    elif method == 'BiBFS':
        forward_fringe = {np.array_str(init_state): ([], init_state)}
        backward_fringe = {np.array_str(solved_state()): ([], solved_state())}

        new_forward_fringe = forward_fringe.copy()
        new_backward_fringe = backward_fringe.copy()

        for limit in range(1, 12):
            curr_forward_fringe = new_forward_fringe.copy()
            curr_backward_fringe = new_backward_fringe.copy()

            new_forward_fringe.clear()
            new_backward_fringe.clear()

            for state, node in curr_forward_fringe.items():
                for i in range(1, 12 + 1):
                    new_state = next_state(node[1], i)
                    new_key = np.array_str(new_state)

                    if new_key in forward_fringe:
                        continue

                    new_actions = list.copy(node[0])
                    new_actions.append(i)

                    new_forward_fringe[new_key] = (new_actions, new_state)

                    if np.array_equal(new_state, solved_state()):
                        print("find solution in straight forward")
                        return np.array(new_actions)
                    if new_key in backward_fringe:
                        print("find solution in forward")
                        return resolve_actions(new_actions, backward_fringe[new_key][0])

            for state, node in curr_backward_fringe.items():
                for i in range(1, 12 + 1):
                    pre_state = next_state(node[1], find_reverse_action(i))
                    new_key = np.array_str(pre_state)

                    if new_key in backward_fringe:
                        continue

                    new_actions = list.copy(node[0])
                    new_actions.append(i)

                    new_backward_fringe[new_key] = (new_actions, pre_state)

                    if new_key in forward_fringe:
                        print("find solution in backward")
                        return resolve_actions(forward_fringe[new_key][0], new_actions)

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
    a = [1, 5, 8]
    b = [8, 2, 12]
    print(resolve_actions(a, b))
#     1, 5, 8, 6, 8, 2
