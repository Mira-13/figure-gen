import cv2
import numpy as np

class Error(Exception):
    def __init__(self, message):
        self.message = message

class ElementData:    
    @property
    def aspect_ratio(self):
        pass

class Plot(ElementData): 
    @property
    def aspect_ratio(self):
        return self._aspect
    
    @aspect_ratio.setter
    def aspect_ratio(self, v):
        self._aspect = v

    def make_png(self, width, height, filename):
        raise NotImplementedError()

    def make_pdf(self, width, height, filename):
        raise NotImplementedError()

    def make_html(self, width, height, filename):
        raise NotImplementedError()

class Image(ElementData):
    @property
    def width_px(self):
        return None

    @property
    def height_px(self):
        return None

    @property
    def is_raster_image(self):
        pass

    @property
    def filename(self):
        pass

    def convert2png(self, out_filename):
        pass

class PDF(Image):
    '''
        Additional dependencies: PyPDF2 and pdf2image (requires poppler)
    '''
    def __init__(self, filename):
        self.file = filename

    @Image.aspect_ratio.getter
    def aspect_ratio(self):
        from PyPDF2 import PdfFileReader
        box = PdfFileReader(open(self.filename, "rb")).getPage(0).mediaBox
        width_pt = box.upperRight[0]
        height_pt = box.upperRight[1]
        return float(float(height_pt) / float(width_pt))

    @Image.is_raster_image.getter
    def is_raster_image(self):
        return False

    @Image.filename.getter
    def filename(self):
        return self.file

    def convert2png(self, out_filename, dpi=1000):
        from pdf2image import convert_from_path
        images = convert_from_path(self.file, dpi=dpi)
        img = np.array(images[0])
        cv2.imwrite(out_filename.replace('.pdf', '.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        return out_filename.replace('.pdf', '.png')

class PNG(Image):
    def __init__(self, raw_image_or_filename):
        '''
            Either provide raw image data OR a filename.
        '''
        if isinstance(raw_image_or_filename, str):
            self.file = raw_image_or_filename
            self.raw = None
            img = cv2.imread(self.file)
            self.width = img.shape[1]
            self.height = img.shape[0]
        else:
            self.file = None
            self.raw = raw_image_or_filename
            self.width = self.raw.shape[1]
            self.height = self.raw.shape[0]

    @Image.width_px.getter
    def width_px(self):
        return self.width

    @Image.height_px.getter
    def height_px(self):
        return self.height

    @Image.aspect_ratio.getter
    def aspect_ratio(self):
        return float(self.height / float(self.width))

    @Image.is_raster_image.getter
    def is_raster_image(self):
        return (self.file is None)

    @Image.filename.getter
    def filename(self):
        return self.file

    def convert2png(self, out_filename, dpi=1000):
        if self.raw is None:
            raise Error('This PNG cannot be converted nor exported to png.')
        clipped = self.raw*255
        clipped[clipped < 0] = 0
        clipped[clipped > 255] = 255
        cv2.imwrite(out_filename, cv2.cvtColor(clipped.astype('uint8'), cv2.COLOR_RGB2BGR))


class HTML(Image):
    def __init__(self, filename, aspect_ratio):
        self.file = filename
        self.a_ratio = float(aspect_ratio)

    @Image.aspect_ratio.getter
    def aspect_ratio(self):
        return self.a_ratio

    @Image.is_raster_image.getter
    def is_raster_image(self):
        return False

    @Image.filename.getter
    def filename(self):
        return self.file

    def convert2png(self, out_filename, dpi=1000):
        raise NotImplementedError()