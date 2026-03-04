from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.table import Table
from rich.style import Style
from rich.color import Color
from src.state import SortState, NQueensState

class ArrayVisualizer(Widget):
    """Widget to display the array as vertical bars."""
    
    state: SortState = reactive(SortState([]))
    
    def render(self) -> Text:
        if not self.state.array:
            return Text("Loading...", style="dim")
            
        arr = self.state.array
        max_val = max(arr) if arr else 1
        
        # Determine available height and width
        height = max(1, self.size.height - 2) # leave room for borders or titles if any
        width = len(arr)
        
        # Scale values to height
        scaled_arr = [int((val / max_val) * height) for val in arr]
        
        lines = []
        for row in range(height, 0, -1):
            line = Text()
            for i, val in enumerate(scaled_arr):
                # Determine color based on state
                style = "green" if i in self.state.sorted_indices else "white"
                
                if i in self.state.comparing:
                    style = "yellow"
                if i in self.state.swapping:
                    style = "red"
                    
                char = "█" if val >= row else " "
                line.append(char, style=Style(color=style))
            lines.append(line)
            
        result = Text("\n").join(lines)
        return result

class GridVisualizer(Widget):
    """Widget to display N-Queens Grid logic."""
    state: NQueensState = reactive(NQueensState())

    def render(self) -> Table:
        n = self.state.n
        if n == 0:
            return Table(show_header=False)
            
        table = Table(
            show_header=False,
            show_edge=True,
            show_lines=True,
            padding=(0, 0),
            collapse_padding=True,
            border_style="bright_blue",
            title=f"N-Queens Algorithm ({n}x{n})"
        )
        
        for _ in range(n):
            table.add_column(width=7, justify="center")

        board = self.state.board
        valid_queens = self.state.valid_queens
        checking = self.state.checking

        for r in range(n):
            row_cells = []
            for c in range(n):
                # Checkerboard BG coloring
                is_light = (r + c) % 2 == 0
                bg_color = "#3d3d3d" if is_light else "#262626"
                
                cell_content = " "
                fg_color = "white"
                bold = False
                
                # If there's a firmly placed valid queen
                if (r, c) in valid_queens:
                    cell_content = "♛" 
                    fg_color = "#00ff00" # Bright Green
                    bold = True
                    
                # If this is the specific cell we're checking right now
                if checking and checking == (r, c):
                    cell_content = "♕"
                    fg_color = "yellow"
                    bg_color = "#d75f00" # Orange-ish
                    bold = True
                
                # If the board array indicates a queen here but it's not strictly 'valid' nor checking
                if r < len(board) and board[r] == c and cell_content == " ":
                    cell_content = "✘"
                    fg_color = "red"
                
                style = Style(color=fg_color, bgcolor=bg_color, bold=bold)
                # Make the cell a bit thicker for "square-ish" look
                row_cells.append(Text(f"\n {cell_content} \n", style=style, justify="center"))
            
            table.add_row(*row_cells)
            
        return table
