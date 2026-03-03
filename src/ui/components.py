from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.style import Style
from src.state import AlgorithmState

class ArrayVisualizer(Widget):
    """Widget to display the array as vertical bars."""
    
    state: AlgorithmState = reactive(AlgorithmState([]))
    
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
