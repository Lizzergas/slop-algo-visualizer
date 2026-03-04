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
    
    .visualizer-container {
        height: 1fr;
        layout: horizontal;
    }

    .grid-container {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        height: 1fr;
    }
    
    .grid-panel {
        layout: vertical;
        border: solid #cba6f7;
        margin: 1 1;
        content-align: center middle;
        height: 100%;
        width: 100%;
    }
    
    .grid-label {
        dock: top;
        content-align: center middle;
        text-style: bold;
        color: #a6e3a1;
        background: #181825;
        width: 100%;
        height: 1;
    }

    ArrayVisualizer {
        width: 3fr;
        height: 1fr;
        margin: 0 1;
        content-align: center middle;
    }
    
    .grid-panel ArrayVisualizer {
        width: 1fr;
        height: 1fr;
        margin: 0 1;
    }
    
    .stats-panel {
        width: 1fr;
        height: 1fr;
        margin: 1 2 1 0;
        border: solid #cba6f7;
        padding: 1 2;
        background: #181825;
    }
    
    .stats-title {
        text-style: bold;
        color: #a6e3a1;
        text-align: center;
        margin-bottom: 1;
    }

    .stats-item {
        margin-bottom: 1;
    }
    
    .stats-label {
        color: #89b4fa;
        text-style: bold;
    }
    
    .stats-value {
        color: #f38ba8;
    }
    
    AnalysisScreen {
        align: center middle;
        background: $background 80%;
    }
    
    #analysis-dialog {
        padding: 1 2;
        width: 90%;
        height: auto;
        border: thick $background 80%;
        background: #1e1e2e;
    }
    
    .analysis-grid {
        layout: grid;
        grid-size: 3;
        grid-gutter: 1 2;
        grid-columns: 1fr 1fr 1fr;
        height: auto;
        margin-top: 1;
    }
    
    .summary-stats {
        layout: horizontal;
        width: 100%;
        padding: 0 4;
        margin-bottom: 1;
        content-align: center middle;
    }
    
    .center-text {
        text-align: center;
        width: 100%;
        margin-bottom: 1;
    }
    
    .button-container {
        align-horizontal: center;
        width: 100%;
        margin-top: 1;
    }
    
    .analysis-title {
        text-style: bold;
        color: #a6e3a1;
        text-align: center;
        margin-bottom: 2;
        width: 100%;
    }
    
    .analysis-subtitle {
        color: #89b4fa;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .analysis-card {
        border: solid #cba6f7;
        background: #181825;
        padding: 1 2;
        margin-bottom: 2;
        height: auto;
    }
    
    .analysis-stats {
        margin-top: 1;
        layout: horizontal;
        color: #f38ba8;
        width: 100%;
        content-align: right middle;
    }
    
    #close_btn {
        margin-top: 2;
        align-horizontal: center;
    }
    
    .plot-widget {
        height: 20;
        margin-top: 1;
        margin-bottom: 1;
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
