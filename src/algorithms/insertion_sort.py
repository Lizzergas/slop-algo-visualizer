from typing import Iterator, List
from src.state import AlgorithmState
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

    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        arr = array.copy()
        n = len(arr)
        yield AlgorithmState(arr.copy())
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            yield AlgorithmState(arr.copy(), comparing=[i, j], sorted_indices=list(range(i)))
            
            while j >= 0 and arr[j] > key:
                yield AlgorithmState(arr.copy(), comparing=[j, j+1], swapping=[j, j+1], sorted_indices=list(range(max(0, i-1))))
                arr[j + 1] = arr[j]
                j -= 1
                
            arr[j + 1] = key
            yield AlgorithmState(arr.copy(), sorted_indices=list(range(i+1)))
            
        yield AlgorithmState(arr.copy(), sorted_indices=list(range(n)))
