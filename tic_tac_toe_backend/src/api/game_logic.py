"""
Tic Tac Toe game rules and logic, pure functions for board/move validation.
"""

from typing import Optional, List


WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
    [0, 4, 8], [2, 4, 6]              # diagonals
]


# PUBLIC_INTERFACE
def check_winner(board: List[str]) -> Optional[str]:
    """
    Return 'X', 'O' if there is a winner, or None.
    """
    for combo in WIN_COMBINATIONS:
        vals = [board[i] for i in combo]
        if vals[0] in ("X", "O") and all(val == vals[0] for val in vals):
            return vals[0]
    return None


# PUBLIC_INTERFACE
def check_draw(board: List[str]) -> bool:
    """
    Returns True if board is full and there is no winner.
    """
    return all(cell in ("X", "O") for cell in board) and check_winner(board) is None


# PUBLIC_INTERFACE
def apply_move(board: List[str], position: int, player: str) -> List[str]:
    """
    Returns a new board state after the move.
    Raises ValueError if the cell is not empty.
    """
    if board[position] in ("X", "O"):
        raise ValueError("Cell already occupied")
    new_board = board.copy()
    new_board[position] = player
    return new_board


# PUBLIC_INTERFACE
def validate_player_turn(current_player: str, move_player: str):
    """
    Verifies the move is made by the correct player.
    """
    if move_player != current_player:
        raise ValueError(f"It is {current_player}'s turn.")


# PUBLIC_INTERFACE
def next_player(current_player: str) -> str:
    return "O" if current_player == "X" else "X"
