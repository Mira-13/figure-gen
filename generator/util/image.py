import numpy as np
import math
import scipy.ndimage

class Error(Exception):
    def __init__(self, message):
        self.message = message

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
    return 0.2126*img[:,:,0] + 0.7152*img[:,:,1] + 0.0722*img[:,:,2]

def exposure(img, exposure):
    return img * pow(2, exposure)

def average_color_channels(img):
    assert(img.shape[2] == 3)
    return np.sum(img, axis=2) / 3.0

def zoom(img, scale=20):
    return scipy.ndimage.zoom(img, (scale, scale, 1), order=0)

def crop(img, crop_args):
    '''
    crop_args: list of 4 elements: left, top, width, height.
    '''
    left, top = crop_args[0], crop_args[1]
    width, height = crop_args[2], crop_args[3]

    # check if out of bounds
    img_width = img.shape[1]
    img_height = img.shape[0]
    if img_width < left + width:
        raise Error("Incorrect usage of 'crop' function. Crop is out of bounds: image width < left offset + crop width.")
    if img_height < top + height:
        raise Error("Incorrect usage of 'crop' function. Crop is out of bounds: image height < top offset + crop height.")

    return img[top:top+height,left:left+width,:]

def scale_and_convert_rgb(rgb_list, scale=255):
    r = round(rgb_list[0] * 1/scale, 2)
    g = round(rgb_list[1] * 1/scale, 2)
    b = round(rgb_list[2] * 1/scale, 2)
    return '{'+str(r)+","+str(g)+","+ str(b)+'}'


def squared_error(img, ref):
    return (img - ref)**2

def relative_squared_error(img, ref, epsilon=0.0001):
    return (img - ref)**2 / (ref**2 + epsilon)

def mse(img, ref):
    return np.mean(luminance(squared_error(img, ref)))

def remove_outliers(error_img):
    f = 0.0001
    errors = np.sort(error_img)
    n = errors.size
    e = errors[0:n-int(n*f)] # ignore fireflies
    return np.mean(e)

def relative_mse(img, ref, epsilon=0.0001):
    err_img_rgb = relative_squared_error(img, ref, epsilon)
    err_img_gray = average_color_channels(err_img_rgb)
    return remove_outliers(err_img_gray)

def sape(img, ref):
    ''' Computes the symmetric absolute precentage error
    '''
    err = np.absolute(ref - img)
    normalizer = np.absolute(img) + np.absolute(ref)
    mask = normalizer != 0
    err[mask] /= normalizer[mask]
    return err

def smape(img, ref):
    ''' Computes the symmetric mean absolute percentage error
    '''
    return np.average(sape(img,ref))