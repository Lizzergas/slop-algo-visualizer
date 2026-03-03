import random
from typing import List

def random_list(size: int = 50, min_val: int = 10, max_val: int = 100) -> List[int]:
    """Generates a random list representing the average case."""
    return [random.randint(min_val, max_val) for _ in range(size)]

def reversed_list(size: int = 50, min_val: int = 10, max_val: int = 100) -> List[int]:
    """Generates an inversely sorted list, typically worst case for Insertion Sort."""
    arr = random_list(size, min_val, max_val)
    arr.sort(reverse=True)
    return arr

def nearly_sorted_list(size: int = 50, min_val: int = 10, max_val: int = 100, swaps: int = 3) -> List[int]:
    """Generates a list that is already sorted except for a few swapped elements."""
    arr = random_list(size, min_val, max_val)
    arr.sort()
    for _ in range(swaps):
        i, j = random.sample(range(size), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def few_unique_list(size: int = 50, options=(10, 50, 90)) -> List[int]:
    """Generates a list with many duplicate values."""
    return [random.choice(options) for _ in range(size)]

DATASETS = {
    "Random": random_list,
    "Reversed (Worst case for Insertion)": reversed_list,
    "Nearly Sorted (Best case for Insertion)": nearly_sorted_list,
    "Few Unique": few_unique_list,
}
