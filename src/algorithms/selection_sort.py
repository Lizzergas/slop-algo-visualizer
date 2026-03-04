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

    @property
    def time_complexity(self) -> str:
        return "Best: O(n²) | Avg: O(n²) | Worst: O(n²)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        arr = array.copy()
        n = len(arr)
        ops = 0
        yield AlgorithmState(arr.copy(), operations=ops, current_iteration=0)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                ops += 1 # compare
                yield AlgorithmState(arr.copy(), comparing=[min_idx, j], sorted_indices=list(range(i)), operations=ops, current_iteration=i)
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                ops += 1 # swap
                yield AlgorithmState(arr.copy(), comparing=[i, min_idx], swapping=[i, min_idx], sorted_indices=list(range(i)), operations=ops, current_iteration=i)
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                
            yield AlgorithmState(arr.copy(), comparing=[i, min_idx], swapping=[i, min_idx] if min_idx != i else [], sorted_indices=list(range(i+1)), operations=ops, current_iteration=i+1)
                
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(n)), operations=ops, current_iteration=n)
