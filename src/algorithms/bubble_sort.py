from typing import Iterator, List
from src.state import SortState
from src.algorithms.base import SortAlgorithm

class BubbleSort(SortAlgorithm):
    @property
    def name(self) -> str:
        return "Bubble Sort"

    @property
    def description(self) -> str:
        return (
            "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.\n"
            "Best: O(n) when already sorted. Worst/Avg: O(n^2)."
        )

    @property
    def time_complexity(self) -> str:
        return "Best: O(n) | Avg: O(n²) | Worst: O(n²)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def sort(self, array: List[int]) -> Iterator[SortState]:
        n = len(array)
        arr = array.copy()
        ops = 0
        # Initial state
        yield SortState(arr.copy(), operations=ops, current_iteration=0)
        
        for i in range(n):
            swapped = False
            # The last i elements are already in place
            sorted_indices = range(n - i, n)
            for j in range(0, n - i - 1):
                ops += 1 # Comparison
                # Yield state before comparison
                yield SortState(
                    arr.copy(),
                    comparing=[j, j + 1],
                    sorted_indices=list(sorted_indices),
                    operations=ops,
                    current_iteration=i + 1
                )
                if arr[j] > arr[j + 1]:
                    ops += 1 # Swap
                    yield SortState(arr.copy(), comparing=[j, j+1], swapping=[j, j+1], sorted_indices=list(sorted_indices), operations=ops, current_iteration=i+1)
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    # Yield state after swap
                    yield SortState(
                        arr.copy(),
                        comparing=[j, j + 1],
                        swapping=[j, j + 1],
                        sorted_indices=list(sorted_indices),
                        operations=ops,
                        current_iteration=i + 1
                    )
            if not swapped:
                break
            
            # Show the freshly sorted element at the end of the pass
            yield SortState(arr.copy(), sorted_indices=list(range(n-i-1, n)), operations=ops, current_iteration=i+1)
                
        yield SortState(arr.copy(), sorted_indices=list(range(n)), operations=ops, current_iteration=n)
