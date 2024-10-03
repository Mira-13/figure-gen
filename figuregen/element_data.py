import shutil
import os
import base64
import simpleimageio
import numpy as np
import tempfile

class Error(Exception):
    def __init__(self, message):
        self.message = message

class ElementData:
    @property
    def aspect_ratio(self):
        """ Aspect ratio (height / width) of the grid element. """
        pass

    def make_raster(self, width, height, base_filename) -> str:
        ''' Writes the element to a raster file format (e.g, .png, .jpg)

        This function should always be implemented. All backends use it as the fallback option.
        The exact file format is implementation specific and might be controlled by the user.

        Args:
            width: Desired width of the image in [mm]
            height: Desired height of the image in [mm]
            base_filename: Backend-generated filename prefix that can be used to generate a unique file
                in the correct location

        Returns:
            The filename of the generated file.
        '''
        raise NotImplementedError()

    def make_pdf(self, width, height, base_filename) -> str:
        ''' Writes the element to a .pdf file.

        Args:
            width: Desired width of the image in [mm]
            height: Desired height of the image in [mm]
            base_filename: Backend-generated filename prefix that can be used to generate a unique file
                in the correct location

        Returns:
            The filename of the generated file.
        '''
        raise NotImplementedError()

    def make_html(self, width, height) -> str:
        ''' Writes the element to a static .html page, images should be embedded as base64.

        The default generates a raster image in a temporary file and encodes it as base64 .png

        Args:
            width: Desired width of the image in [mm]
            height: Desired height of the image in [mm]

        Returns:
            The generated inline html code.
        '''
        temp_folder = tempfile.TemporaryDirectory()
        fname = self.make_raster(width, height, os.path.join(temp_folder.name, "image"))
        with open(fname, "rb") as f:
            b64 = base64.b64encode(f.read())
        temp_folder.cleanup()

        html = "<img src='data:image/png;base64," + b64.decode('utf-8')
        html += f"' style='width: {width}mm; height: {height}mm;' />"
        return html

class Plot(ElementData):
    ''' Base class for all generated images and plots.

    Offers a user-controllable aspect ratio
    '''
    @property
    def aspect_ratio(self):
        return self._aspect

    @aspect_ratio.setter
    def aspect_ratio(self, v):
        self._aspect = v

class Image(ElementData):
    @property
    def width_px(self):
        raise NotImplementedError()

    @property
    def height_px(self):
        raise NotImplementedError()

class PDF(Image):
    ''' Loads and embeds the first page of a pdf file.

    Additional dependencies: pypdf and pdf2image (the latter requires poppler to be installed and in the PATH)
    '''
    def __init__(self, filename, dpi=300, use_jpeg=False):
        self.file = filename
        self.dpi = dpi
        self.ext = '.jpg' if use_jpeg else '.png'
        self.mimetype = 'data:image/jpeg;base64,' if use_jpeg else 'data:image/png;base64,'

    @Image.aspect_ratio.getter
    def aspect_ratio(self):
        from pypdf import PdfReader
        box = PdfReader(open(self.file, "rb")).pages[0].mediabox
        width_pt = box.upper_right[0]
        height_pt = box.upper_right[1]
        return float(float(height_pt) / float(width_pt))

    def convert(self):
        from pdf2image.pdf2image import convert_from_path
        images = convert_from_path(self.file, dpi=self.dpi, last_page=1)
        return np.array(images[0]) / 255

    def make_raster(self, width, height, base_filename) -> str:
        img = self.convert()
        simpleimageio.write(base_filename + self.ext, simpleimageio.srgb_to_lin(img))
        return base_filename + self.ext

    def make_pdf(self, width, height, base_filename) -> str:
        shutil.copy(self.file, base_filename + ".pdf")
        return base_filename + ".pdf"

class RasterImage(Image):
    ''' Abstract base class for all supported raster image types. '''
    def __init__(self, raw_image_or_filename):
        '''
            Either provide raw image data OR a filename.
        '''
        assert raw_image_or_filename is not None

        if isinstance(raw_image_or_filename, str):
            self.file = raw_image_or_filename
            self.raw = simpleimageio.lin_to_srgb(simpleimageio.read(self.file))
            self.width = self.raw.shape[1]
            self.height = self.raw.shape[0]
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

    def convert(self, out_filename):
        simpleimageio.write(out_filename, simpleimageio.srgb_to_lin(self.raw))

class PNG(RasterImage):
    ''' A raster image that will be converted to .png '''
    def __init__(self, raw_image_or_filename):
        self.ext = ".png"
        RasterImage.__init__(self, raw_image_or_filename)

    def make_raster(self, width, height, base_filename) -> str:
        filename = base_filename + self.ext
        self.convert(filename)
        return filename

class JPEG(RasterImage):
    ''' A raster image that will be converted to .jpg '''
    def __init__(self, raw_image_or_filename, quality=85):
        self.ext = ".jpg"
        self.quality = quality
        RasterImage.__init__(self, raw_image_or_filename)

    def make_raster(self, width, height, base_filename) -> str:
        filename = base_filename + self.ext
        simpleimageio.write(filename, simpleimageio.srgb_to_lin(self.raw), self.quality)
        return filename

class HTML(Image):
    ''' Embeds a .html.

    Currently ownly useful to the HTML backend, as it does not render the webpage.
    '''
    def __init__(self, filename, aspect_ratio):
        self.file = filename
        self.a_ratio = float(aspect_ratio)

    @Image.aspect_ratio.getter
    def aspect_ratio(self):
        return self.a_ratio
