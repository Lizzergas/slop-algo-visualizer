from typing import Iterator, List
from src.state import SortState
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

    def sort(self, array: List[int]) -> Iterator[SortState]:
        self.operations = 0
        self.current_iteration = 0
        arr = array.copy()
        n = len(arr)
        # Initial un-sorted state
        yield SortState(arr.copy(), operations=self.operations, current_iteration=self.current_iteration)
        
        yield from self._quick_sort(arr, 0, n - 1)
        yield SortState(arr.copy(), sorted_indices=list(range(n)), operations=self.operations, current_iteration=n)

    def _quick_sort(self, arr: List[int], low: int, high: int) -> Iterator[SortState]:
        if low < high:
            pi_iterator = self._partition(arr, low, high)
            pi = None
            for state in pi_iterator:
                if isinstance(state, SortState):
                    yield state
                else:
                    pi = state
            
            if pi is not None:
                yield from self._quick_sort(arr, low, pi - 1)
                yield from self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr: List[int], low: int, high: int) -> Iterator[SortState | int]:
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.operations += 1 # Comparison
            # Compare current element with pivot BEFORE condition
            yield SortState(arr.copy(), comparing=[j, high], operations=self.operations, current_iteration=self.current_iteration)
            
            if arr[j] < pivot:
                i += 1
                self.operations += 1 # Swap
                arr[i], arr[j] = arr[j], arr[i]
                # State AFTER a swap during partitioning
                yield SortState(arr.copy(), comparing=[j, high], swapping=[i, j], operations=self.operations, current_iteration=self.current_iteration)
                
        # Final swap to put pivot in correct place
        self.operations += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield SortState(arr.copy(), swapping=[i + 1, high], operations=self.operations, current_iteration=self.current_iteration)
        
        yield i + 1
