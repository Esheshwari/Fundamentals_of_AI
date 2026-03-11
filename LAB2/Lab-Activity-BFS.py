from collections import deque

def bfs_maze(maze, start, goal):
    """
    Finds the shortest path through a maze using BFS.

    Key difference from DFS:
    - DFS uses a stack (LIFO)
    - BFS uses a queue (FIFO)
    - Because BFS explores level by level,
      it guarantees the shortest path.
    """

    # Maze dimensions
    rows = len(maze)
    cols = len(maze[0])

    # Track visited cells
    visited = set()
    visited.add(start)

    # Queue stores (position, path_so_far)
    queue = deque([(start, [start])])

    while queue:
        (x, y), path = queue.popleft()

        # Goal check
        if (x, y) == goal:
            return path

        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            # Check boundaries, wall, and visited
            if (0 <= nx < rows and
                0 <= ny < cols and
                maze[nx][ny] != 1 and
                (nx, ny) not in visited):

                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    # No path found
    return None


# -------------------------
# TEST CASE
# -------------------------
maze = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0]
]

start = (0, 0)
goal = (3, 3)

solution = bfs_maze(maze, start, goal)
print("Shortest Path using BFS:", solution)
