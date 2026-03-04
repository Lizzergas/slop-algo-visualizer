from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AlgorithmState:
    """Represents the state of an algorithm at a specific step in time."""
    array: List[int]
    comparing: Optional[List[int]] = None
    swapping: Optional[List[int]] = None
    sorted_indices: Optional[List[int]] = None
    operations: int = 0
    time_elapsed: float = 0.0
    current_iteration: int = 0

    def __post_init__(self):
        if self.comparing is None:
            self.comparing = []
        if self.swapping is None:
            self.swapping = []
        if self.sorted_indices is None:
            self.sorted_indices = []
