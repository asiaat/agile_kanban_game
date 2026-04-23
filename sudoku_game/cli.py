"""Command-line interface for Sudoku game."""

import sys
import argparse
from sudoku_game.core import Sudoku, generate_puzzle


def main():
    parser = argparse.ArgumentParser(description="Sudoku Puzzle Generator and Solver")
    parser.add_argument("--new", action="store_true", help="Generate new puzzle")
    parser.add_argument("--size", type=int, default=3, help="Board size: 2 (4x4), 3 (9x9), 4 (16x16)")
    parser.add_argument("--difficulty", type=int, default=30, help="Difficulty: cells to remove (20=easy, 30=medium, 45=hard)")
    parser.add_argument("--solve", action="store_true", help="Solve puzzle from input")
    parser.add_argument("--input", type=str, help="Input file or string")

    args = parser.parse_args()

    if args.new:
        try:
            puzzle, solution = generate_puzzle(n=args.size, difficulty=args.difficulty)
            print(f"=== NEW SUDOKU PUZZLE ({args.size*args.size}x{args.size*args.size}) ===")
            print(f"Difficulty: {args.difficulty} cells removed")
            print()
            print("=== PUZZLE ===")
            puzzle.print_board()
            print()
            print("=== SOLUTION ===")
            solution.print_board()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.solve:
        if args.input:
            # Parse input string
            try:
                lines = [line.strip() for line in args.input.split('\n') if line.strip()]
                board = []
                for line in lines:
                    row = [int(c) if c.isdigit() else 0 for c in line.replace('.', '0').replace(' ', '')]
                    if row:
                        board.append(row)

                if board:
                    n = int(len(board) ** 0.5)
                    if n * n != len(board):
                        raise ValueError("Invalid board size")

                    game = Sudoku(n)
                    game.set_board(board)

                    print("=== ORIGINAL ===")
                    game.print_board()
                    print()

                    if game.solve():
                        print("=== SOLVED ===")
                        game.print_board()
                    else:
                        print("No solution exists!")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Usage: --solve --input 'puzzle_string'")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()