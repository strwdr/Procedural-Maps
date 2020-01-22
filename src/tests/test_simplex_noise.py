from simplex_noise import SimplexNoise
import random
import numpy

SEED = 1
INSTANCE = SimplexNoise(SEED)


def test_seed():
    assert INSTANCE.seed == SEED


def test_simplex_noise_static():
    for i in range(1000):
        simplex_noise = INSTANCE.simplex_noise(random.randint(-100, 100), random.randint(-100, 100))
        assert type(simplex_noise) == float
        assert simplex_noise >= 0
        assert simplex_noise <= 1


def test_simplex_noise_octaves():
    for i in range(1000):
        simplex_noise = INSTANCE.simplex_noise(random.randint(-100, 100), random.randint(-100, 100), (10, 10), (20, 20))
        assert type(simplex_noise) == float
        assert simplex_noise >= 0
        assert simplex_noise <= 1


def test_gen_noise_map():
    shape = (100, 100)
    octaves = [(10, 10), (2, 2)]
    elevation_distribution = [3, 1]
    noise_map = INSTANCE.gen_noise_map(shape=shape, octaves=octaves, elevation_distribution=elevation_distribution)
    assert type(noise_map) == numpy.ndarray
    assert noise_map.shape == shape
    assert noise_map.dtype == float

