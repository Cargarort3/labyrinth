from collections import deque
import random


def matrix_to_graph(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    graph = {}

    for i in range(1, rows+1):
        for j in range(1, columns+1):
            if matrix[i-1][j-1] == 0:
                node = (i, j)
                graph[node] = []

                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni = i + di
                    nj = j + dj
                    if 0 < ni <= rows and 0 < nj <= columns and matrix[ni-1][nj-1] == 0:
                        graph[node].append((ni, nj))

    return graph


def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                queue.append((neighbor, path + [neighbor]))

    return None


def dfs(graph, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                stack.append((neighbor, path + [neighbor]))

    return None


def random_walk(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    path = [start]
    current = start

    for _ in range(1000):
        for _ in range(rows*cols - 1):
            if current == end:
                return path

            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 < nx <= rows and 0 < ny <= cols:
                    if matrix[nx-1][ny-1] == 0 and (nx, ny) not in path:
                        neighbors.append((nx, ny))

            if not neighbors:
                path = [start]
                current = start
            else:
                next_node = random.choice(neighbors)
                path.append(next_node)
                current = next_node

    return None


def path_movements(path):
    moves = {
        (1, 0): "🡇",
        (-1, 0): "🡅",
        (0, 1): "🡆",
        (0, -1): "🡄"
    }
    res = []

    tuples = list(zip(path, path[1:]))
    for (i1, j1), (i2, j2) in tuples:
        res.append(((i1, j1), moves[(i2-i1, j2-j1)]))
    res.append((path[-1], "🚩"))

    return res


def generate_random_labyrinth(dimensions, start, end):
    n, m = dimensions
    x1, y1 = start[0] - 1, start[1] - 1
    x2, y2 = end[0] - 1, end[1] - 1

    lab = [[1] * m for _ in range(n)]
    lab[x1][y1] = 0
    lab[x2][y2] = 0
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def in_bounds(x, y):
        return 0 <= x < n and 0 <= y < m

    def dfs(x, y):
        lab[x][y] = 0
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2
            if in_bounds(nx, ny) and lab[nx][ny] == 1:
                lab[mx][my] = 0
                dfs(nx, ny)

    dfs(x1, y1)

    end1, end2 = x2, y2
    while bfs(matrix_to_graph(lab), (x1 + 1, y1 + 1), (x2 + 1, y2 + 1)) is None:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nx, ny = end1 + dx, end2 + dy
        if in_bounds(nx, ny):
            lab[nx][ny] = 0
            end1, end2 = nx, ny

    return lab
