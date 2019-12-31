from SimplexNoise import SimplexNoise
import random
import Constants
import CommonTools
import json
import numpy as np


class Terrain:
    def __init__(self, seed=0, config=None):
        self._seed = seed
        self._random = random.Random(seed)
        self._simplex_noise = SimplexNoise(self.random.randint(0, Constants.MAX_SEED_VALUE))
        if config is None:
            with open('config.json') as json_file:
                data = json.load(json_file)
            self._config = data
        else:
            self._config = config

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
                if biome_map[x][y] is None:
                    color_map[x][y] = Constants.NONE_COLOR
                else:
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
            noise_exp=hm_cfg['noise_exp'],
            ridge_noise_layers=hm_cfg['ridge_noise_layers']
        )
        mm_cfg = self.config['moisture_map']

        moisture_map = self.simplex_noise.generate_simplex_map(
            shape=cfg['shape'],
            octaves=mm_cfg['octaves'],
            elevation_distribution=mm_cfg['elevation_distribution'],
            noise_exp=mm_cfg['noise_exp'],
            ridge_noise_layers=mm_cfg['ridge_noise_layers']
        )

        biome_map = self.generate_biome_map(height_map, moisture_map)
        color_map = self.generate_color_map(biome_map)
        CommonTools.export_image(color_map, 't2.png')
        CommonTools.plot2d(height_map)
        CommonTools.plot2d(moisture_map, cmap='gray')
