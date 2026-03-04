from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical, Horizontal, Grid
from textual_plotext import PlotextPlot

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
                    yield PlotextPlot(id="cpu_plot", classes="plot-widget")
                    
                    cpu_data = self.monitor.history_cpu
                    time_data = self.monitor.history_time
                    if not cpu_data:
                        cpu_data = [0]
                        time_data = [0.0]
                        
                    max_cpu = max(cpu_data)
                    avg_cpu = sum(cpu_data) / len(cpu_data)
                    max_cpu_time = time_data[cpu_data.index(max_cpu)]
                    
                    with Horizontal(classes="analysis-stats"):
                        yield Label(f"Peak Spike: [white]{max_cpu:.1f}% at T={max_cpu_time:.2f}s[/white]")
                        yield Label(f"Avg: [white]{avg_cpu:.1f}%[/white]")

                # Memory Analysis
                with Vertical(classes="analysis-card"):
                    yield PlotextPlot(id="mem_plot", classes="plot-widget")
                    
                    mem_data = self.monitor.history_memory
                    time_data = self.monitor.history_time
                    if not mem_data:
                        mem_data = [0]
                        time_data = [0.0]
                        
                    max_mem = max(mem_data)
                    avg_mem = sum(mem_data) / len(mem_data)
                    max_mem_time = time_data[mem_data.index(max_mem)]
                    
                    with Horizontal(classes="analysis-stats"):
                        yield Label(f"Peak Spike: [white]{max_mem:.1f} MB at T={max_mem_time:.2f}s[/white]")
                        yield Label(f"Avg: [white]{avg_mem:.1f} MB[/white]")

                # Iterations Analysis
                with Vertical(classes="analysis-card"):
                    yield PlotextPlot(id="iters_plot", classes="plot-widget")
                    
                    iters_data = self.monitor.history_iterations
                    if not iters_data:
                        iters_data = [0]
                        
                    max_iters = max(iters_data)
                    
                    with Horizontal(classes="analysis-stats"):
                        yield Label(f"Max Iterations Reached: [white]{max_iters}[/white]")
                
            with Horizontal(classes="button-container"):
                yield Button("Close Analysis", id="close_btn", variant="primary")

    def on_mount(self) -> None:
        """Render the explicit Plotext charts after mounting."""
        time_data = self.monitor.history_time
        if not time_data:
            time_data = [0.0]
            
        # Compile CPU Chart
        cpu_data = self.monitor.history_cpu or [0]
        cpu_plt = self.query_one("#cpu_plot", PlotextPlot).plt
        cpu_plt.plot(time_data, cpu_data, color="cyan")
        cpu_plt.title("CPU Utilization During Sort")
        cpu_plt.xlabel("Elapsed Time (s)")
        cpu_plt.ylabel("CPU %")

        # Compile RAM Chart
        mem_data = self.monitor.history_memory or [0]
        mem_plt = self.query_one("#mem_plot", PlotextPlot).plt
        mem_plt.plot(time_data, mem_data, color="magenta", marker="dot")
        mem_plt.title("Memory Utilization During Sort")
        mem_plt.xlabel("Elapsed Time (s)")
        mem_plt.ylabel("RAM Usage (MB)")

        # Compile Iterations Chart
        iters_data = self.monitor.history_iterations or [0]
        iters_plt = self.query_one("#iters_plot", PlotextPlot).plt
        iters_plt.plot(time_data, iters_data, color="yellow", marker="dot")
        iters_plt.title("Algorithm Progress (i/n)")
        iters_plt.xlabel("Elapsed Time (s)")
        iters_plt.ylabel("Iterations (i)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_btn":
            self.action_dismiss_modal()

    def action_dismiss_modal(self) -> None:
        self.app.pop_screen()
