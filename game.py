from random import randint, choice
import subprocess
import platform
import time
import numpy as np

HEIGHT = 20
WIDTH = 20

class MapGrid:
    def __init__(self, width, height, start, goal):
        self.width = width
        self.height = height
        self.walls = []
        self.start = start
        self.goal = goal
        self.player = self.start

    def move_player(self, d):
        x = self.player[0]
        y = self.player[1]
        pos = (x, y)

        if d == 'r' and x + 1 <= WIDTH - 1 and y <= HEIGHT - 1 and x + 1 >= 0 and y >= 0:
            pos = (x + 1, y)
        if d == 'l' and x - 1 <= WIDTH - 1 and y <= HEIGHT - 1 and x - 1 >= 0 and y >= 0:
            pos = (x - 1, y)
        if d == 'u' and x <= WIDTH - 1 and y - 1 <= HEIGHT - 1 and x >= 0 and y - 1 >= 0:
            pos = (x, y - 1)
        if d == 'd' and x <= WIDTH - 1 and y + 1 <= HEIGHT - 1 and x >= 0 and y + 1 >= 0:
            pos = (x, y + 1)

        if pos not in self.walls:
            self.player = pos

        if pos == self.goal:
            print("You made it to the end!")


def draw_grid(g, width=2):
    for y in range(g.height):
        for x in range(g.width):
            if (x, y) in g.walls:
                symbol = '#'
            elif (x, y) == g.player:
                symbol = '$'
            elif (x, y) == g.start:
                symbol = '<'
            elif (x, y) == g.goal:
                symbol = '>'
            else:
                symbol = '.'
            print("%%-%ds" % width % symbol, end="")
        print()


def get_walls(g: MapGrid, pct=.70) -> list:
        out = []
        for i in range(int(g.height*g.width*pct)//2):

            x = randint(1, g.width-2)
            y = randint(1, g.height-2)
            if (x, y) != g.start and (x, y) != g.goal:
                out.append((x, y))
                # out.append((x + choice([-1, 0, 1]), y + choice([-1, 0, 1])))
        return out


def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(.1)


def create_graph(g: MapGrid):
    res = {}
    for i in range(0, g.height):
        for j in range(0, g.width):
            res[(i, j)] = []
            if (i + 1, j) not in g.walls and i + 1 <= g.height - 1:
                res[(i, j)].append((i + 1, j))
            if (i - 1, j) not in g.walls and i - 1 >= 0:
                res[(i, j)].append((i - 1, j))
            if (i, j + 1) not in g.walls and j + 1 <= g.width - 1:
                res[(i, j)].append((i, j + 1))
            if (i, j - 1) not in g.walls and j - 1 >= 0:
                res[(i, j)].append((i, j - 1))
    return res

# def find_shortest_path(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     if start not in graph:
#         return None
#     shortest = None
#     for node in graph[start]:
#         if node not in path:
#             newpath = find_shortest_path(graph, node, end, path)
#             if newpath:
#                 if not shortest or len(newpath) < len(shortest):
#                     shortest = newpath
#     return shortest

def dijsktra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    iterations = 0
    while current_node != end:
        iterations += 1
        visited.add(current_node)
        destinations = graph[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            iterations += 1
            weight = 1 + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        iterations += 1
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    print('iterations Dejk: ', iterations)
    return path


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    iterations = 0
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        iterations = iterations + 1
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            iterations = iterations + 1
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                iterations = iterations + 1
                path.append(current.position)
                current = current.parent
            print('iterations A*: ', iterations)
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            iterations = iterations + 1

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            iterations = iterations + 1

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:

                iterations = iterations + 1
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    g = MapGrid(WIDTH, HEIGHT, (randint(0, HEIGHT-1), randint(0, WIDTH-1)), (randint(0, HEIGHT-1), randint(0, WIDTH-1)))
    g.walls = get_walls(g)
    draw_grid(g)
    graph = create_graph(g)
    path = dijsktra(graph, g.start, g.goal)
    path.pop(0)
    print("path_dej: ", path)
    maze = [[0 for x in range(g.width)] for y in range(g.height)]

    for wall in g.walls:
        maze[wall[0]][wall[1]] = 1

    start = g.start
    end = g.goal

    path_a = astar(maze, start, end)
    path_a.pop(0)
    print("path_a: ", path_a)


    moves = 0
    input()
    while g.player != g.goal and path:
        d = ''
        if g.player[0] < path[0][0]:
            d = 'r'
        if g.player[0] > path[0][0]:
            d = 'l'
        if g.player[1] > path[0][1]:
            d = 'u'
        if g.player[1] < path[0][1]:
            d = 'd'
        g.move_player(d)
        moves += 1
        print()
        path.pop(0)
        draw_grid(g)
        time.sleep(0.3)
        clear()

    print("You made it!")
    # print('moves:', moves)


if __name__ == '__main__':
    main()