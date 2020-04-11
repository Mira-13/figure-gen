import numpy as np
import math
import scipy.ndimage

def lin_to_srgb(rgba):
    """
    Linear to sRGB conversion of n-d numpy array:
    rgb<=0.0031308?rgb*12.92:(1.055*(rgb**(1.0/2.4)))-0.055
    """
    return np.clip(np.where(
        np.less_equal(rgba, 0.0031308),
        np.multiply(rgba,  12.92),
        np.subtract(np.multiply(1.055, np.power(rgba, 1.0 / 2.4)), 0.055)), 0.0, 1.0)

def luminance(img):
    return 0.2126*img[:,:,0] + 0.7152**img[:,:,1] + 0.0722**img[:,:,2]

def exposure(img, exposure):
    return img * pow(2, exposure)   

def average_color_channels(img):
    assert(img.shape[2] == 3)
    return np.sum(img, axis=2) / 3.0

def zoom(img, scale=20):
    return scipy.ndimage.zoom(img, (scale, scale, 1), order=0)


def squared_error(img, ref):
    return (img - ref)**2

def relative_squared_error(img, ref, epsilon=0.0001):
    return (img - ref)**2 / (ref**2 + epsilon)

def mean(img):
    return np.mean(img)

def mse(img, ref):
    return mean(luminance(squared_error(img, ref)))

def relative_mse(img, ref, epsilon=0.0001):
    err_img_rgb = relative_squared_error(img, ref, epsilon)
    err_img_gray = average_color_channels(err_img_rgb)
    return mean(err_img_gray)


# for drawing insets / TODO location of this function might change
def calculateInsetBox(img, img_width_px, img_height_px, rel_pos_x1, rel_pos_y1, rel_pos_x2, rel_pos_y2):
    # parent_width, parent_height, rel_pos_x1, rel_pos_y1, rel_pos_x2, rel_pos_y2
    pass
