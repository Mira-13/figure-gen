import numpy as np

from simpleimageio import lin_to_srgb, luminance, exposure, average_color_channels, zoom

def crop(img, left, top, width, height):
    assert top >= 0 and left >= 0, "crop is outside the image"
    assert left + width <= img.shape[1], "crop is outside the image"
    assert top + height <= img.shape[0], "crop is outside the image"

    assert img.ndim == 2 or img.ndim == 3, "not an image"

    if img.ndim == 3:
        return img[top:top+height,left:left+width,:]
    elif img.ndim == 2:
        return img[top:top+height,left:left+width]

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
        c = crop(image, self.left, self.top, self.width, self.height)
        return zoom(c, self.scale)

    @property
    def marker_pos(self):
        return self.get_marker_pos()

    def get_marker_pos(self):
        return [self.left, self.top]

    @property
    def marker_size(self):
        return self.get_marker_size()

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
                list_img (list of image arrays): provide preferably two or three images.
                    You can provide more (but it might look ugly).
                degree (integer): A value between -45° and 45°.
                vertical (boolean): Either uses a vertical or horizontal splitting.
                weights (list of floats): Matches the weights to each image in list_img.
            '''
            self.degree = degree
            if self.degree > 45 or self.degree < -45:
                print(
                    'Warning: SplitImage should get a degree between -45° and 45°, else the weights might not work as intended. '
                    f'Try setting "vertical = {not vertical}" instead.'
                )
            self.is_vertical = vertical
            self.num_img = len(list_img)
            assert self.num_img > 1, "at least two images are required"

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

        assert len(weights) == self.num_img, "need one weight per image"

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

from simpleimageio import mse, relative_mse, relative_mse_outlier_rejection

def squared_error(img, ref):
    return (img - ref)**2

def relative_squared_error(img, ref, epsilon=0.0001):
    return (img - ref)**2 / (ref**2 + epsilon)

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