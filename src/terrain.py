from simplex_noise import SimplexNoise
import common_tools
import constants
import numpy as np
from copy import deepcopy


class Terrain:
    def __init__(self, config, seed=constants.DEFAULT_SEED, shape=None, octave_stretch=None):
        self._seed = seed
        self._simplex_noise = SimplexNoise(seed)
        self._config = config
        # if passed, multiply all local octave settings by octave_stretch
        if octave_stretch is not None:
            if octave_stretch[0] < 0 or octave_stretch[1] < 0:
                raise ValueError("octave_stretch values cannot be less than 0")
            for tmp_height_map in self._config['height_map']:
                for tmp_octave in tmp_height_map['octaves']:
                    tmp_octave[0] *= octave_stretch[0]
                    tmp_octave[1] *= octave_stretch[1]
            for tmp_moisture_map in self._config['moisture_map']:
                for tmp_octave in tmp_moisture_map['octaves']:
                    tmp_octave[0] *= octave_stretch[0]
                    tmp_octave[1] *= octave_stretch[1]
        # assign shape from the argument to instance's config
        if shape is not None:
            self._config['shape'] = shape

        # if there is no shape settings given as an argument, set instance's shape to default value
        if 'shape' not in self._config:
            self._config['shape'] = constants.DEFAULT_SHAPE
        if self.shape[0] <= 0 or self.shape[1] <= 0:
            raise ValueError("shape values cannot be less than 0")

        self._terrain = {}
        self._generate_terrain()

    @property
    def config(self):
        return self._config.copy()  # we don't want the user to modify the config

    @config.setter
    def config(self, new_config):
        self._config = new_config
        self._generate_terrain()

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed
        # simplex noise instance must be dependent on local seed
        self._reset_simplex_noise()
        self._generate_terrain()

    @property
    def terrain(self):
        return self._terrain.copy()

    @property
    def moisture_map(self):
        return self._terrain['moisture_map'].copy()

    @property
    def height_map(self):
        return self._terrain['height_map'].copy()

    @property
    def shape(self):
        return deepcopy(self._config['shape'])

    def _reset_simplex_noise(self):
        self._simplex_noise = SimplexNoise(self._seed)

    def _calc_biome(self, h, m):  # h as height m as moisture
        t = self.config['biome_thresholds']
        for level in t:
            if level[0] >= h:
                for moisture in level[1]:
                    if moisture[0] >= m:
                        return moisture[1]
        return None

    def get_biome_map(self, height_map=None, moisture_map=None):
        if height_map is None:
            height_map = self._terrain['height_map']
        if moisture_map is None:
            moisture_map = self._terrain['moisture_map']
        if height_map.shape != moisture_map.shape:
            raise ValueError(
                f"height_map shape {height_map.shape} does not match moisture_map shape {moisture_map.shape}")
        shape = height_map.shape
        h = height_map
        m = moisture_map
        biome_map = np.zeros(shape, dtype=object)
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                biome_map[x][y] = self._calc_biome(h[x][y], m[x][y])
        return biome_map

    def get_color_map(self, biome_map=None):
        if biome_map is None:
            biome_map = self.get_biome_map()
        shape = biome_map.shape
        color_map = np.zeros([shape[0], shape[1], 3], dtype=np.uint8)
        biomes = self.config['biomes']
        for x in range(0, shape[0]):
            for y in range(0, shape[1]):
                if biome_map[x][y] is None:
                    color_map[x][y] = constants.NONE_COLOR
                else:
                    color_map[x][y] = biomes[biome_map[x][y]]
        return color_map

    def _generate_terrain(self):
        cfg = self._config
        shape = cfg['shape']

        if 'normalization_range' in cfg:
            normalization_range = cfg['normalization_range']
        else:
            normalization_range = constants.DEFAULT_NORMALIZATION_RANGE

        # if 'default_octaves_density' in cfg:
        #     multiplier = cfg['default_octaves_density']
        # else:
        #     multiplier = (1, 1)

        height_map = self._simplex_noise.gen_multi_noise_map(
            shape,
            cfg['height_map']
        )
        height_map = common_tools.normalize_np2d_array(height_map, normalization_range)
        moisture_map = self._simplex_noise.gen_multi_noise_map(
            shape,
            cfg['moisture_map']
        )
        moisture_map = common_tools.normalize_np2d_array(moisture_map, normalization_range)
        print(moisture_map)

        self._terrain = {
            'height_map': height_map,
            'moisture_map': moisture_map
        }
        # reset simplex noise seed so that next call of that method generates terrain dependent on seed
        self._reset_simplex_noise()

