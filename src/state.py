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

    def __init__(self, array: Optional[List[int]] = None, comparing: Optional[List[int]] = None, swapping: Optional[List[int]] = None, sorted_indices: Optional[List[int]] = None, operations: int = 0, time_elapsed: float = 0.0, current_iteration: int = 0):
        super().__init__(operations=operations, time_elapsed=time_elapsed, current_iteration=current_iteration)
        self.array = array if array is not None else []
        self.comparing = comparing if comparing is not None else []
        self.swapping = swapping if swapping is not None else []
        self.sorted_indices = sorted_indices if sorted_indices is not None else []

@dataclass
class NQueensState(BaseState):
    """Specific state representation for Backtracking N-Queens algorithms."""
    n: int = 0
    board: List[int] = field(default_factory=list) # board[row] = col
    checking: Optional[Tuple[int, int]] = None
    valid_queens: List[Tuple[int, int]] = field(default_factory=list)

    def __init__(self, n: int = 0, board: Optional[List[int]] = None, checking: Optional[Tuple[int, int]] = None, valid_queens: Optional[List[Tuple[int, int]]] = None, operations: int = 0, time_elapsed: float = 0.0, current_iteration: int = 0):
        super().__init__(operations=operations, time_elapsed=time_elapsed, current_iteration=current_iteration)
        self.n = n
        self.board = board if board is not None else []
        self.checking = checking
        self.valid_queens = valid_queens if valid_queens is not None else []
