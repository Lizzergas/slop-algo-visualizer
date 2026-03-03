# Algorithm Visualizer Architecture

This document describes the design, architecture, and extension guidelines for the Algorithm Visualizer project.

## 1. Architecture Overview

The application is built using a unidirectional data flow and non-blocking TUI (Terminal User Interface) design via the **Textual** library. To visualize algorithms without freezing the terminal, we utilize the **Strategy/Template Pattern** combined with **Python Generators**.

Instead of a sorting algorithm executing completely and returning a sorted list, each algorithm is implemented as a generator that `yields` an atomic `AlgorithmState` at every critical step (e.g., comparison, swap). The UI consumes this generator frame-by-frame on a timer, causing the visual bars to update in real-time.

## 2. Directory Structure

```text
src/
├── main.py                # Main entrypoint; launches the Textual App.
├── state.py               # Contains the central Data Transfer Object (AlgorithmState).
├── algorithms/            # The Core Algorithms Domain
│   ├── base.py            # Abstract Base class dictating the interface.
│   ├── factory.py         # Factory class used by the UI to fetch algorithms.
│   └── *_sort.py          # Concrete implementations of sorting algorithms.
├── datasets/              # Dataset Generation Domain
│   └── generators.py      # Functions for best, worst, and average-case arrays.
└── ui/                    # Presentation Layer
    ├── app.py             # Main Textual App, manages global styles & screens.
    ├── components.py      # Isolated widgets (e.g., ArrayVisualizer drawing Rich bars).
    ├── menu.py            # Main Menu screen (Dataset/Algorithm selection).
    └── visualizer.py      # Screen that ties the generator to the widget via a Timer.
```

## 3. Core Components

### `state.py`
Defines `AlgorithmState`, a dataclass holding the current `array`, lists of indices currently being `comparing` or `swapping`, and elements that have been finalized as `sorted_indices`. It also maintains an `operations` integer for real-time tracking of array comparisons and swaps.

### `algorithms/base.py - SortAlgorithm`
The ABC defining the contract for every algorithm.
- `name` property.
- `description` property (used in the UI info panel).
- `time_complexity` property (returns best/avg/worst case string).
- `space_complexity` property (returns space complexity string).
- `sort(self, array: List[int]) -> Iterator[AlgorithmState]` method.

### `ui/visualizer.py`
Requests an algorithm iterator, sets up a Textual Timer, and pulls the `next(iterator)` at a high frame rate, passing the resulting `AlgorithmState` down to the `ArrayVisualizer` and `StatsPanel` reactive properties.

---

## 4. How to Extend the Application

### 4.1 Adding a New Sorting Algorithm
1. Create a new file in `src/algorithms/` (e.g., `src/algorithms/heap_sort.py`).
2. Import `SortAlgorithm` and `AlgorithmState`.
3. Create a class extending `SortAlgorithm`.
4. Provide standard properties (`name`, `description`, `time_complexity`, `space_complexity`).
5. Implement the `sort` method as a generator using `yield` and tracking `operations`:
    ```python
    from typing import Iterator, List
    from src.state import AlgorithmState
    from src.algorithms.base import SortAlgorithm

    class HeapSort(SortAlgorithm):
        @property
        def name(self) -> str: return "Heap Sort"
        
        @property
        def description(self) -> str: return "Description here..."
        
        @property
        def time_complexity(self) -> str: return "Best/Avg/Worst: O(n log n)"
        
        @property
        def space_complexity(self) -> str: return "O(1)"

        def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
            arr = array.copy()
            # Yield initial state
            yield AlgorithmState(arr.copy())
            
            # ... during logic when comparing i and j:
            yield AlgorithmState(arr.copy(), comparing=[i, j])
            
            # ... when swapping i and j:
            arr[i], arr[j] = arr[j], arr[i]
            yield AlgorithmState(arr.copy(), comparing=[i, j], swapping=[i, j])
            
            # Yield final sorted state
            yield AlgorithmState(arr.copy(), sorted_indices=list(range(len(arr))))
    ```
5. Register your layout in `src/algorithms/factory.py` inside the `AlgorithmFactory._algorithms` dictionary. The UI will automatically pick it up and display it in the menu.

### 4.2 Adding a New Dataset
1. Open `src/datasets/generators.py`.
2. Write a new standalone function that accepts `size` and returns `List[int]`.
    ```python
    def pure_random_list(size: int = 50) -> List[int]:
        return [random.randint(1, 1000) for _ in range(size)]
    ```
3. Add the function to the `DATASETS` dictionary at the bottom of the file. The dictionary key is what will appear in the UI list.

    ```python
    DATASETS = {
        "Random": random_list,
        "Pure Random (1-1000)": pure_random_list
    }
    ```

### 4.3 Modifying Key Bindings
Global keys are maintained in `ui/app.py`. Screen-specific keys (like vim movements) are inside the `BINDINGS` list on the designated Screen classes (`ui/menu.py` and `ui/visualizer.py`). Textual action handlers correspond to the binding (e.g. `Binding("j", "cursor_down", ...)` triggers `action_cursor_down(self)`).
