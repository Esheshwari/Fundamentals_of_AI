import math

HUMAN= "O"
AI = "X"
EMPTY = " "
board = [EMPTY for _ in range(9)]

def print_board(board):
  """ 
  Print the board in a 3x3 grid format.

  """
  win_conditions = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
      
    ]

  for condition in win_conditions:
      if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
        return True
      return False

  def is_board_full(board):
    """ check is there are no empty spaces left """

    return EMPTY not in board

  def get_empty_spots(board):
    """ Return a list of indices where the board is empty """

    empty_spots = []
    for i, spot in enumerate(board):
      if spot == EMPTY:
        empty_spots.append(i)
      return empty_spots
