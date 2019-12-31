from SimplexNoise import SimplexNoise
import random
import Constants
import CommonTools
import json
import numpy as np
from PIL import Image


class Terrain:
    def __init__(self, seed=0, config = None):
        self._seed = seed
        self._random = random.Random(seed)
        self._simplex_noise = SimplexNoise(self.random.randint(0, Constants.MAX_SEED_VALUE))
        if config is None:
            with open('config.json') as json_file:
                data = json.load(json_file)
            self._config = data
        else:
            self._config = config
        """
        self._config = {
            'shape': (500, 500),
            'height_map': {
                'octaves': [(2, 2),
                            (6, 6),
                            (10, 10),
                            (20, 20),
                            (40, 40),
                            (50, 50),
                            (100, 100),
                            (200, 200)],
                'elevation_distribution': [40, 20, 10, 10, 6, 5, 2, 1],
            },
            'moisture_map': {
                'octaves': [(5, 5),
                            (10, 10),
                            (20, 20),
                            (30, 30),
                            (50, 50)],

                'elevation_distribution': [10, 7, 4, 3, 2],
            },
            'biomes': {
                'WATER': (30, 144, 255),
                'BEACH': (255, 255, 102),
                'DESERT': (255, 255, 102),
                'GRASSLAND': (154, 205, 50),
                'FOREST': (34, 139, 34),
                'TAIGA': (46, 139, 87),
                'STONE': (169, 169, 169),
                'SNOW': (224, 255, 255),
            },
            'biome_thresholds': [
                (0.6, [(1., 'WATER')]),
                (0.63, [(0.2, 'STONE'), (1., 'BEACH')]),
                (0.8, [(0.2, 'DESERT'), (0.7, 'GRASSLAND'), (1., 'FOREST')]),
                (0.90, [(0.3, 'TAIGA'), (0.9, 'STONE'), (1., 'SNOW')]),

                (0.96, [(0.7, 'STONE'), (1., 'SNOW')]),
                (1., [(1, 'SNOW')]),
            ],
        }
        """

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, new_config):
        self._config = new_config

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if self._seed != value:
            self._seed = value
            self._random = random.Random(value)

    @property
    def random(self):
        return self._random

    @property
    def simplex_noise(self):
        return self._simplex_noise

    def calc_biome(self, h, m):  # h as height m as moisture
        t = self.config['biome_thresholds']
        for level in t:
            if level[0] >= h:
                for moisture in level[1]:
                    if moisture[0] >= m:
                        return moisture[1]
        return None

    def generate_biome_map(self, height_map, moisture_map):
        if height_map.shape != moisture_map.shape:
            raise ValueError(
                f"height_map shape {height_map.shape} does not match moisture_map shape {moisture_map.shape}")
        shape = height_map.shape
        h = height_map
        m = moisture_map
        biome_map = np.zeros(shape, dtype=object)
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                biome_map[x][y] = self.calc_biome(h[x][y], m[x][y])
        return biome_map

    def generate_color_map(self, biome_map):
        shape = biome_map.shape
        color_map = np.zeros([shape[0], shape[1], 3], dtype=np.uint8)
        biomes = self.config['biomes']
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                color_map[x][y] = biomes[biome_map[x][y]]
        return color_map

    def generate_terrain(self):
        a = json.dumps(self.config)
        print(a)
        cfg = self.config
        hm_cfg = self.config['height_map']
        height_map = self.simplex_noise.generate_simplex_map(
            shape=cfg['shape'],
            octaves=hm_cfg['octaves'],
            elevation_distribution=hm_cfg['elevation_distribution'],
        )
        mm_cfg = self.config['moisture_map']

        moisture_map = self.simplex_noise.generate_simplex_map(
            shape=cfg['shape'],
            octaves=mm_cfg['octaves'],
            elevation_distribution=mm_cfg['elevation_distribution'],
        )

        biome_map = self.generate_biome_map(height_map, moisture_map)
        color_map = self.generate_color_map(biome_map)
        CommonTools.export_image(color_map, 't.png')
        # CommonTools.plot3d(g)
        CommonTools.plot2d(height_map)
        CommonTools.plot2d(moisture_map, cmap='gray')
