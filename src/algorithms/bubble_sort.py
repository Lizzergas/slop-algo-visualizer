from typing import Iterator, List
from src.state import AlgorithmState
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

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        n = len(array)
        arr = array.copy()
        ops = 0
        yield AlgorithmState(arr.copy(), operations=ops, current_iteration=0)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                ops += 1 # Comparison
                yield AlgorithmState(arr.copy(), comparing=[j, j+1], sorted_indices=list(range(n-i, n)), operations=ops, current_iteration=i)
                if arr[j] > arr[j + 1]:
                    ops += 1 # Swap
                    yield AlgorithmState(arr.copy(), comparing=[j, j+1], swapping=[j, j+1], sorted_indices=list(range(n-i, n)), operations=ops, current_iteration=i)
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    yield AlgorithmState(arr.copy(), comparing=[j, j+1], swapping=[j, j+1], sorted_indices=list(range(n-i, n)), operations=ops, current_iteration=i)
            if not swapped:
                break
            
            # Show the freshly sorted element at the end of the pass
            yield AlgorithmState(arr.copy(), sorted_indices=list(range(n-i-1, n)), operations=ops, current_iteration=i+1)
                
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(n)), operations=ops, current_iteration=n)
