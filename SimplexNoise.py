import numpy as np
import random
import math
from opensimplex import OpenSimplex
import Constants
import CommonTools


class SimplexNoise:
    def __init__(self, seed=0):
        self._random = random.Random(seed)
        self._simplex_seed = 0
        self._open_simplex = OpenSimplex()
        self.shuffle_simplex_seed()

    @property
    def simplex_seed(self):
        return self._simplex_seed

    @simplex_seed.setter
    def simplex_seed(self, value):
        self._simplex_seed = value
        self._open_simplex = OpenSimplex(value)

    @property
    def open_simplex(self):
        return self._open_simplex

    @property
    def random(self):
        return self._random

    def shuffle_simplex_seed(self):
        self.simplex_seed = self.random.randint(0, Constants.MAX_SEED_VALUE)

    def simplex_noise(self, x, y, octaves=None, shape=None):
        if octaves is None or shape is None:
            point = self.open_simplex.noise2d(x, y)
        else:
            point = self.open_simplex.noise2d((x / shape[0]) * octaves[0], (y / shape[1]) * octaves[1])
        return point

    def ridge_noise(self, x, y, octaves=None, shape=None):
        return 2 * (0.5 - math.fabs(0.5 - self.simplex_noise(x, y, octaves, shape)))

    def generate_simplex_map(self, shape: tuple, octaves: list, elevation_distribution: list, noise_exp=1.,
                             ridge_noise_layers=0):
        elevation_n = len(octaves)

        if type(octaves) != list:
            raise TypeError(f"octaves is not a list")
        if type(elevation_distribution) != list:
            raise TypeError(f"elevation_distribution is not a list")
        if len(octaves) != len(elevation_distribution):
            raise ValueError(
                f"len(octaves) ({len(octaves)}) != len(elevation_distribution) ({len(elevation_distribution)})")
        if len(octaves) < ridge_noise_layers:
            raise ValueError(f"ridge_noise_layers value is too big ({ridge_noise_layers})")
        a = np.zeros(shape, dtype=float)

        for i in range(0, elevation_n):
            new_octaves = octaves[i]
            tmp = np.zeros(shape, dtype=float)
            self.shuffle_simplex_seed()
            for x in range(shape[0]):
                for y in range(shape[1]):
                    if i <= ridge_noise_layers - 1:
                        tmp[x][y] += elevation_distribution[i] * self.ridge_noise(x, y, new_octaves, shape)
                    else:
                        tmp[x][y] += elevation_distribution[i] * self.simplex_noise(x, y, new_octaves, shape)
            a += tmp
        a = CommonTools.normalize_np2d_array(a)
        for x in range(shape[0]):
            for y in range(shape[1]):
                a[x][y] = math.pow(a[x][y], noise_exp)
        return a
