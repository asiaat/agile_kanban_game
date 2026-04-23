"""HTML generator for Sudoku puzzles - print-optimized."""

from sudoku_game.core import Sudoku, generate_puzzle


def generate_html(puzzle, solution, filename="sudoku.html", include_solution=True):
    """Generate printable HTML file from puzzle."""
    
    n = puzzle.n
    size = puzzle.size
    
    # Determine cell size based on board size
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
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    return filename


def main():
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Generate Sudoku HTML")
    parser.add_argument("--size", type=int, default=3, help="Board size: 2, 3, or 4")
    parser.add_argument("--difficulty", type=int, default=30, help="Cells to remove")
    parser.add_argument("--output", type=str, default="sudoku.html", help="Output filename")
    parser.add_argument("--no-solution", action="store_true", help="Exclude solution")
    
    args = parser.parse_args()
    
    puzzle, solution = generate_puzzle(n=args.size, difficulty=args.difficulty)
    
    filename = generate_html(
        puzzle, 
        solution, 
        filename=args.output,
        include_solution=not args.no_solution
    )
    
    print(f"Generated: {filename}")
    print(f"Board: {args.size*args.size}x{args.size*args.size}")


if __name__ == "__main__":
    main()