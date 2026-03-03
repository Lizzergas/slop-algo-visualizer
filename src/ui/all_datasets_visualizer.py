import time
from typing import Optional, Dict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Container, Grid
from textual.binding import Binding
from textual.timer import Timer

from src.ui.components import ArrayVisualizer
from src.algorithms.factory import AlgorithmFactory
from src.datasets.generators import DATASETS

class GridPanel(Container):
    """A container holding a single ArrayVisualizer and its title/stats."""
    def __init__(self, ds_name: str, **kwargs):
        super().__init__(**kwargs)
        self.ds_name = ds_name
        self.visualizer = ArrayVisualizer(id=f"vis_{ds_name.split()[0].lower()}")
        
    def compose(self) -> ComposeResult:
        # We use a Label to show the dataset name and the current ops/time
        yield Label(f"{self.ds_name} | Ops: 0 | Time: 0.000s", id="grid_header", classes="grid-label")
        yield self.visualizer

    def update_stats(self, ops: int, elapsed: float, is_done: bool) -> None:
        header = self.query_one("#grid_header", Label)
        status = "[DONE]" if is_done else ""
        header.update(f"{self.ds_name} {status} | Ops: {ops:,} | Time: {elapsed:.3f}s")


class AllDatasetsVisualizerScreen(Screen):
    """Screen for visualizing the same algorithm on all 4 datasets simultaneously."""

    BINDINGS = [
        Binding("q", "quit_to_menu", "Back to Menu", show=True),
        Binding("space", "pause_play", "Pause/Play", show=True),
        Binding("r", "restart", "Restart", show=True),
        Binding("plus", "speed_up", "Speed Up", show=True),
        Binding("=", "speed_up", "Speed Up", show=False),
        Binding("+", "speed_up", "Speed Up", show=False),
        Binding("minus", "speed_down", "Speed Down", show=True),
        Binding("-", "speed_down", "Speed Down", show=False),
    ]

    def __init__(self, algo_name: str, **kwargs):
        super().__init__(**kwargs)
        self.algo_name = algo_name
        self.array_size = 30 # Slightly smaller default width to fit grid better
        self.base_fps = 45
        self.speed_multiplier = 1.0
        self.is_paused = False
        self.update_timer: Optional[Timer] = None
        
        # State tracking per dataset
        self.iterators = {}
        self.elapsed_times = {}
        self.operations = {}
        self.finished = {}
        self.last_tick_time: float = 0.0

    def _get_info_text(self) -> str:
        algo = AlgorithmFactory.get_algorithm(self.algo_name)
        return (f"Algorithm: {self.algo_name} | Dataset: ALL | "
                f"Speed: {self.speed_multiplier:.1f}x\n[dim]{algo.description}[/dim]")

    def compose(self) -> ComposeResult:
        yield Header()
        
        info_text = self._get_info_text()
        yield Static(info_text, id="info_label", classes="info-panel")
        
        with Grid(classes="grid-container"):
            for ds_name in DATASETS.keys():
                yield GridPanel(ds_name=ds_name, classes="grid-panel", id=f"panel_{ds_name.split()[0].lower()}")
            
        yield Footer()

    def on_mount(self) -> None:
        self.start_algorithm()
        
    def start_algorithm(self) -> None:
        self.is_paused = False
        algo_class = AlgorithmFactory._algorithms[self.algo_name]
        
        for ds_name, dataset_gen in DATASETS.items():
            array = dataset_gen(size=self.array_size)
            # Create a separate instance of the algorithm for each dataset
            algo_instance = algo_class() 
            self.iterators[ds_name] = algo_instance.sort(array)
            self.elapsed_times[ds_name] = 0.0
            self.operations[ds_name] = 0
            self.finished[ds_name] = False
            
            # Reset UI
            panel = self.query_one(f"#panel_{ds_name.split()[0].lower()}", GridPanel)
            panel.update_stats(0, 0.0, False)
            
        self.last_tick_time = time.perf_counter()
        self._update_timer_speed()
            
    def _update_timer_speed(self) -> None:
        if self.update_timer:
            self.update_timer.stop()
        
        current_fps = self.base_fps * self.speed_multiplier
        interval = 1 / max(1, current_fps)
        self.update_timer = self.set_interval(interval, self.update_visualizers)

    def _update_info_label(self) -> None:
        info_label = self.query_one("#info_label", Static)
        info_label.update(self._get_info_text())

    def update_visualizers(self) -> None:
        if self.is_paused:
            self.last_tick_time = time.perf_counter()
            return

        current_time = time.perf_counter()
        delta = current_time - self.last_tick_time
        self.last_tick_time = current_time
        
        all_finished = True

        for ds_name, iterator in self.iterators.items():
            if self.finished[ds_name]:
                continue
                
            all_finished = False
            self.elapsed_times[ds_name] += delta
            
            try:
                state = next(iterator)
                self.operations[ds_name] = state.operations
                
                panel = self.query_one(f"#panel_{ds_name.split()[0].lower()}", GridPanel)
                panel.visualizer.state = state
                panel.visualizer.refresh()
                panel.update_stats(state.operations, self.elapsed_times[ds_name], False)
                
            except StopIteration:
                self.finished[ds_name] = True
                panel = self.query_one(f"#panel_{ds_name.split()[0].lower()}", GridPanel)
                panel.update_stats(self.operations[ds_name], self.elapsed_times[ds_name], True)

        if all_finished:
            if self.update_timer:
                self.update_timer.pause()
            self.notify("All sorting complete!", title="Finished", timeout=3)

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

    def action_speed_up(self) -> None:
        self.speed_multiplier = min(20.0, self.speed_multiplier + 0.5)
        self._update_timer_speed()
        self._update_info_label()
        self.app.clear_notifications()
        self.notify(f"Speed: {self.speed_multiplier:.1f}x", timeout=1)

    def action_speed_down(self) -> None:
        self.speed_multiplier = max(0.5, self.speed_multiplier - 0.5)
        self._update_timer_speed()
        self._update_info_label()
        self.app.clear_notifications()
        self.notify(f"Speed: {self.speed_multiplier:.1f}x", timeout=1)
