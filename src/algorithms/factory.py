from typing import Dict, List
from src.algorithms.base import SortAlgorithm
from src.algorithms.bubble_sort import BubbleSort
from src.algorithms.selection_sort import SelectionSort
from src.algorithms.insertion_sort import InsertionSort
from src.algorithms.merge_sort import MergeSort
from src.algorithms.quick_sort import QuickSort

class AlgorithmFactory:
    """Factory to retrieve and instantiate available sorting algorithms."""
    
    _algorithms = {
        "Bubble Sort": BubbleSort,
        "Selection Sort": SelectionSort,
        "Insertion Sort": InsertionSort,
        "Merge Sort": MergeSort,
        "Quick Sort": QuickSort
    }

    @classmethod
    def get_available_algorithms(cls) -> List[str]:
        return list(cls._algorithms.keys())

    @classmethod
    def get_algorithm(cls, name: str) -> SortAlgorithm:
        algo_class = cls._algorithms.get(name)
        if not algo_class:
            raise ValueError(f"Algorithm {name} not found.")
        return algo_class()
