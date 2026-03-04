from typing import Iterator, List
from src.state import NQueensState
from src.algorithms.base import BacktrackingAlgorithm

class NQueensAlgorithm(BacktrackingAlgorithm):
    """Solves the N-Queens problem using backtracking."""
    
    @property
    def name(self) -> str:
        return "N-Queens"
        
    @property
    def description(self) -> str:
        return "Places N queens on an NxN chessboard so that no two attack each other."
        
    @property
    def time_complexity(self) -> str:
        return "O(N!)"
        
    @property
    def space_complexity(self) -> str:
        return "O(N)"
        
    def solve(self, n: int) -> Iterator[NQueensState]:
        self.operations = 0
        board = [-1] * n # board[i] is the column position of the queen in row i
        
        # Initial empty state
        yield NQueensState(n=n, board=list(board), time_elapsed=0.0)
        
        yield from self._place_queens(board, 0, n)
        
        # Final solved state
        valid_queens = [(r, c) for r, c in enumerate(board) if c != -1]
        yield NQueensState(n=n, board=list(board), valid_queens=valid_queens, operations=self.operations, current_iteration=n)

    def _place_queens(self, board: List[int], row: int, n: int) -> Iterator[NQueensState]:
        if row >= n:
            return # A valid solution has been built incrementally
            
        for col in range(n):
            self.operations += 1
            
            # Show checking the square
            valid_queens = [(r, c) for r, c in enumerate(board[:row])]
            yield NQueensState(
                n=n,
                board=list(board),
                checking=(row, col),
                valid_queens=valid_queens,
                operations=self.operations,
                current_iteration=row
            )
            
            if self._is_safe(board, row, col):
                board[row] = col
                # Proceed to next row
                yield from self._place_queens(board, row + 1, n)
                # If we return and didn't solve everything, this path failed, backtrack
                
                # We do not strictly have to reset board[row] here unless we want to visualize it backtracking,
                # but setting it to -1 and yielding shows the "take back"
                # To simplify, we'll let the next column overwrite it or reset explicitly if we drop out
                
        # If no column worked, reset the row to -1 to visually remove the queen
        board[row] = -1
        valid_queens = [(r, c) for r, c in enumerate(board[:row])]
        yield NQueensState(
            n=n,
            board=list(board),
            valid_queens=valid_queens,
            operations=self.operations,
            current_iteration=row
        )

    def _is_safe(self, board: List[int], row: int, col: int) -> bool:
        """Check if placing a queen at (row, col) conflicts with already placed queens."""
        for r in range(row):
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True
