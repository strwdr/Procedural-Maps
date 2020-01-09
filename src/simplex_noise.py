import numpy as np
import random
import math
from opensimplex import OpenSimplex
import constants


class SimplexNoise:
    """Class responsible for creating noise maps"""
    def __init__(self, seed=0):
        self._random = random.Random(seed)
        self._seed = seed
        self._simplex_seed = 0
        self._open_simplex = OpenSimplex()
        self._shuffle_simplex_seed()  # make simplex seed dependent on local random instance

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self._random.seed(value)
        self._shuffle_simplex_seed()

    def _shuffle_simplex_seed(self):
        self._simplex_seed = self._random.randint(0, constants.MAX_SEED_VALUE)
        self._open_simplex = OpenSimplex(self._simplex_seed)

    def simplex_noise(self, x, y, octave=None, shape=None, noise_variant='simplex'):
        """Returns the value of two-dimensional simplex noise function for a point.
        By default, OpenSimplex noise2d method returns float in range (-1:1),
        that method converts it to (0:1).


        Keyword arguments:
        x -- the x coordinate of simplex function
        y -- the y coordinate of simplex function
        octaves -- a tuple of numbers of octaves in appropriate dimension of shape (x, y)
        shape -- a tuple of dimensions lengths (int, int)
        noise_variant -- a string that contains the information about the desired noise variant


        if both octaves and shape are passed, the method scales the coordinates so that the number of octaves in the
        given dimension will fit in the shape
        otherwise, the default OpenSimplex noise2d method is returned
        """
        if octave is None or shape is None:
            point = self._open_simplex.noise2d(x, y)
        else:
            point = self._open_simplex.noise2d((x / shape[0]) * octave[0], (y / shape[1]) * octave[1])
        point += 1.
        point /= 2
        if point < 0.:
            point = 0.
        if noise_variant == 'ridge':
            point = 2 * (0.5 - math.fabs(0.5 - self.simplex_noise(x, y, octave, shape)))
        elif noise_variant != 'simplex':
            raise ValueError(f"there is no such noise variant as {noise_variant}")
        return point

    def gen_noise_map(self, shape: tuple, octaves: list, elevation_distribution: list, noise_exp=1.,
                      noise_variant='simplex'):
        """Returns two-dimensional numpy array (float dtype) of combined noise maps.


        Keyword arguments:
        shape -- a dimension length tuple (int, int)
        octaves -- an array of tuples; for each layer, respectively, there is a tuple (float, float) with the number
        of octaves for both dimensions
        elevation_distribution -- an array of floats; for each layer, respectively, there is a multiplier by which the
        method multiplies the values ​​of all layers (noise maps) at the end
        noise_exp -- an exponent to which all the layers are raised (not negative float)
        noise_variant -- a string that contains the information about the desired noise variant
        """
        elevation_n = len(octaves)

        if type(octaves) != list:
            raise TypeError(f"octaves is not a list")
        if type(elevation_distribution) != list:
            raise TypeError(f"elevation_distribution is not a list")
        if len(octaves) != len(elevation_distribution):
            raise ValueError(
                f"len(octaves) ({len(octaves)}) != len(elevation_distribution) ({len(elevation_distribution)})")
        if noise_exp < 0:
            raise ValueError(f"noise_exp ({noise_exp}) cannot be less than 0")
        a = np.zeros(shape, dtype=float)
        for i in range(0, elevation_n):
            new_octave = octaves[i]
            tmp = np.zeros(shape, dtype=float)
            self._shuffle_simplex_seed()
            for x in range(shape[0]):
                for y in range(shape[1]):
                    tmp[x][y] += elevation_distribution[i] * self.simplex_noise(x, y, new_octave, shape, noise_variant)
            a += tmp
        for x in range(shape[0]):
            for y in range(shape[1]):
                a[x][y] = math.pow(a[x][y], noise_exp)
        return a

    def gen_multi_noise_map(self, shape, noise_map_kwargs_array):
        """Returns two-dimensional numpy array (float dtype) of combined noise maps.
        Combines as many independent noise maps created by the gen_noise_map() method,
        as many parameter dicts contain noise_map_kwargs_array


        Keyword arguments:
        shape -- a dimension length tuple (int, int)
        noise_map_kwargs_array -- an array of dictionaries of noise maps parameters
        """
        tmp_map = np.zeros(shape, dtype=float)
        for kwargs in noise_map_kwargs_array:
            tmp_map += self.gen_noise_map(shape, **kwargs)
        return tmp_map
