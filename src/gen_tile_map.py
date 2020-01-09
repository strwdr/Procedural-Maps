import common_tools
from terrain import Terrain
import constants
import json
import argparse
import image
from schema import Schema, And, Use, Optional, SchemaError


if __name__ == "__main__":
    # get input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", default=constants.DEFAULT_CONFIG_PATH, type=str)
    parser.add_argument("--resolution", required=False, type=int, nargs="+")
    parser.add_argument("--octave_stretch", required=False, type=float, nargs="+")
    parser.add_argument("--output_path", default=constants.DEFAULT_OUTPUT_PATH, type=str)
    parser.add_argument("--seed", default=constants.DEFAULT_SEED, type=int)
    parser.add_argument('--grid', dest='grid', action='store_true')
    parser.add_argument('--no_grid', dest='grid', action='store_false')
    parser.set_defaults(grid=False)
    args = parser.parse_args()

    with open(args.config_path) as json_file:
        world_conf = json.load(json_file)

    print(args.octave_stretch)
    terrain = Terrain(config=world_conf, seed=args.seed, shape=args.resolution, octave_stretch=args.octave_stretch)
    color_map = terrain.get_color_map()
    img = image.create_image_from_color_map(color_map, args.grid)
    print(args.output_path)
    image.save_image(img, args.output_path)
    common_tools.plot2d(terrain.height_map)
    common_tools.plot2d(terrain.moisture_map, cmap='gray')
