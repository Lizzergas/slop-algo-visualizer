import psutil
import time
from typing import List, Tuple

class SystemMonitor:
    """Tracks CPU and Memory usage dynamically."""
    
    def __init__(self):
        self.process = psutil.Process()
        # Initial call to cpu_percent to set the baseline
        self.process.cpu_percent()
        
        self.history_time: List[float] = []
        self.history_cpu: List[float] = []
        self.history_memory: List[float] = [] # Memory in MB
        
        self.start_time = time.perf_counter()

    def tick(self) -> Tuple[float, float]:
        """
        Records the current CPU and memory usage and returns them.
        Returns: (cpu_percent, memory_mb)
        """
        current_time = time.perf_counter() - self.start_time
        cpu_percent = self.process.cpu_percent()
        
        # Resident Set Size (RSS) in Megabytes
        memory_mb = self.process.memory_info().rss / (1024 * 1024)
        
        self.history_time.append(current_time)
        self.history_cpu.append(cpu_percent)
        self.history_memory.append(memory_mb)
        
        return cpu_percent, memory_mb
