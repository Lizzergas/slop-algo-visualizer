from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Sparkline, Button
from textual.containers import Vertical, Horizontal, Grid

from src.metrics.system_monitor import SystemMonitor
from src.state import AlgorithmState

class AnalysisScreen(ModalScreen):
    """Modal Screen for displaying post-algorithm resource usage analysis."""
    
    BINDINGS = [
        ("q", "dismiss_modal", "Close Analysis"),
        ("escape", "dismiss_modal", "Close Analysis"),
    ]
    
    def __init__(self, algo_name: str, ds_name: str, monitor: SystemMonitor, final_state: AlgorithmState, **kwargs):
        super().__init__(**kwargs)
        self.algo_name = algo_name
        self.ds_name = ds_name
        self.monitor = monitor
        self.final_state = final_state

    def compose(self) -> ComposeResult:
        with Vertical(id="analysis-dialog"):
            yield Label(f"Performance Analysis: {self.algo_name}", classes="analysis-title")
            yield Label(f"Dataset: [white]{self.ds_name}[/white] ({len(self.final_state.array)} elements)", classes="analysis-subtitle center-text")
            
            with Horizontal(classes="summary-stats"):
                yield Label(f"Time Taken: [white]{self.final_state.time_elapsed:.3f}s[/white]")
                yield Label(f"Total Operations: [white]{self.final_state.operations:,}[/white]")
            
            with Grid(classes="analysis-grid"):
                # CPU Analysis
                with Vertical(classes="analysis-card"):
                    yield Label("CPU Usage Spikes (%)", classes="analysis-subtitle")
                    
                    cpu_data = self.monitor.history_cpu
                    if not cpu_data:
                        cpu_data = [0]
                    max_cpu = max(cpu_data)
                    avg_cpu = sum(cpu_data) / len(cpu_data)
                    
                    yield Sparkline(cpu_data, summary_function=max)
                    with Horizontal(classes="analysis-stats"):
                        yield Label(f"Max: {max_cpu:.1f}%")
                        yield Label(f"Avg: {avg_cpu:.1f}%")

                # Memory Analysis
                with Vertical(classes="analysis-card"):
                    yield Label("Memory Usage Spikes (MB)", classes="analysis-subtitle")
                    
                    mem_data = self.monitor.history_memory
                    if not mem_data:
                        mem_data = [0]
                    max_mem = max(mem_data)
                    avg_mem = sum(mem_data) / len(mem_data)
                    
                    yield Sparkline(mem_data, summary_function=max)
                    with Horizontal(classes="analysis-stats"):
                        yield Label(f"Max: {max_mem:.1f} MB")
                        yield Label(f"Avg: {avg_mem:.1f} MB")
                
            with Horizontal(classes="button-container"):
                yield Button("Close Analysis", id="close_btn", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_btn":
            self.action_dismiss_modal()

    def action_dismiss_modal(self) -> None:
        self.app.pop_screen()
