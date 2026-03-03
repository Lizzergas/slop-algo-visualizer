from typing import Optional
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.timer import Timer

from src.ui.components import ArrayVisualizer
from src.algorithms.factory import AlgorithmFactory
from src.datasets.generators import DATASETS

class AlgorithmVisualizerScreen(Screen):
    """Screen for visualizing the algorithm in real-time."""

    BINDINGS = [
        Binding("q", "quit_to_menu", "Back to Menu", show=True),
        Binding("space", "pause_play", "Pause/Play", show=True),
        Binding("r", "restart", "Restart", show=True),
    ]

    def __init__(self, algo_name: str, ds_name: str, **kwargs):
        super().__init__(**kwargs)
        self.algo_name = algo_name
        self.ds_name = ds_name
        self.sort_iterator = None
        self.update_timer: Optional[Timer] = None
        self.is_paused = False
        self.array_size = 50 # Default width
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        algo = AlgorithmFactory.get_algorithm(self.algo_name)
        info_text = f"Algorithm: {self.algo_name} | Dataset: {self.ds_name}\n[dim]{algo.description}[/dim]"
        yield Static(info_text, id="info_label", classes="info-panel")
        
        self.visualizer = ArrayVisualizer(id="visualizer")
        yield self.visualizer
        yield Footer()

    def on_mount(self) -> None:
        self.start_algorithm()
        
    def start_algorithm(self) -> None:
        algo = AlgorithmFactory.get_algorithm(self.algo_name)
        dataset_gen = DATASETS[self.ds_name]
        
        array = dataset_gen(size=self.array_size)
        self.sort_iterator = algo.sort(array)
        self.is_paused = False
        
        if self.update_timer:
            self.update_timer.stop()
            
        # target higher FPS for smoother sorting experience, but depends on terminal
        self.update_timer = self.set_interval(1 / 45, self.update_visualizer)
        
    def update_visualizer(self) -> None:
        if self.is_paused:
            return
            
        try:
            state = next(self.sort_iterator)
            self.visualizer.state = state
            self.visualizer.refresh()
        except StopIteration:
            if self.update_timer:
                self.update_timer.pause()
            self.notify("Sorting complete!", title="Finished", timeout=2)

    def action_quit_to_menu(self) -> None:
        if self.update_timer:
            self.update_timer.stop()
        self.app.pop_screen()
        
    def action_pause_play(self) -> None:
        self.is_paused = not self.is_paused
        status = "Paused" if self.is_paused else "Resumed"
        self.notify(status, timeout=1)
        
    def action_restart(self) -> None:
        self.start_algorithm()
        self.notify("Restarted", timeout=1)
