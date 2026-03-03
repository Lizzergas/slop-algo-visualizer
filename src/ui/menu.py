from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.binding import Binding

from src.algorithms.factory import AlgorithmFactory
from src.datasets.generators import DATASETS
from src.ui.visualizer import AlgorithmVisualizerScreen

class MenuScreen(Screen):
    """Main Menu text UI for Algorithm selections."""

    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "escape_focus", "Blur", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        
        algos = AlgorithmFactory.get_available_algorithms()
        yield Label("Select Sorting Algorithm:", classes="menu-title")
        
        list_items = [ListItem(Label(algo), id=f"algo_{i}") for i, algo in enumerate(algos)]
        self.algo_list = ListView(*list_items, id="algo_list")
        yield self.algo_list
        
        yield Label("Select Dataset:", classes="menu-title")
        dataset_items = [ListItem(Label(ds), id=f"ds_{i}") for i, ds in enumerate(DATASETS.keys())]
        self.dataset_list = ListView(*dataset_items, id="dataset_list")
        yield self.dataset_list
        
        yield Footer()

    def on_mount(self) -> None:
        self.algo_list.focus()

    def action_cursor_down(self) -> None:
        """Handle vim-like j key bindings."""
        if self.algo_list.has_focus:
            self.algo_list.action_cursor_down()
        elif self.dataset_list.has_focus:
            self.dataset_list.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Handle vim-like k key bindings."""
        if self.algo_list.has_focus:
            self.algo_list.action_cursor_up()
        elif self.dataset_list.has_focus:
            self.dataset_list.action_cursor_up()
            
    def action_escape_focus(self) -> None:
        self.app.set_focus(None)
            
    from textual import on

    @on(ListView.Selected, "#algo_list")
    def on_algo_selected(self, event: ListView.Selected) -> None:
        """Handle enter to move from algorithms to dataset."""
        self.dataset_list.focus()

    @on(ListView.Selected, "#dataset_list")
    def on_dataset_selected(self, event: ListView.Selected) -> None:
        """Handle enter to start visualization after picking dataset."""
        self._start_visualization()
            
    def _start_visualization(self) -> None:
        algo_idx = self.algo_list.index
        ds_idx = self.dataset_list.index
        
        if algo_idx is not None and ds_idx is not None:
            algo_name = AlgorithmFactory.get_available_algorithms()[algo_idx]
            ds_name = list(DATASETS.keys())[ds_idx]
            
            screen = AlgorithmVisualizerScreen(algo_name=algo_name, ds_name=ds_name)
            self.app.push_screen(screen)
