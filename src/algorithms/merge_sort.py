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

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        arr = array.copy()
        yield AlgorithmState(arr.copy())
        
        yield from self._merge_sort(arr, 0, len(arr) - 1)
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(len(arr))))

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
            yield AlgorithmState(arr.copy(), comparing=[left+i, mid+1+j])
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            yield AlgorithmState(arr.copy(), swapping=[k])
            k += 1
            
        while i < len(L):
            arr[k] = L[i]
            yield AlgorithmState(arr.copy(), swapping=[k])
            i += 1
            k += 1
            
        while j < len(R):
            arr[k] = R[j]
            yield AlgorithmState(arr.copy(), swapping=[k])
            j += 1
            k += 1
