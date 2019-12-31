import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image


def export_image(color_map, path):
    color_map = np.swapaxes(color_map,0,1)
    img = Image.fromarray(color_map, 'RGB')
    img.save(path)


def cut_values_below_level(g, level):
    return np.where(g > level, g, level)


def normalize_np2d_array(norm, down=0, up=1):  # m as map
    if up <= down:
        raise ValueError(f"up ({up}) must be bigger tha down ({down})")
    diff = up - down
    ret = (norm - np.min(norm)) / np.ptp(norm)  # scale array values to 0:1
    ret *= diff
    ret += down
    return ret


def island_mask(height_map, center, radius):
    shape = height_map.shape
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            dist = math.sqrt(((x - center[0]) ** 2 + (y - center[1]) ** 2))
            diff = max(radius - dist, 0.)
            ratio = diff / radius
            height_map[x][y] = (-1 + height_map[x][y] + ratio) / 2
    height_map = normalize_np2d_array(height_map)
    return height_map


def plot3d(a):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = np.arange(0, a.shape[0], 1)
    y = np.arange(0, a.shape[1], 1)
    x, y = np.meshgrid(x, y)
    z = a[x, y]
    surf = ax.plot_surface(x, y, z, cmap='gist_earth', linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def plot2d(a, cmap='gist_earth'):
    plt.figure()
    plt.imshow(a, cmap=cmap, interpolation='none')
    plt.colorbar()
    plt.show()

