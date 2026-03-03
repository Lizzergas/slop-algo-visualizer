from abc import ABC, abstractmethod
from typing import Iterator, List
from src.state import AlgorithmState

class SortAlgorithm(ABC):
    """Base class for all sorting algorithms."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the algorithm (e.g., 'Bubble Sort')."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of the algorithm and its best/worst case."""
        pass

    @abstractmethod
    def sort(self, array: List[int]) -> Iterator[AlgorithmState]:
        """
        Sort yielding the state of the array at each significant step.
        """
        pass
