from Terrain import Terrain


def test_calc_biome():
    terrain = Terrain(0)
    terrain.config['biomes'] =  [
            ('WATER', (30, 144, 255)),
            ('BEACH', (255, 255, 102)),
            ('DESERT', (255, 255, 102)),
            ('GRASSLAND', (154, 205, 50)),
            ('FOREST', (34, 139, 34)),
            ('TAIGA', (46, 139, 87)),
            ('SNOW', (224, 255, 255)),
            ('NONE', (0, 0, 0))
        ]

    terrain.config['biome_thresholds'] = [
            (0.6, [(1., 'WATER')]),
            (0.63, [(1., 'BEACH')]),
            (0.8, [(0.2, 'DESERT'), (0.7, 'GRASSLAND'), (1., 'FOREST')]),
            (0.96, [(0.4, 'GRASSLAND'), (0.7, 'TAIGA'), (1., 'SNOW')]),
            (1., [(1, 'SNOW')]),
        ]

    h, m = 0.5, 1.
    assert terrain.calc_biome(h, m) == 'WATER'
    h, m = 0.60000000001, 0.111
    assert terrain.calc_biome(h, m) == 'BEACH'
    h, m = 0.7, 0.
    assert terrain.calc_biome(h, m) == 'DESERT'
    h, m = 0.799999999999999, 0.6
    assert terrain.calc_biome(h, m) == 'GRASSLAND'
    h, m = 0.631, 0.71
    assert terrain.calc_biome(h, m) == 'FOREST'
    h, m = 0.95, 0.4
    assert terrain.calc_biome(h, m) == 'GRASSLAND'
    h, m = 0.96, 0.69
    assert terrain.calc_biome(h, m) == 'TAIGA'
    h, m = 0.81, 0.71
    assert terrain.calc_biome(h, m) == 'SNOW'
    h, m = 1., 0.1
    assert terrain.calc_biome(h, m) == 'SNOW'
