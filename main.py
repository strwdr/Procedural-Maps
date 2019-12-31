import numpy as np
from SimplexNoise import SimplexNoise
import CommonTools
from Terrain import Terrain

if __name__ == "__main__":
    seed = 21121

    terrain_generator = Terrain(seed)
    terrain_generator.generate_terrain()
