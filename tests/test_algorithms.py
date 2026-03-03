import pytest
from src.datasets.generators import random_list, reversed_list, nearly_sorted_list, few_unique_list
from src.algorithms.factory import AlgorithmFactory

@pytest.mark.parametrize("algo_name", AlgorithmFactory.get_available_algorithms())
def test_algorithm_sorts_correctly(algo_name):
    algo = AlgorithmFactory.get_algorithm(algo_name)
    
    # Test on various datasets
    for generator in [random_list, reversed_list, nearly_sorted_list, few_unique_list]:
        original_array = generator(size=20)
        expected = sorted(original_array)
        
        # Run generator to completion
        generator_states = algo.sort(original_array)
        final_state = None
        for state in generator_states:
            final_state = state
            
        assert final_state is not None
        assert final_state.array == expected, f"{algo_name} failed on dataset."
