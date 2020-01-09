from src.terrain import Terrain
import numpy as np


config = {
        "normalization_range": [0, 1],
        'shape': [8, 1],
        'height_map': [
            {
                "noise_variant": "ridge",
                "octaves": [
                    [3, 3]
                ],
                "elevation_distribution": [1],
                "noise_exp": 1
            },
        ],
        'moisture_map': [
            {
              "noise_variant": "simplex",
              "octaves": [
                [3, 3]
              ],
              "elevation_distribution": [5],
              "noise_exp": 1
            },
        ],
        'biomes': [
            ('WATER', (30, 144, 255)),
            ('BEACH', (255, 255, 102)),
            ('DESERT', (255, 255, 102)),
            ('GRASSLAND', (154, 205, 50)),
            ('FOREST', (34, 139, 34)),
            ('TAIGA', (46, 139, 87)),
            ('SNOW', (224, 255, 255)),
        ],
        'biome_thresholds': [
            (0.6, [(1., 'WATER')]),
            (0.63, [(1., 'BEACH')]),
            (0.8, [(0.2, 'DESERT'), (0.7, 'GRASSLAND'), (1., 'FOREST')]),
            (0.96, [(0.4, 'GRASSLAND'), (0.7, 'TAIGA'), (1., 'SNOW')]),
            (1, [(1, 'SNOW')]),
        ]
    }


def test_config_property():
    terrain = Terrain(0, config)
    tmp_config = terrain.config
    tmp_config['normalization_range'] = [0, 2]
    assert tmp_config != terrain.config


def test_biomes():

    terrain = Terrain(0, config)

    height_map = np.asarray(
        [[
            0.5,
            0.60000000001,
            0.7,
            0.799999999999999,
            0.631,
            0.95,
            0.96,
            0.81,
            1.
        ]],
        dtype=float
    )
    moisture_map = np.asarray(
        [[
            1.,
            0.111,
            0.,
            0.6,
            0.71,
            0.4,
            0.69,
            0.71,
            0.1
        ]],
        dtype=float
    )

    moisture_map = np.transpose(moisture_map)
    height_map = np.transpose(height_map)
    biome_map = terrain.get_biome_map(height_map, moisture_map)
    assert biome_map[0][0] == 'WATER'
    assert biome_map[1][0] == 'BEACH'
    assert biome_map[2][0] == 'DESERT'
    assert biome_map[3][0] == 'GRASSLAND'
    assert biome_map[4][0] == 'FOREST'
    assert biome_map[5][0] == 'GRASSLAND'
    assert biome_map[6][0] == 'TAIGA'
    assert biome_map[7][0] == 'SNOW'
    assert biome_map[8][0] == 'SNOW'
