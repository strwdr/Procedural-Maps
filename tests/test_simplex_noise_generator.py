import pytest
from SimplexNoise import SimplexNoise as sng
import CommonTools
import numpy as np
import random

random.seed(1000)


def test_normalization():
    for t in range(100):
        a = random.randint(1, 1000)
        b = random.randint(a + 1, 1001)
        down = min(a, b)
        up = max(a, b)
        shape = (300, 300)
        test_array = np.zeros(shape, dtype=float)
        test_array[1][1] = 1
        test_array[100][100] = 100
        test_array = CommonTools.normalize_np2d_array(test_array, down, up)
        max_value = np.amax(test_array)
        min_value = np.amin(test_array)
        assert max_value == up
        assert min_value == down

