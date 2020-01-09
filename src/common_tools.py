import numpy as np
import matplotlib.pyplot as plt
import config


def normalize_np2d_array(array, normalization_range=config.DEFAULT_NORMALIZATION_RANGE):
    """Returns normalized two-dimensional numpy array of floats


    Keyword arguments:
    array -- numpy 2d array (float dtype)
    normalization_range -- float tuple, desired normalization range, for (a, b) a is the down boundary, b is the upper
    boundary
    """
    down = normalization_range[0]
    up = normalization_range[1]
    if up <= down:
        raise ValueError(f"up ({up}) must be bigger than down ({down})")
    diff = up - down
    if np.min(array) == np.max(array):
        ret = np.zeros(array.shape, dtype=float)
    else:
        ret = (array - np.min(array)) / np.ptp(array)  # scale array values
    ret *= diff
    ret += down
    return ret


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
