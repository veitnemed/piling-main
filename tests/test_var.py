from src.experiments import calculate_variance, calculate_mean
import numpy as np

def test_variance():
    nums = np.arange(1,100, 1)
    assert np.var(nums, ddof = 1) == calculate_variance(nums)

    