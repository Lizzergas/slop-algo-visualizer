from abc import ABC, abstractmethod
from typing import Iterator, List, Any
from src.state import BaseState, SortState, NQueensState

class Algorithm(ABC):
    """Top level interface for all algorithms in the application."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the algorithm."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Category. e.g. 'Sorting' or 'Backtracking'."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def time_complexity(self) -> str:
        pass

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        pass

    @abstractmethod
    def execute(self, payload: Any) -> Iterator[BaseState]:
        """Core execution loop yielding state frames."""
        pass

class SortAlgorithm(Algorithm):
    """Base class for all array sorting operations."""
    
    @property
    def category(self) -> str:
        return "Sorting"
        
    def execute(self, payload: Any) -> Iterator[BaseState]:
        return self.sort(payload)

    @abstractmethod
    def sort(self, array: List[int]) -> Iterator[SortState]:
        """Sort yielding the array state at each significant step."""
        pass

class BacktrackingAlgorithm(Algorithm):
    """Base class for backtracking operations."""
    
    @property
    def category(self) -> str:
        return "Backtracking"

    def execute(self, payload: Any) -> Iterator[BaseState]:
        return self.solve(payload)

    @abstractmethod
    def solve(self, n: int) -> Iterator[NQueensState]:
        """Solve yielding the grid backtracing state at each critical check."""
        pass
