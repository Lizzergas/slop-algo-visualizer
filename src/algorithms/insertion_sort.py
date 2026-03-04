from typing import Iterator, List
from src.state import SortState
from src.algorithms.base import SortAlgorithm

class InsertionSort(SortAlgorithm):
    @property
    def name(self) -> str:
        return "Insertion Sort"

    @property
    def description(self) -> str:
        return (
            "Builds the final sorted array one item at a time by taking elements and inserting them into their correct position.\n"
            "Best: O(n) when nearly sorted. Worst: O(n^2) when reversed."
        )

    @property
    def time_complexity(self) -> str:
        return "Best: O(n) | Avg: O(n²) | Worst: O(n²)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def sort(self, array: List[int]) -> Iterator[SortState]:
        arr = array.copy()
        n = len(arr)
        ops = 0
        yield SortState(arr.copy(), operations=ops, current_iteration=0)
        
        for i in range(1, n):
            j = i
            
            ops += 1 # setup compare
            yield SortState(arr.copy(), comparing=[j, j-1], sorted_indices=list(range(i)), operations=ops, current_iteration=i)
            
            while j > 0 and arr[j-1] > arr[j]:
                ops += 1 # shift/swap
                yield SortState(arr.copy(), comparing=[j-1, j], swapping=[j-1, j], sorted_indices=list(range(max(0, i))), operations=ops, current_iteration=i)
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
                
            yield SortState(arr.copy(), sorted_indices=list(range(i+1)), operations=ops, current_iteration=i+1)
            
        yield SortState(arr.copy(), sorted_indices=list(range(n)), operations=ops, current_iteration=n)
