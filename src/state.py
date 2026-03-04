from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class BaseState:
    """Base generic state representation for any algorithm step."""
    operations: int = 0
    time_elapsed: float = 0.0
    current_iteration: int = 0

@dataclass
class SortState(BaseState):
    """Specific state representations for Sorting (Array) algorithms."""
    array: List[int] = field(default_factory=list)
    comparing: Optional[List[int]] = None
    swapping: Optional[List[int]] = None
    sorted_indices: Optional[List[int]] = None

    def __post_init__(self):
        if self.comparing is None:
            self.comparing = []
        if self.swapping is None:
            self.swapping = []
        if self.sorted_indices is None:
            self.sorted_indices = []

@dataclass
class NQueensState(BaseState):
    """Specific state representation for Backtracking N-Queens algorithms."""
    n: int = 0
    board: List[int] = field(default_factory=list) # board[row] = col
    checking: Optional[Tuple[int, int]] = None
    valid_queens: List[Tuple[int, int]] = field(default_factory=list)
