"""HTML generator for Sudoku puzzles - print-optimized."""

import os
import re
from datetime import datetime

from sudoku_game.core import Sudoku, generate_puzzle


def generate_html(puzzle, solution, filename="sudoku.html", include_solution=True, output_dir="output"):
    """Generate printable HTML file from puzzle."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure .html extension
    if not filename.endswith('.html'):
        filename += '.html'
    
    filepath = os.path.join(output_dir, filename)
    
    n = puzzle.n
    size = puzzle.size
    cell_size = 40 if size == 9 else 30
    
    # Generate grid HTML
    puzzle_cells = ""
    solution_cells = ""
    
    for i in range(size):
        for j in range(size):
            p_val = puzzle.board[i][j]
            s_val = solution.board[i][j]
            
            # Add spacing class for box borders
            classes = []
            if j % n == 0 and j > 0:
                classes.append("box-left")
            if i % n == 0 and i > 0:
                classes.append("box-top")
            
            puzzle_cells += f'<div class="cell{" " + " ".join(classes) if classes else ""}">{p_val if p_val != 0 else ""}</div>'
            solution_cells += f'<div class="cell{" " + " ".join(classes) if classes else ""}">{s_val}</div>'
    
    # Determine solution display
    solution_block = ""
    if include_solution:
        solution_block = f'''
    <div class="page-break"></div>
    <h2>Lahendus / Solution</h2>
    <div class="grid">{solution_cells}</div>
'''
    
    html = f'''<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sudoku - {size}x{size}</title>
    <style>
        @page {{
            size: auto;
            margin: 5mm;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 20px;
            background: white;
        }}
        
        h1 {{
            text-align: center;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .info {{
            text-align: center;
            margin-bottom: 20px;
            color: #666;
            font-size: 14px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat({size}, {cell_size}px);
            gap: 0;
            width: {size * cell_size}px;
            margin: 0 auto;
            border: 3px solid #333;
        }}
        
        .cell {{
            width: {cell_size}px;
            height: {cell_size}px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: {18 if size == 9 else 14}px;
            border: 1px solid #ddd;
            background: white;
        }}
        
        .cell.box-left {{
            border-left: 3px solid #333;
        }}
        
        .cell.box-top {{
            border-top: 3px solid #333;
        }}
        
        .cell:empty {{
            color: #ccc;
        }}
        
        .page-break {{
            page-break-after: always;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #999;
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            
            .page-break {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
    <h1>Sudoku {size}x{size}</h1>
    <p class="info">Täida ruudud numbritega 1-{size} | Fill with numbers 1-{size}</p>
    
    <div class="grid">
        {puzzle_cells}
    </div>
    
    {solution_block}
    
    <p class="footer">Sudoku Game Engine</p>
</body>
</html>
'''
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return filepath


def main():
    import argparse
    import os
    
    import re
    
    parser = argparse.ArgumentParser(description="Generate Sudoku HTML")
    parser.add_argument("--size", type=int, default=3, choices=[2, 3, 4], help="Board size: 2 (4x4), 3 (9x9), 4 (16x16)")
    parser.add_argument("--difficulty", type=int, default=30, help="Cells to remove: 20=easy, 30=medium, 45=hard")
    parser.add_argument("--output", type=str, default="", help="Output filename")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory")
    parser.add_argument("--no-solution", action="store_true", help="Exclude solution")
    
    args = parser.parse_args()
    
    args.difficulty = args.difficulty or 30
    
    # Validate difficulty range (cells to remove)
    args.difficulty = max(5, min(60, args.difficulty))
    
    # Board size string (e.g., "4x4", "9x9")
    size_str = f"{args.size*args.size}x{args.size*args.size}"
    
    # Use timestamp only if no custom filename provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"{size_str}_{timestamp}.html"
    elif args.output:
        # Only add timestamp and size if filename doesn't have numeric suffix pattern
        if not re.search(r'_\d{12}$', args.output):
            base, ext = os.path.splitext(args.output)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Add size prefix if not present
            if not base.startswith(size_str):
                args.output = f"{size_str}_{base}_{timestamp}{ext}"
            else:
                args.output = f"{base}_{timestamp}{ext}"
        if not ext:
            args.output += '.html'
    
    puzzle, solution = generate_puzzle(n=args.size, difficulty=args.difficulty)
    
    filepath = generate_html(
        puzzle, 
        solution, 
        filename=args.output,
        include_solution=not args.no_solution,
        output_dir=args.output_dir
    )
    
    print(f"Generated: {filepath}")
    print(f"Board: {args.size*args.size}x{args.size*args.size}")
    print(f"Difficulty: {args.difficulty} cells removed")


if __name__ == "__main__":
    main()