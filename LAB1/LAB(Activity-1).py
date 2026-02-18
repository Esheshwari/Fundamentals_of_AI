def dfs_maze(maze, start, goal):
    """
    Finds a path through a maze using Depth-First Search (DFS)

    Args:
        maze: 2D list where 0 = open cell, 1 = wall
        start: (row, col) tuple for the starting position
        goal: (row, col) tuple for the target position

    Returns:
        A list of (row, col) tuples representing the path
        from start to goal, or None if no path exists.
    """

    # Total rows and columns in maze
    rows = len(maze)
    cols = len(maze[0])

    # Stack stores tuples: (current_position, path_taken_to_reach_here)
    stack = [(start, [start])]

    # Set to track visited cells
    visited = set()

    # Continue until stack becomes empty
    while stack:
        # Pop the last inserted element (LIFO)
        (x, y), path = stack.pop()

        # If goal is reached, return the path
        if (x, y) == goal:
            return path

        # Process only if cell not already visited
        if (x, y) not in visited:
            visited.add((x, y))

            # Possible moves: up, down, left, right
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dx, dy in moves:
                nx, ny = x + dx, y + dy

                # Check:
                # 1. Inside maze boundaries
                # 2. Not a wall
                # 3. Not visited
                if (0 <= nx < rows and
                    0 <= ny < cols and
                    maze[nx][ny] != 1 and
                    (nx, ny) not in visited):

                    # Push new position and updated path
                    stack.append(((nx, ny), path + [(nx, ny)]))

    # If stack empties and goal not found
    return None


# --------------------------
# MAZE TEST CASE 1 (Solvable)
# --------------------------
maze1 = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0]
]

start1 = (0, 0)
goal1 = (3, 3)

solution1 = dfs_maze(maze1, start1, goal1)

print("Maze 1 Solution:", solution1)


# --------------------------
# MAZE TEST CASE 2 (No Path)
# --------------------------
maze2 = [
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 0, 0]
]

start2 = (0, 0)
goal2 = (3, 3)

solution2 = dfs_maze(maze2, start2, goal2)

print("Maze 2 Solution:", solution2)


# --------------------------
# MAZE TEST CASE 3 (Larger Maze)
# --------------------------
maze3 = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]
]

start3 = (0, 0)
goal3 = (4, 4)

solution3 = dfs_maze(maze3, start3, goal3)

print("Maze 3 Solution:", solution3)


"""
-----------------------------------------------------
STEPS OF DFS ALGORITHM USED HERE
-----------------------------------------------------

1. Initialize a stack and push the starting position
   along with the path containing only the start.

2. Create a set to store visited nodes.

3. While the stack is not empty:
    a. Pop the top element (LIFO).
    b. If it is the goal, return the path.
    c. If not visited:
        i. Mark as visited.
        ii. Explore all valid neighboring cells
            (up, down, left, right).
        iii. Push each valid neighbor onto the stack
             with the updated path.

4. If stack becomes empty and goal not found,
   return None (no path exists).

-----------------------------------------------------
WHY DFS WORKS HERE
-----------------------------------------------------

- DFS explores as far as possible along one branch
  before backtracking.
- Uses stack (LIFO).
- Does not guarantee shortest path.
- Uses backtracking naturally via stack pop().
"""
