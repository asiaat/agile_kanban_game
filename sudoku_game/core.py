"""Sudoku Engine - Core logic for generating and solving Sudoku puzzles."""

import math
import random


class Sudoku:
    """Sudoku puzzle engine with backtracking solver."""

    def __init__(self, n=3):
        """
        n: Size of inner square (e.g., n=3 means 3x3 inner squares and 9x9 board).
        """
        self.n = n
        self.size = n * n
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def set_board(self, new_board):
        """Set custom board state."""
        if len(new_board) == self.size and len(new_board[0]) == self.size:
            self.board = new_board
        else:
            raise ValueError(f"Board must be {self.size}x{self.size}")

    def print_board(self):
        """Display the board with grid lines."""
        for i in range(self.size):
            if i % self.n == 0 and i != 0:
                print("-" * (self.size * 2 + self.n * 2))

            for j in range(self.size):
                if j % self.n == 0 and j != 0:
                    print("| ", end="")

                val = self.board[i][j]
                print(str(val if val != 0 else ".") + " ", end="")
            print()

    def is_valid(self, num, row, col):
        """Check if placing num at (row, col) is valid."""
        # Check row
        for j in range(self.size):
            if self.board[row][j] == num:
                return False

        # Check column
        for i in range(self.size):
            if self.board[i][col] == num:
                return False

        # Check n x n box
        box_row = (row // self.n) * self.n
        box_col = (col // self.n) * self.n

        for i in range(box_row, box_row + self.n):
            for j in range(box_col, box_col + self.n):
                if self.board[i][j] == num:
                    return False

        return True

    def find_empty(self):
        """Find next empty cell."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def copy(self):
        """Create a deep copy of the puzzle."""
        new_game = Sudoku(self.n)
        new_game.board = [row[:] for row in self.board]
        return new_game

    def solve(self):
        """Solve using backtracking algorithm."""
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty

        # Try numbers in random order for variety
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)

        for num in nums:
            if self.is_valid(num, row, col):
                self.board[row][col] = num

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

    def is_solved(self):
        """Check if puzzle is solved."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False

        # Verify all numbers are valid
        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                self.board[i][j] = 0
                if not self.is_valid(num, i, j):
                    self.board[i][j] = num
                    return False
                self.board[i][j] = num

        return True


def generate_puzzle(n=3, difficulty=40):
    """
    Generate a new Sudoku puzzle.

    Args:
        n: Board size (n=3 for 9x9, n=2 for 4x4)
        difficulty: Number of cells to remove (more = harder)

    Returns:
        A tuple (puzzle, solution) as Sudoku objects
    """
    # Create solved board
    game = Sudoku(n)
    _fill_diagonal(game)

    if game.solve():
        # Create puzzle by removing cells
        puzzle = game.copy()
        cells_removed = 0

        while cells_removed < difficulty:
            i = random.randint(0, game.size - 1)
            j = random.randint(0, game.size - 1)

            if puzzle.board[i][j] != 0:
                puzzle.board[i][j] = 0
                cells_removed += 1

        return puzzle, game

    raise RuntimeError("Failed to generate puzzle")


def _fill_diagonal(game):
    """Fill diagonal boxes (independent of each other)."""
    for i in range(0, game.size, game.n):
        filled = 0
        nums = list(range(1, game.size + 1))
        random.shuffle(nums)

        for j in range(game.n):
            for k in range(game.n):
                if filled < len(nums):
                    game.board[i + j][i + k] = nums[filled]
                    filled += 1