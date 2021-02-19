from typing import Tuple, List
import numpy as np

from . import image
from .. import figuregen

class CropComparison:
    """ Matrix of cropped and zoomed images next to a reference image.

    Derived classes can change some behaviour, like the choice of error metric, by overriding the
    corresponding methods.

    Additional content can be added (or removed) by the user simply by accessing the individual
    grids in the generated list of grids.
    """
    def __init__(self, reference_image, method_images, crops: List[image.Cropbox],
                 scene_name = None, method_names = None, use_latex = False):
        """ Shows a reference image next to a grid of crops from different methods.

        Args:
            reference_image: a reference image (or any other image to put full-size in the lefthand grid)
            method_images: list of images, each corresponds to a new column in the crop grid
            crops: list of crops to take from each method, each creates a new row and a marker on the reference
            scene_name: [optional] string, name of the scene to put underneath the reference image
            method_names: [optional] list of string, names for the reference and each method, to put above the crops
            use_latex: set to true to pretty-print captions with LaTeX commands (requires TikZ backend)

        Returns:
            A list of two grids:
            The first is a single image (reference), the second a series of crops, one or more for each method.
        """
        self._reference_image = reference_image
        self._method_images = method_images
        self.use_latex = use_latex

        self._errors = [
            self.compute_error(reference_image, m)
            for m in method_images
        ]
        self._crop_errors = [
            [
                self.compute_error(crop.crop(reference_image), crop.crop(m))
                for m in method_images
            ]
            for crop in crops
        ]

        # Create the grid for the reference image
        self._ref_grid = figuregen.Grid(1, 1)
        self._ref_grid[0, 0].set_image(self.tonemap(reference_image))
        for crop in crops:
            self._ref_grid[0, 0].set_marker(crop.marker_pos, crop.marker_size, color=[255,255,255])

        if scene_name is not None:
            self._ref_grid.set_col_titles("bottom", [scene_name])

        # Create the grid with the crops
        self._crop_grid = figuregen.Grid(num_cols=len(method_images) + 1, num_rows=len(crops))
        for row in range(len(crops)):
            self._crop_grid[row, 0].set_image(self.tonemap(crops[row].crop(reference_image)))
            for col in range(len(method_images)):
                self._crop_grid[row, col + 1].set_image(self.tonemap(crops[row].crop(method_images[col])))

        # Put error values underneath the columns
        error_strings = [ f"{self.error_metric_name}" ]
        error_strings.extend([ self.error_string(i, self.errors) for i in range(len(self.errors)) ])
        self._crop_grid.set_col_titles("bottom", error_strings)
        self._crop_grid.layout.set_padding(column=1, row=1)
        self._crop_grid.layout.set_col_titles("bottom", fontsize=8, field_size_mm=2.8, offset_mm=0.5)

        # If given, show method names on top
        if method_names is not None:
            self._crop_grid.set_col_titles("top", method_names)
            self._crop_grid.layout.set_col_titles("top", fontsize=8, field_size_mm=2.8, offset_mm=0.25)

        self._ref_grid.copy_layout(self._crop_grid)
        self._ref_grid.layout.set_padding(right=1)

    def tonemap(self, img):
        return figuregen.JPEG(image.lin_to_srgb(img), quality=80)

    @property
    def error_metric_name(self) -> str:
        return "relMSE"

    def compute_error(self, reference_image, method_image) -> Tuple[str, List[float]]:
        return image.relative_mse(method_image, reference_image, 0.01)

    def error_string(self, index: int, errors: List[float]):
        """ Generates the human-readable error string for the i-th element in a list of error values.

        Args:
            index: index in the list of errors
            errors: list of error values, one per method, in order
        """
        if self.use_latex and index == np.argmin(errors):
            return f"$\\mathbf{{{errors[index]:.2f} ({errors[index]/errors[0]:.2f}\\times)}}$"
        elif self.use_latex:
            return f"${errors[index]:.2f} ({errors[index]/errors[0]:.2f}\\times)$"
        else:
            return f"{errors[index]:.2f} ({errors[index]/errors[0]:.2f}x)"

    @property
    def crop_errors(self) -> List[List[float]]:
        """ Error values within the cropped region of each method.
        First dimension is the crop, second the method.
        """
        return self._crop_errors

    @property
    def errors(self) -> List[float]:
        return self._errors

    @property
    def figure_row(self) -> List[figuregen.Grid]:
        return [ self._ref_grid, self._crop_grid ]
