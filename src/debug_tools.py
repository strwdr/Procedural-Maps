import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot3d(a):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(0, a.shape[0], 1)
    y = np.arange(0, a.shape[1], 1)
    x, y = np.meshgrid(x, y)
    z = a[x, y]
    surf = ax.plot_surface(x, y, z, cmap='gist_earth', linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def plot2d(a, cmap='gist_earth'):
    plt.figure()
    plt.imshow(np.swapaxes(a, 0, 1), cmap=cmap, interpolation='none')
    plt.colorbar()
    plt.show()
