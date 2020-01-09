import common_tools
from terrain import Terrain
import config
import json
import argparse
import image
from schema import Schema, And, Use, Optional, SchemaError


def generate_gif(seed, path):
    terrain_generator = Terrain(seed)
    tmp_config = terrain_generator.config

    i = 1
    while i < 2000:
        #print(tmp_config['moisture_map'][0]['noise_exp'])
        terrain_generator.seed = i
        color_map = terrain_generator.get_color_map()
        common_tools.export_image(color_map, path + f'/{i}.png')
        i += 1


if __name__ == "__main__":
    # get input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default=config.DEFAULT_CONFIG_PATH, type=str)
    parser.add_argument("--resolution", required=False, type=int, nargs="+")
    parser.add_argument("--output_path", default=config.DEFAULT_OUTPUT_PATH, type=str)
    parser.add_argument("--seed", default=config.DEFAULT_SEED, type=int)
    parser.add_argument("--grid", default=False, type=bool)

    args = parser.parse_args()

    with open(args.config_path) as json_file:
        world_conf = json.load(json_file)

    terrain = Terrain(config=world_conf, seed=args.seed, shape=args.resolution)
    color_map = terrain.get_color_map()
    img = image.create_image_from_color_map(color_map, args.grid)
    image.save_image(img, args.output_path)
    common_tools.plot2d(terrain.height_map)
    common_tools.plot2d(terrain.moisture_map, cmap='gray')
