from typing import Iterator, List
from src.state import AlgorithmState
from src.algorithms.base import SortAlgorithm

class QuickSort(SortAlgorithm):
    @property
    def name(self) -> str:
        return "Quick Sort"

    @property
    def description(self) -> str:
        return (
            "Selects a 'pivot' element and partitions the other elements into two sub-arrays, according to whether they are less than or greater than the pivot.\n"
            "Best/Avg: O(n log n). Worst: O(n^2) when already sorted or reversed (with poor pivot)."
        )

    @property
    def time_complexity(self) -> str:
        return "Best: O(n log n) | Avg: O(n log n) | Worst: O(n²)"

    @property
    def space_complexity(self) -> str:
        return "O(log n)"

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        self.ops = 0
        arr = array.copy()
        yield AlgorithmState(arr.copy(), operations=self.ops)
        
        yield from self._quick_sort(arr, 0, len(arr) - 1)
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(len(arr))), operations=self.ops)

    def _quick_sort(self, arr: List[int], low: int, high: int) -> Iterator[AlgorithmState]:
        if low < high:
            pi_iterator = self._partition(arr, low, high)
            pi = None
            for state in pi_iterator:
                if isinstance(state, AlgorithmState):
                    yield state
                else:
                    pi = state
            
            if pi is not None:
                yield from self._quick_sort(arr, low, pi - 1)
                yield from self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr: List[int], low: int, high: int) -> Iterator[AlgorithmState | int]:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.ops += 1 # Comparison
            yield AlgorithmState(arr.copy(), comparing=[j, high], operations=self.ops)
            if arr[j] < pivot:
                i += 1
                self.ops += 1 # Swap
                yield AlgorithmState(arr.copy(), comparing=[i, j], swapping=[i, j], operations=self.ops)
                arr[i], arr[j] = arr[j], arr[i]
                yield AlgorithmState(arr.copy(), comparing=[i, j], swapping=[i, j], operations=self.ops)
                
        self.ops += 1 # Swap pivot
        yield AlgorithmState(arr.copy(), comparing=[i + 1, high], swapping=[i + 1, high], operations=self.ops)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield AlgorithmState(arr.copy(), comparing=[i + 1, high], swapping=[i + 1, high], operations=self.ops)
        
        yield i + 1
