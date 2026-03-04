from typing import Iterator, List
from src.state import AlgorithmState
from src.algorithms.base import SortAlgorithm

class MergeSort(SortAlgorithm):
    @property
    def name(self) -> str:
        return "Merge Sort"

    @property
    def description(self) -> str:
        return (
            "Divide and conquer algorithm that splits the array in halves, sorts them and merges them back.\n"
            "Best/Worst/Avg: O(n log n). Consistent performance regardless of initial order."
        )

    @property
    def time_complexity(self) -> str:
        return "Best: O(n log n) | Avg: O(n log n) | Worst: O(n log n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        self.ops = 0
        arr = array.copy()
        yield AlgorithmState(arr.copy(), operations=self.ops, current_iteration=0)
        
        yield from self._merge_sort(arr, 0, len(arr) - 1)
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(len(arr))), operations=self.ops, current_iteration=len(arr))

    def _merge_sort(self, arr: List[int], left: int, right: int) -> Iterator[AlgorithmState]:
        if left < right:
            mid = (left + right) // 2
            
            yield from self._merge_sort(arr, left, mid)
            yield from self._merge_sort(arr, mid + 1, right)
            
            yield from self._merge(arr, left, mid, right)

    def _merge(self, arr: List[int], left: int, mid: int, right: int) -> Iterator[AlgorithmState]:
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(L) and j < len(R):
            self.ops += 1 # Comparison
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            self.ops += 1 # Write (act as swap for operations)
            yield AlgorithmState(arr.copy(), comparing=[k], swapping=[k], operations=self.ops, current_iteration=right)
            k += 1
            
        while i < len(L):
            arr[k] = L[i]
            self.ops += 1 # Write
            yield AlgorithmState(arr.copy(), comparing=[k], swapping=[k], operations=self.ops, current_iteration=right)
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            self.ops += 1 # Write
            yield AlgorithmState(arr.copy(), comparing=[k], swapping=[k], operations=self.ops, current_iteration=right)
            j += 1
            k += 1
