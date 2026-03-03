from typing import Optional
import time
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.timer import Timer

from src.ui.components import ArrayVisualizer
from src.algorithms.factory import AlgorithmFactory
from src.datasets.generators import DATASETS

class StatsPanel(Static):
    """A sidebar panel that displays complexity and running metrics."""

    def __init__(self, algo_name: str, **kwargs):
        super().__init__(**kwargs)
        self.algo = AlgorithmFactory.get_algorithm(algo_name)

    def compose(self) -> ComposeResult:
        yield Label("ALGORITHM STATS", classes="stats-title")
        
        with Vertical(classes="stats-item"):
            yield Label("Time Complexity:", classes="stats-label")
            yield Label(self.algo.time_complexity, classes="stats-value")

        with Vertical(classes="stats-item"):
            yield Label("Space Complexity:", classes="stats-label")
            yield Label(self.algo.space_complexity, classes="stats-value")

        with Vertical(classes="stats-item"):
            yield Label("Operations (Swaps/Compares):", classes="stats-label")
            yield Label("0", id="ops_value", classes="stats-value")

        with Vertical(classes="stats-item"):
            yield Label("Time Elapsed:", classes="stats-label")
            yield Label("0.000s", id="time_value", classes="stats-value")

    def update_metrics(self, ops: int, elapsed: float) -> None:
        ops_label = self.query_one("#ops_value", Label)
        ops_label.update(f"{ops:,}")
        
        time_label = self.query_one("#time_value", Label)
        time_label.update(f"{elapsed:.3f}s")


class AlgorithmVisualizerScreen(Screen):
    """Screen for visualizing the algorithm in real-time."""

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

    def __init__(self, algo_name: str, ds_name: str, **kwargs):
        super().__init__(**kwargs)
        self.algo_name = algo_name
        self.ds_name = ds_name
        self.sort_iterator = None
        self.update_timer: Optional[Timer] = None
        self.is_paused = False
        self.array_size = 50 # Default width
        self.base_fps = 45 # Default frames per second base
        self.speed_multiplier = 1.0
        
        # Real-time tracking
        self.start_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.last_tick_time: float = 0.0
        
    def _get_info_text(self) -> str:
        algo = AlgorithmFactory.get_algorithm(self.algo_name)
        return (f"Algorithm: {self.algo_name} | Dataset: {self.ds_name} | "
                f"Speed: {self.speed_multiplier:.1f}x\n[dim]{algo.description}[/dim]")

    def compose(self) -> ComposeResult:
        yield Header()
        
        info_text = self._get_info_text()
        yield Static(info_text, id="info_label", classes="info-panel")
        
        with Horizontal(classes="visualizer-container"):
            self.visualizer = ArrayVisualizer(id="visualizer")
            yield self.visualizer
            
            self.stats_panel = StatsPanel(algo_name=self.algo_name, classes="stats-panel")
            yield self.stats_panel
            
        yield Footer()

    def on_mount(self) -> None:
        self.start_algorithm()
        
    def start_algorithm(self) -> None:
        algo = AlgorithmFactory.get_algorithm(self.algo_name)
        dataset_gen = DATASETS[self.ds_name]
        
        array = dataset_gen(size=self.array_size)
        self.sort_iterator = algo.sort(array)
        self.is_paused = False
        self.elapsed_time = 0.0
        self.last_tick_time = time.perf_counter()
        
        self.stats_panel.update_metrics(0, self.elapsed_time)
        self._update_timer_speed()
            
    def _update_timer_speed(self) -> None:
        if self.update_timer:
            self.update_timer.stop()
        
        current_fps = self.base_fps * self.speed_multiplier
        # Ensure we don't divide by zero or go too slow if multiplier gets very small
        interval = 1 / max(1, current_fps)
        self.update_timer = self.set_interval(interval, self.update_visualizer)

    def _update_info_label(self) -> None:
        info_label = self.query_one("#info_label", Static)
        info_label.update(self._get_info_text())

    def update_visualizer(self) -> None:
        if self.is_paused:
            self.last_tick_time = time.perf_counter() # Prevent jump after resume
            return
            
        current_time = time.perf_counter()
        self.elapsed_time += (current_time - self.last_tick_time)
        self.last_tick_time = current_time
            
        try:
            state = next(self.sort_iterator)
            self.visualizer.state = state
            self.visualizer.refresh()
            self.stats_panel.update_metrics(state.operations, self.elapsed_time)
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

    def action_speed_up(self) -> None:
        self.speed_multiplier = min(20.0, self.speed_multiplier + 0.5)
        self._update_timer_speed()
        self._update_info_label()
        self.notify(f"Speed: {self.speed_multiplier:.1f}x", timeout=1)

    def action_speed_down(self) -> None:
        self.speed_multiplier = max(0.5, self.speed_multiplier - 0.5)
        self._update_timer_speed()
        self._update_info_label()
        self.notify(f"Speed: {self.speed_multiplier:.1f}x", timeout=1)
