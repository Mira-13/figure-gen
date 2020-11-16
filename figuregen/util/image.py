import numpy as np
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

class Cropbox:
    def __init__(self, top, left, height, width, scale=1):
        self.top = top
        self.left = left
        self.bottom = top + height
        self.right = left + width
        self.height = height
        self.width = width
        self.scale = scale

    def crop(self, image):
        c = crop(image, [self.left, self.top, self.width, self.height])
        return zoom(c, self.scale)

    def get_marker_pos(self):
        return [self.left, self.top]

    def get_marker_size(self):
        return [self.right - self.left, self.bottom - self.top]

class SplitImage:
    def __init__(self, list_img, vertical=True, degree=15, weights=None):
            '''
            This class allows to split several images and make one image out of them.
            The weights define how much space each image will take within that new image,
            and the degree along with vertical (boolean) decides how these images are split.
            Returns one raw image data.

            args:
                list_img (list of image arrays): at best provide two or three images. 
                    You can provide more (but it might look ugly).
                degree (integer): A value between -45° and 45°.
                vertical (boolean): Either uses a vertical or horizontal splitting.
                weights (list of floats): Matches the weights to each image in list_img. 
            '''
            self.degree = degree
            if self.degree > 45 or self.degree < -45:
                print('Warning: SplitImage should get a degree between -45° and 45°, else the weights might not work like intended.' /
                'You might want to switch vertical from True to False or reverse.')
            self.is_vertical = vertical
            self.num_img = len(list_img)
            if self.num_img <= 1:
                raise Error('You provided too few images (less than 2), which means, \
            there is nothing to split.')

            self.weights = self._normalize_weights(weights)
            self.img_width = list_img[0].shape[1]
            self.img_height = list_img[0].shape[0]
            self.split_image = np.tile([x / 255 for x in [0,0,0]], (self.img_height, self.img_width, 1))
            # self.degree_rad = degree * np.pi / 180.0
            self.tan_degree_rad = np.tan(degree * np.pi / 180.0)

            self.start_pos = []
            self.end_pos = []
            self._make_split_image(list_img)

    def _calculate_default_weights(self):
        scale = 1.0 + int(self.degree / 10) * 0.25
        weights = np.zeros(self.num_img)
        weights.fill(scale)
        weights[0] = 1.0
        weights[-1] = 1.0
        return weights

    def _normalize_weights(self, weights):
        if weights is None:
            weights = self._calculate_default_weights()
        elif len(weights) != self.num_img:
            raise Error("Each image needs it's own weight. Please make sure that the length of the list \
        containing weights is as long as the number of images.")

        # normalize weight scaling
        weights /= np.sum(weights)
        return weights

    def _make_split_image(self, list_img):
        if not self.is_vertical:
            cur_pos = 0
            for i in range(len(list_img)):
                for col in range(self.img_width):
                    rel_w = float(self.img_width) * 0.5 - col
                    offset = self.tan_degree_rad * rel_w

                    if i == 0:
                        start = 0
                    else:
                        start = int(cur_pos + offset)
                    
                    if i == len(list_img) - 1:
                        end = self.img_height
                    else:
                        end = int(cur_pos + self.weights[i] * self.img_height + offset)
                    
                    start = max(0, start)
                    end = min(self.img_height, end)

                    # save start and end position to draw a line between images
                    self.split_image[start:end, col] = list_img[i][start:end, col]
                    if col == 0 and start != 0.:
                        self.start_pos.append((start, col))
                    if col == self.img_width-1 and end != self.img_height:
                        self.end_pos.append((end, col))
                
                cur_pos += self.weights[i] * self.img_height

        else:
            cur_pos = 0
            for i in range(len(list_img)):
                for row in range(self.img_height):
                    rel_h = float(self.img_height) * 0.5 - row
                    offset = self.tan_degree_rad * rel_h

                    if i == 0:
                        start = 0
                    else:
                        start = int(cur_pos + offset)

                    if i == len(list_img) - 1:
                        end = self.img_width
                    else:
                        end = int(cur_pos + self.weights[i] * self.img_width + offset)

                    start = max(0, start)
                    end = min(self.img_width, end)

                    self.split_image[row,start:end] = list_img[i][row,start:end]

                    

                cur_pos += self.weights[i] * self.img_width

    def get_image(self):
        return self.split_image

    def get_start_positions(self):
        cur_pos = 0
        positions = []
        if not self.is_vertical:
            for i in range(1, self.num_img):
                cur_pos += self.weights[i-1] * self.img_height
                offset = self.tan_degree_rad * (float(self.img_width) * 0.5)
                r = int(cur_pos + offset)
                c = 0
                positions.append((r, c))
            return positions
        for i in range(1, self.num_img):
            cur_pos += self.weights[i-1] * self.img_width
            offset = self.tan_degree_rad * (float(self.img_height) * 0.5)
            c = int(cur_pos + offset)
            r = 0
            positions.append((r, c))
        return positions

    def get_end_positions(self):
        cur_pos = 0
        positions = []
        if not self.is_vertical:
            for i in range(1,self.num_img):
                cur_pos += self.weights[i-1] * self.img_height
                offset = self.tan_degree_rad * (float(self.img_width) * 0.5)
                r = int(cur_pos - offset)
                c = self.img_width
                positions.append((r, c))
            return positions
        for i in range(1,self.num_img):
            cur_pos += self.weights[i-1] * self.img_width
            offset = self.tan_degree_rad * (float(self.img_height) * 0.5)
            c = int(cur_pos - offset)
            r = self.img_height
            positions.append((r, c))
        return positions

    def get_weights(self):
        return self.weights


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

def remove_outliers(error_img, percentage):
    errors = np.sort(error_img.flatten())
    num_outliers = int(errors.size * 0.01 * percentage)
    e = errors[0:errors.size-num_outliers]
    return np.mean(e)

def relative_mse(img, ref, epsilon=0.0001):
    err_img_rgb = relative_squared_error(img, ref, epsilon)
    err_img_gray = average_color_channels(err_img_rgb)
    return np.mean(err_img_gray)

def relative_mse_outlier_rejection(img, ref, epsilon=0.0001, percentage=0.1):
    err_img_rgb = relative_squared_error(img, ref, epsilon)
    err_img_gray = average_color_channels(err_img_rgb)
    return remove_outliers(err_img_gray, percentage)

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