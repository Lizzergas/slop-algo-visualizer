from typing import Iterator, List
from src.state import AlgorithmState
from src.algorithms.base import SortAlgorithm

class SelectionSort(SortAlgorithm):
    @property
    def name(self) -> str:
        return "Selection Sort"

    @property
    def description(self) -> str:
        return (
            "Divides the input list into a sorted and an unsorted sublist. Repeatedly selects the smallest element from the unsorted sublist.\n"
            "Best/Worst/Avg: O(n^2) since it always scans the remaining elements."
        )

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        arr = array.copy()
        n = len(arr)
        yield AlgorithmState(arr.copy())
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                yield AlgorithmState(arr.copy(), comparing=[min_idx, j], sorted_indices=list(range(i)))
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                yield AlgorithmState(arr.copy(), comparing=[i, min_idx], swapping=[i, min_idx], sorted_indices=list(range(i)))
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield AlgorithmState(arr.copy(), comparing=[i, min_idx], swapping=[i, min_idx], sorted_indices=list(range(i+1)))
                
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(n)))
