import numpy as np
import constants


def normalize_np2d_array(array, normalization_range=constants.DEFAULT_NORMALIZATION_RANGE):
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


