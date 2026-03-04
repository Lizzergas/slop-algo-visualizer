# Algorithm Visualizer Architecture

This document describes the design, architecture, and extension guidelines for the Algorithm Visualizer project.

## 1. Architecture Overview

The application is built using a unidirectional data flow and non-blocking TUI (Terminal User Interface) design via the **Textual** library. It employs a **multi-category algorithm engine** to visualize diverse logic (Sorting, Backtracking, etc.).

### 1.1 Generic State Abstraction
Instead of hardcoding the UI to "Arrays", we use a **Protocol-based State Hierarchy**. Algorithms are generators that yield a `BaseState` object.
- **Sorting Algorithms** yield `SortState` (containing `array`, `swapping`, `comparing`).
- **N-Queens Algorithms** yield `NQueensState` (containing `board`, `n`, `checking`).

The UI dynamically mounts the correct visualizer widget based on the algorithm's **Category**.

## 2. Directory Structure

```text
src/
├── main.py                # Main entrypoint; launches the Textual App.
├── state.py               # Central State Hierarchy (BaseState, SortState, NQueensState).
├── algorithms/            # The Core Algorithms Domain
│   ├── base.py            # Abstract Base class & category definitions.
│   ├── factory.py         # Factory class used by the UI to fetch algorithms.
│   ├── *_sort.py          # Concrete implementations of sorting algorithms.
│   └── n_queens.py        # Implementation of N-Queens backtracking.
├── audio/                 # Audio synthesis domain (Sine waves mapped to frequencies).
├── metrics/               # Resource monitoring (CPU/RAM tracking).
└── ui/                    # Presentation Layer
    ├── app.py             # Main Textual App & global styles.
    ├── components.py      # Specialized Widgets (ArrayVisualizer, GridVisualizer).
    ├── menu.py            # Dynamic Selection screen (Category-aware).
    ├── visualizer.py      # Core visualization lifecycle controller.
    └── analysis_screen.py # Post-run performance graphing (Plotext).
```

## 3. Core Components

### `state.py`
Defines the `BaseState` ABC with common metrics (`operations`, `time_elapsed`, `current_iteration`).
Subclasses provide domain-specific data:
- `SortState`: `array`, `comparing`, `swapping`, `sorted_indices`.
- `NQueensState`: `board` (List[int]), `n` (size), `checking` (tuple), `valid_queens`.

### `algorithms/base.py`
The `Algorithm` ABC dictates the contract:
- `category`: "Sorting", "Backtracking", etc.
- `execute(payload: Any) -> Iterator[BaseState]`: Core generator loop.

### `ui/visualizer.py`
The `AlgorithmVisualizerScreen` is category-agnostic. On construction, it checks `algo.category` to:
1. **Mount Widgets**: Sets either `ArrayVisualizer` (bars) or `GridVisualizer` (chessboard).
2. **Start Iterator**: Passes either a dataset array or a board size `N` to the algorithm.

## 4. How to Extend the Application

### 4.1 Adding a New Category (e.g., Graph Algorithms)
1. Add a new `GraphState(BaseState)` in `src/state.py`.
2. Implement a `GraphAlgorithm` base in `src/algorithms/base.py`.
3. Create a `GraphVisualizer(Widget)` in `src/ui/components.py` to draw nodes/edges.
4. Update `AlgorithmVisualizerScreen.compose` to handle the "Graph" category.

### 4.2 Adding a New Algorithm
1. Create a implementation file in `src/algorithms/`.
2. Inherit from `SortAlgorithm` or `BacktrackingAlgorithm`.
3. Implement the `sort()` or `solve()` generator.
4. Register the class in `src/algorithms/factory.py`.

### 4.3 Adding a Dataset
1. Open `src/datasets/generators.py`.
2. Add a generation function and update the `DATASETS` dictionary.

---

## 5. Visual Standards
- **Sorting**: Uses vertical bars (`█`) with green/yellow/red semantic highlighting.
- **Grids**: Uses Unicode symbols (`♛` for queens, `♕` for checking) and high-contrast checkerboard patterns (`#3d3d3d` / `#262626`).
- **Charts**: Performance graphs use `textual-plotext` for real-time line/scatter visualization of CPU and RAM spikes.

