def dfs_maze_3d(maze, start, goal):
    """
    3D DFS Maze Solver
    Modified version of 2D DFS.
    """

    # ---------------------------
    # CHANGE 1: Added depth (3rd dimension)
    # 2D had: rows, cols
    # 3D now has: depth, rows, cols
    # ---------------------------
    depth = len(maze)          # Number of layers (z-axis)
    rows = len(maze[0])        # Rows (x-axis)
    cols = len(maze[0][0])     # Columns (y-axis)

    # ---------------------------
    # CHANGE 2: Position now (z, x, y) instead of (x, y)
    # ---------------------------
    stack = [(start, [start])]
    visited = set()

    while stack:
        # CHANGE 3: Extract 3 coordinates instead of 2
        (z, x, y), path = stack.pop()

        # Goal check updated for 3D
        if (z, x, y) == goal:
            return path

        if (z, x, y) not in visited:
            visited.add((z, x, y))

            # ---------------------------
            # CHANGE 4: 6 possible directions instead of 4
            # 2D moves → up, down, left, right (4)
            # 3D moves → add layer up & layer down (6)
            # ---------------------------
            moves = [
                (1, 0, 0),    # Move to next layer (z+1)
                (-1, 0, 0),   # Move to previous layer (z-1)
                (0, 1, 0),    # Move forward (x+1)
                (0, -1, 0),   # Move backward (x-1)
                (0, 0, 1),    # Move right (y+1)
                (0, 0, -1)    # Move left (y-1)
            ]

            for dz, dx, dy in moves:
                # CHANGE 5: Calculate new 3D position
                nz, nx, ny = z + dz, x + dx, y + dy

                # ---------------------------
                # CHANGE 6: Boundary check updated for 3D
                # Added depth check (0 <= nz < depth)
                # ---------------------------
                if (0 <= nz < depth and
                    0 <= nx < rows and
                    0 <= ny < cols and
                    maze[nz][nx][ny] == 0 and
                    (nz, nx, ny) not in visited):

                    # DFS logic remains SAME:
                    # Push new state with updated path
                    stack.append(((nz, nx, ny), path + [(nz, nx, ny)]))

    return None


# --------------------------
# TEST CASE 1 (Solvable)
# --------------------------
maze3d = [
    [  # Layer 0
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0]
    ],
    [  # Layer 1
        [0, 1, 0],
        [0, 0, 0],
        [1, 1, 0]
    ]
]

start = (0, 0, 0)
goal = (1, 2, 2)

solution = dfs_maze_3d(maze3d, start, goal)
print("3D Maze Solution:", solution)


# --------------------------
# TEST CASE 2 (No Path)
# --------------------------
maze3d_no_path = [
    [
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
    ]
]

start2 = (0, 0, 0)
goal2 = (1, 2, 2)

solution2 = dfs_maze_3d(maze3d_no_path, start2, goal2)
print("3D Maze No Path Solution:", solution2)
