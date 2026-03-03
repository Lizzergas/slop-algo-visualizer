from textual.app import App, ComposeResult
from textual.binding import Binding

from src.ui.menu import MenuScreen

class AlgoVisualizerApp(App):
    """The main Application class."""
    
    TITLE = "Algorithm Visualizer"
    
    CSS = """
    Screen {
        background: #1e1e2e;
        color: #cdd6f4;
    }

    Header {
        background: #89b4fa;
        color: #11111b;
        text-style: bold;
    }

    Footer {
        background: #313244;
    }

    #algo_list, #dataset_list {
        height: 1fr;
        border: solid #89dceb;
        background: #181825;
        margin: 1 2;
    }
    
    ListView > ListItem {
        padding: 0 1;
        background: transparent;
    }
    
    ListView:focus > ListItem.--highlight {
        background: #f38ba8;
        color: #11111b;
        text-style: bold;
    }

    .menu-title {
        content-align: center middle;
        text-style: bold;
        color: #a6e3a1;
        margin-top: 1;
    }
    
    .info-panel {
        content-align: center middle;
        padding: 1;
        border-bottom: solid #45475a;
        background: #181825;
        color: #cdd6f4;
    }
    
    ArrayVisualizer {
        height: 1fr;
        margin: 1 2;
        content-align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    def on_mount(self) -> None:
        """Push the starting screen when app mounts."""
        self.push_screen(MenuScreen())

if __name__ == "__main__":
    app = AlgoVisualizerApp()
    app.run()
