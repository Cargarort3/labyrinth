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

    for _ in range(100):
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
