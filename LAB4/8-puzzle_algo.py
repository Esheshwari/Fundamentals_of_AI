import heapq

# --------------------------
# PUZZLE STATE CLASS
# --------------------------
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board        # Current board
        self.parent = parent      # Parent state
        self.move = move          # Move taken
        self.depth = depth        # g(n)
        self.cost = cost          # f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.cost < other.cost


# --------------------------
# PRINT BOARD FUNCTION
# --------------------------
def print_board(board):
    print("+---+---+---+")
    for i in range(0, 9, 3):
        row = "|"
        for j in range(3):
            val = board[i + j]
            if val == 0:
                row += "   |"
            else:
                row += f" {val} |"
        print(row)
        print("+---+---+---+")


# --------------------------
# GOAL STATE
# --------------------------
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Moves: position changes
moves = {
    "U": -3,
    "D": 3,
    "L": -1,
    "R": 1,
}


# --------------------------
# HEURISTIC FUNCTION
# Manhattan Distance
# --------------------------
def heuristic(board):
    distance = 0
    for i in range(9):
        if board[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(board[i] - 1, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


# --------------------------
# MOVE TILE FUNCTION
# --------------------------
def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]

    # Swap blank and tile
    new_board[blank_pos], new_board[new_blank_pos] = (
        new_board[new_blank_pos],
        new_board[blank_pos],
    )

    return new_board


# --------------------------
# A* ALGORITHM
# --------------------------
def a_star(start_state):
    open_list = []
    closed_list = set()

    start_node = PuzzleState(
        start_state,
        None,
        None,
        0,
        heuristic(start_state)
    )

    heapq.heappush(open_list, start_node)

    while open_list:
        current_state = heapq.heappop(open_list)

        # Goal check
        if current_state.board == goal_state:
            return current_state

        closed_list.add(tuple(current_state.board))

        blank_pos = current_state.board.index(0)

        for move in moves:
            # Invalid moves
            if move == "U" and blank_pos < 3:
                continue
            if move == "D" and blank_pos > 5:
                continue
            if move == "L" and blank_pos % 3 == 0:
                continue
            if move == "R" and blank_pos % 3 == 2:
                continue

            new_board = move_tile(current_state.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue

            new_state = PuzzleState(
                new_board,
                current_state,
                move,
                current_state.depth + 1,
                current_state.depth + 1 + heuristic(new_board)
            )

            heapq.heappush(open_list, new_state)

    return None


# --------------------------
# PRINT SOLUTION PATH
# --------------------------
def print_solution(solution):
    path = []
    current = solution

    while current:
        path.append(current)
        current = current.parent

    path.reverse()

    for step in path:
        print(f"Move: {step.move}")
        print_board(step.board)


# --------------------------
# MAIN EXECUTION
# --------------------------
initial_state = [1, 2, 3, 4, 0, 5, 7, 8, 6]

solution = a_star(initial_state)

if solution:
    print("✅ Solution Found!\n")
    print_solution(solution)
else:
    print("❌ No solution exists.")
