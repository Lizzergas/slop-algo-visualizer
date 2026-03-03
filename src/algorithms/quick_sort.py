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

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        arr = array.copy()
        yield AlgorithmState(arr.copy())
        
        yield from self._quick_sort(arr, 0, len(arr) - 1)
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(len(arr))))

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
            yield AlgorithmState(arr.copy(), comparing=[j, high])
            if arr[j] < pivot:
                i += 1
                yield AlgorithmState(arr.copy(), comparing=[i, j], swapping=[i, j])
                arr[i], arr[j] = arr[j], arr[i]
                yield AlgorithmState(arr.copy(), comparing=[i, j], swapping=[i, j])
                
        yield AlgorithmState(arr.copy(), comparing=[i + 1, high], swapping=[i + 1, high])
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield AlgorithmState(arr.copy(), comparing=[i + 1, high], swapping=[i + 1, high])
        
        yield i + 1
