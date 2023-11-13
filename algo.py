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

    explore_count = 0
    expand_count = 0

    if method == 'Random':
        return list(np.random.randint(1, 12 + 1, 10))

    elif method == 'IDS-DFS':
        fringe = [([], init_state)]
        for limit in range(1, 10):
            new_fringe = []
            for node in fringe:
                explore_count += 1
                for i in range(1, 12 + 1):
                    expand_count += 1

                    new_state = next_state(node[1], i)
                    actions = list.copy(node[0])
                    actions.append(i)
                    new_node = (actions, new_state)

                    new_fringe.append(new_node)

                    if np.array_equal(new_node[1], solved_state()):
                        print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                              expand_count, "\nSearch depth: ", limit, "\n")
                        return np.array(new_node[0])
            fringe = new_fringe

        print("Could not find the answer")

    elif method == 'A*':
        expanded_states = {}
        fringe = [(0 + calculate_heuristic(init_location), [], init_state, init_location)]

        while True:
            target_node = heapq.heappop(fringe)

            explore_count += 1
            for i in range(1, 12 + 1):
                new_state = next_state(target_node[2], i)
                state_str = np.array_str(new_state)

                expand_count += 1

                if state_str in expanded_states:
                    continue

                actions = list.copy(target_node[1])
                actions.append(i)
                new_location = next_location(target_node[3], i)
                new_node = (
                    len(actions) + calculate_heuristic(new_location),
                    actions,
                    new_state,
                    new_location)

                heapq.heappush(fringe, new_node)

                if np.array_equal(new_node[2], solved_state()):
                    print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                          expand_count, "\nSearch depth: ", len(new_node[1]), "\n")
                    return np.array(new_node[1])

            expanded_states[np.array_str(target_node[2])] = True

    elif method == 'BiBFS':
        forward_fringe = {np.array_str(init_state): ([], init_state)}
        backward_fringe = {np.array_str(solved_state()): ([], solved_state())}

        new_forward_fringe = forward_fringe.copy()
        new_backward_fringe = backward_fringe.copy()

        while True:
            curr_forward_fringe = new_forward_fringe.copy()
            curr_backward_fringe = new_backward_fringe.copy()

            new_forward_fringe.clear()
            new_backward_fringe.clear()

            explore_count += 1
            for state, node in curr_forward_fringe.items():
                for i in range(1, 12 + 1):
                    expand_count += 1

                    new_state = next_state(node[1], i)
                    new_key = np.array_str(new_state)

                    if new_key in forward_fringe:
                        continue

                    new_actions = list.copy(node[0])
                    new_actions.append(i)

                    new_forward_fringe[new_key] = (new_actions, new_state)
                    forward_fringe[new_key] = (new_actions, new_state)

                    if np.array_equal(new_state, solved_state()):
                        print("find solution in straight forward")
                        print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                              expand_count, "\nSearch depth: ", len(new_actions), "\n")
                        return np.array(new_actions)
                    if new_key in backward_fringe:
                        whole_actions = resolve_actions(new_actions, backward_fringe[new_key][0])
                        print("find solution in forward")
                        print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                              expand_count, "\nSearch depth: ", len(whole_actions), "\n")
                        return whole_actions

            explore_count += 1
            for state, node in curr_backward_fringe.items():
                for i in range(1, 12 + 1):
                    expand_count += 1

                    pre_state = next_state(node[1], find_reverse_action(i))
                    new_key = np.array_str(pre_state)

                    if new_key in backward_fringe:
                        continue

                    new_actions = list.copy(node[0])
                    new_actions.append(i)

                    new_backward_fringe[new_key] = (new_actions, pre_state)
                    backward_fringe[new_key] = (new_actions, pre_state)

                    if new_key in forward_fringe:
                        whole_actions = resolve_actions(forward_fringe[new_key][0], new_actions)
                        print("find solution in backward")
                        print("\nNumber of explored nodes: ", explore_count, "\nNumber of expanded Nodes: ",
                              expand_count, "\nSearch depth: ", len(whole_actions), "\n")
                        return whole_actions

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
