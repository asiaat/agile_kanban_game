# Sudoku Game Engine

A Python-based Sudoku puzzle generator and solver.

## Usage

```bash
# Generate new puzzle (9x9, medium difficulty)
python -m sudoku_game.cli --new

# Generate easy puzzle
python -m sudoku_game.cli --new --difficulty 20

# Generate hard puzzle
python -m sudoku_game.cli --new --difficulty 45

# Generate 4x4 board (16x16 puzzle)
python -m sudoku_game.cli --new --size 4

# Solve a puzzle
python -m sudoku_game.cli --solve --input "530070000600195000098000060800060003400803001700020060100050040000000070041500000"
```

## Python API

```python
from sudoku_game import Sudoku, generate_puzzle

# Generate new puzzle
puzzle, solution = generate_puzzle(n=3, difficulty=30)

# Solve existing puzzle
game = Sudoku(3)
game.set_board([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])
game.solve()
game.print_board()
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--size` | Board size: 2 (4x4), 3 (9x9), 4 (16x16) |
| `--difficulty` | Cells to remove: 20 (easy), 30 (medium), 45 (hard) |