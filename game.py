from random import randint, choice
import subprocess
import platform
import time
import numpy as np

HEIGHT = 11
WIDTH = 20

class MapGrid:
    def __init__(self, file='map.txt'): #width, height, start, goal
        self.score = 0
        self.walls = []
        self.ghosts = []
        self.goals = []
        self.empty = []
        with open('map.txt', 'r') as f:
            lines = f.readlines()
            map = [[x.strip()] for x in lines]
        for i, line in enumerate(map):
            for j in range(len(line[0])):
                if map[i][0][j] == '%':
                    self.walls.append((j, i))
                if map[i][0][j] == '.':
                    self.goals.append((j, i))
                if map[i][0][j] == 'G':
                    self.ghosts.append((j, i))
                    self.empty.append((j, i))
                if map[i][0][j] == ' ':
                    self.empty.append((j, i))
                if map[i][0][j] == 'P':
                    self.start = (j, i)
                    self.player = (j, i)
                    self.empty.append((j, i))
        self.width = j + 1
        self.height = i + 1
        print(self.ghosts)

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
            if (x, y) in self.goals:
                self.goals.remove((x, y))
                self.empty.append((x, y))
                self.score += 1

    def move_ghosts(self):
        for p, ghost in enumerate(self.ghosts):
            x = ghost[0]
            y = ghost[1]
            pos = (x, y)
            res = {}
            for i in range(0, self.width):
                for j in range(0, self.height):
                    res[(i, j)] = []
                    if (i + 1, j) not in self.walls and i + 1 < self.width:
                        res[(i, j)].append((i + 1, j))
                    if (i - 1, j) not in self.walls and i - 1 > -1:
                        res[(i, j)].append((i - 1, j))
                    if (i, j + 1) not in self.walls and j + 1 < self.height:
                        res[(i, j)].append((i, j + 1))
                    if (i, j - 1) not in self.walls and j - 1 > -1:
                        res[(i, j)].append((i, j - 1))
            graph = res
            move = dijsktra(graph, pos, self.player)[1]
            d = ''
            if ghost[0] < move[0]:
                d = 'r'
            if ghost[0] > move[0]:
                d = 'l'
            if ghost[1] > move[1]:
                d = 'u'
            if ghost[1] < move[1]:
                d = 'd'
            if randint(0, 1) == 0:
                d = d
            else:
                d = choice(['r', 'l', 'u', 'd'])
            if d == 'r' and x + 1 <= WIDTH - 1 and y <= HEIGHT - 1 and x + 1 >= 0 and y >= 0:
                pos = (x + 1, y)
            if d == 'l' and x - 1 <= WIDTH - 1 and y <= HEIGHT - 1 and x - 1 >= 0 and y >= 0:
                pos = (x - 1, y)
            if d == 'u' and x <= WIDTH - 1 and y - 1 <= HEIGHT - 1 and x >= 0 and y - 1 >= 0:
                pos = (x, y - 1)
            if d == 'd' and x <= WIDTH - 1 and y + 1 <= HEIGHT - 1 and x >= 0 and y + 1 >= 0:
                pos = (x, y + 1)

            if pos not in self.walls:
                self.ghosts[p] = pos

def draw_grid(g, width=2):
    for y in range(g.height):
        for x in range(g.width):
            if (x, y) in g.walls:
                symbol = '#'
            elif (x, y) == g.player:
                symbol = '$'
            elif (x, y) in g.ghosts:
                symbol = 'G'
            elif (x, y) in g.goals:
                symbol = '.'
            elif (x, y) in g.empty:
                symbol = ' '
            print("%%-%ds" % width % symbol, end="")
        print()


def clear():
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(.1)


def create_graph(g: MapGrid):
    res = {}
    dangerous = []
    for ghost in g.ghosts:
        dangerous.append(ghost)
        dangerous.append((ghost[0] - 1, ghost[1]))
        dangerous.append((ghost[0] + 1, ghost[1]))
        dangerous.append((ghost[0], ghost[1] - 1))
        dangerous.append((ghost[0], ghost[1] + 1))
    for i in range(0, g.width):
        for j in range(0, g.height):
            res[(i, j)] = []
            if (i + 1, j) not in g.walls and i + 1 < g.width and (i + 1, j) not in dangerous:#:
                res[(i, j)].append((i + 1, j))
            if (i - 1, j) not in g.walls and i - 1 > -1 and (i - 1, j) not in dangerous:#:
                res[(i, j)].append((i - 1, j))
            if (i, j + 1) not in g.walls and j + 1 < g.height and (i, j + 1) not in dangerous:#:
                res[(i, j)].append((i, j + 1))
            if (i, j - 1) not in g.walls and j - 1 > -1 and (i, j - 1) not in dangerous:#:
                res[(i, j)].append((i, j - 1))
    return res


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
    return path


def main():
    g = MapGrid()
    clear()
    draw_grid(g)
    while g.goals:
        # print('g.goals: ', g.goals)
        graph = create_graph(g)
        # print('graph: ', graph)
        target = choice(g.goals)
        # print('target: ', target)
        path = dijsktra(graph, g.player, target)
        # print('path: ', path)
        if path == "Route Not Possible":
            # print('AAAA')
            g.move_ghosts()
            clear()
            draw_grid(g)
            continue
        path = path[1:]
        # input()
        while path:
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
            g.move_ghosts()
            print()
            path = path[1:]
            clear()
            draw_grid(g)
            if g.player in g.ghosts:
                print('You lose!')
                print("Score: ", g.score)
                return
            time.sleep(0.1)
            graph = create_graph(g)
            path = dijsktra(graph, g.player, target)
            # print('path: ', path)
            if path == "Route Not Possible":
                # print('BBBB')
                target = choice(g.goals)
                graph = create_graph(g)
                path = dijsktra(graph, g.player, target)
                while path == "Route Not Possible":
                    g.move_ghosts()
                    clear()
                    draw_grid(g)
                    if g.player in g.ghosts:
                        print('You lose!')
                        print("Score: ", g.score)
                        return
                    graph = create_graph(g)
                    path = dijsktra(graph, g.player, target)
                continue
            path = path[1:]
            if target == g.player and len(g.goals) == 1:
                break
        if target == g.player and len(g.goals) == 1:
            break
    print("You won!")
    print("Score: ", g.score)

if __name__ == '__main__':
    main()