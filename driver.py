import argparse
import timeit
from collections import deque
from state import State
from heapq import heappush, heappop, heapify
import itertools
import random


def initial():
    mov = ['up','down', 'left', 'right']
    list = [0,1,2,3,4,5,6,7,8]
    i = 0 
    while(i<=21):
        zero_loc = list.index(0)
        res = random.choice(mov)
        if res == 'up':
            if zero_loc <= 2:
                print( "no up")
            else:
                list[zero_loc], list[zero_loc-3] = list[zero_loc-3], list[zero_loc]
        elif res == 'down':
            if zero_loc >= 6:
                print( "no down")
            else:
                list[zero_loc], list[zero_loc+3] = list[zero_loc+3], list[zero_loc]
        elif res == 'left':
            if (zero_loc == 0) or (zero_loc == 3) or (zero_loc == 6):
                print( "no left")
            else:
                list[zero_loc], list[zero_loc-1] = list[zero_loc-1], list[zero_loc]
        elif res == 'right':
            if (zero_loc == 2) or (zero_loc == 5) or (zero_loc == 8):
                print( "no right")
            else:
                list[zero_loc], list[zero_loc+1] = list[zero_loc+1], list[zero_loc]
        
        i+=1
  
    return list


goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_node = State
# initial_state = [8, 7, 6, 5, 4, 3, 2, 1, 0]
initial_state = initial()
board_len = 9
board_side = int(board_len ** 0.5)

nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

moves = list()
costs = set()

def init():
    random.shuffle(initial_state)
    if not solvable(initial_state):
        init()

def solvable(state):
    invcnt = inv_cnt(state)
    if invcnt % 2 == 0:
        return True
    return False

def inv_cnt(state):
    inv_count = 0; 
    for i in range(0,8,1):
        for j in range(i+1,9,1):
            if state[j] and state[i] and state[i] > state[j]:
                  inv_count = inv_count + 1
    return inv_count

def bfs(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored, queue = set(), deque([State(start_state, None, None, 0, 0, 0)])

    while queue:

        node = queue.popleft()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return queue

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(queue) > max_frontier_size:
            max_frontier_size = len(queue)

def ast(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored, heap, heap_entry, counter = set(), list(), {}, itertools.count()

    key = h(start_state)

    root = State(start_state, None, None, 0, 0, key)

    entry = (key, 0, root)

    heappush(heap, entry)

    heap_entry[root.map] = entry

    while heap:

        node = heappop(heap)

        explored.add(node[2].map)

        if node[2].state == goal_state:
            goal_node = node[2]
            return heap

        neighbors = expand(node[2])

        for neighbor in neighbors:

            neighbor.key = neighbor.cost + h(neighbor.state)

            entry = (neighbor.key, neighbor.move, neighbor)

            if neighbor.map not in explored:

                heappush(heap, entry)

                explored.add(neighbor.map)

                heap_entry[neighbor.map] = entry

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

            elif neighbor.map in heap_entry and neighbor.key < heap_entry[neighbor.map][2].key:

                hindex = heap.index((heap_entry[neighbor.map][2].key,
                                     heap_entry[neighbor.map][2].move,
                                     heap_entry[neighbor.map][2]))

                heap[int(hindex)] = entry

                heap_entry[neighbor.map] = entry

                heapify(heap)

        if len(heap) > max_frontier_size:
            max_frontier_size = len(heap)


def ida(start_state):

    global costs

    threshold = h(start_state)

    while 1:
        response = dls_mod(start_state, threshold)

        if type(response) is list:
            return response
            break

        threshold = response

        costs = set()


def dls_mod(start_state, threshold):

    global max_frontier_size, goal_node, max_search_depth, costs

    explored, stack = set(), list([State(start_state, None, None, 0, 0, threshold)])

    while stack:

        node = stack.pop()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        if node.key > threshold:
            costs.add(node.key)

        if node.depth < threshold:

            neighbors = reversed(expand(node))

            for neighbor in neighbors:
                if neighbor.map not in explored:

                    neighbor.key = neighbor.cost + h(neighbor.state)
                    stack.append(neighbor)
                    explored.add(neighbor.map)

                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

    return min(costs)


def expand(node):

    global nodes_expanded
    nodes_expanded += 1

    neighbors = list()

    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes


def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_len - board_side, board_len):

            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_len, board_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_len, board_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def h(state):

    return sum(abs(b % board_side - g % board_side) + abs(b//board_side - g//board_side)
               for b, g in ((state.index(i), goal_state.index(i)) for i in range(1, board_len)))


def backtrace():

    moves = []

    current_node = goal_node

    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'up'
        elif current_node.move == 2:
            movement = 'down'
        elif current_node.move == 3:
            movement = 'left'
        else:
            movement = 'right'

        moves.insert(0, movement)
        current_node = current_node.parent
    print moves
    return moves