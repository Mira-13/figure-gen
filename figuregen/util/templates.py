from typing import Tuple, List
import numpy as np

from . import image
from .. import figuregen as fig

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
        self._ref_grid = fig.Grid(1, 1)
        self._ref_grid[0, 0].image = self.tonemap(reference_image)
        for crop in crops:
            self._ref_grid[0, 0].set_marker(crop.marker_pos, crop.marker_size, color=[255,255,255])

        if scene_name is not None:
            self._ref_grid.set_col_titles("bottom", [scene_name])

        # Create the grid with the crops
        self._crop_grid = fig.Grid(num_cols=len(method_images) + 1, num_rows=len(crops))
        for row in range(len(crops)):
            self._crop_grid[row, 0].image = self.tonemap(crops[row].crop(reference_image))
            for col in range(len(method_images)):
                self._crop_grid[row, col + 1].image = self.tonemap(crops[row].crop(method_images[col]))

        # Put error values underneath the columns
        error_strings = [ f"{self.error_metric_name}" ]
        error_strings.extend([ self.error_string(i, self.errors) for i in range(len(self.errors)) ])
        self._crop_grid.set_col_titles("bottom", error_strings)

        crop_layout = self._crop_grid.layout
        crop_layout.row_space = 1
        crop_layout.column_space = 1
        crop_layout.column_titles[fig.BOTTOM] = fig.TextFieldLayout(fontsize=8, size=2.8, offset=0.5)

        # If given, show method names on top
        if method_names is not None:
            self._crop_grid.set_col_titles("top", method_names)
            crop_layout.column_titles[fig.TOP] = fig.TextFieldLayout(fontsize=8, size=2.8, offset=0.25)

        self._ref_grid.copy_layout(self._crop_grid)
        self._ref_grid.layout.padding[fig.RIGHT] = 1

    def tonemap(self, img):
        return fig.JPEG(image.lin_to_srgb(img), quality=80)

    @property
    def error_metric_name(self) -> str:
        return "relMSE"

    def compute_error(self, reference_image, method_image) -> Tuple[str, List[float]]:
        return image.relative_mse(method_image, reference_image)

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
    def figure_row(self) -> List[fig.Grid]:
        return [ self._ref_grid, self._crop_grid ]

class FullSizeWithCrops:
    """ Side-by-side comparison of full-size images. Below each image is a row of crops.

    Derived classes can change some behaviour, like the choice of error metric, by overriding the
    corresponding methods.

    Additional content can be added (or removed) by the user simply by accessing the individual
    grids in the generated list of grids.
    """
    def __init__(self, reference_image, method_images, crops: List[image.Cropbox],
                 crops_below = True, method_names = None, use_latex = False):
        """ Shows a reference image next to a grid of crops from different methods.

        Args:
            reference_image: a reference image (or any other image to put full-size in the lefthand grid)
            method_images: list of images, each corresponds to a new column in the crop grid
            crops: list of crops to take from each method, each creates a new row and a marker on the reference
            crops_below: [optional] if False, the crops will be a column to the right of each image
            method_names: [optional] list of string, names for the reference and each method, to put above the crops
            use_latex: set to true to pretty-print captions with LaTeX commands (requires TikZ backend)

        Returns:
            A list of two grids:
            The first is a single image (reference), the second a series of crops, one or more for each method.
        """
        self._reference_image = reference_image
        self._method_images = method_images
        self.use_latex = use_latex
        self._crops_below = crops_below

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

        # Put in one list to make our life easier in the following
        images = [reference_image]
        images.extend(method_images)

        # Create the grid for the reference image
        self._ref_grid = [ fig.Grid(1, 1) for _ in range(len(images)) ]
        for i in range(len(images)):
            self._ref_grid[i][0, 0].image = self.tonemap(images[i])
            for crop in crops:
                self._ref_grid[i][0, 0].set_marker(crop.marker_pos, crop.marker_size, color=[255,255,255])

        # Create the grid with the crops
        if self._crops_below:
            self._crop_grid = [
                fig.Grid(num_cols=len(crops), num_rows=1)
                for _ in range(len(images))
            ]
            for i in range(len(images)):
                for col in range(len(crops)):
                    self._crop_grid[i][0, col].image = self.tonemap(crops[col].crop(images[i]))
        else:
            self._crop_grid = [
                fig.Grid(num_cols=1, num_rows=len(crops))
                for _ in range(len(images))
            ]
            for i in range(len(images)):
                for row in range(len(crops)):
                    self._crop_grid[i][row, 0].image = self.tonemap(crops[row].crop(images[i]))

        # Add padding to the right of all but the last image
        for i in range(len(images) - 1):
            self._ref_grid[i].layout.padding[fig.RIGHT] = 1
            self._crop_grid[i].layout.padding[fig.RIGHT] = 1
            if self._crops_below:
                self._ref_grid[i].layout.padding[fig.BOTTOM] = 1

        if self._crops_below:
            self._ref_grid[-1].layout.padding[fig.BOTTOM] = 1
        else:
            self._ref_grid[-1].layout.padding[fig.RIGHT] = 1

        # Put error values underneath the columns
        if self._crops_below:
            for i in range(len(images)):
                if i > 0:
                    err = self.error_string(i - 1, self.errors)
                else:
                    err = self.error_metric_name
                self._crop_grid[i].set_title("bottom", method_names[i] + "\\\\" + err)
                self._crop_grid[i].layout.titles[fig.BOTTOM] = fig.TextFieldLayout(size=6, offset=1, fontsize=8)
        else:
            pass # TODO

        # TODO this requires titles spanning multiple grids (the image and its crops)!
        # error_strings = [ f"{self.error_metric_name}" ]
        # error_strings.extend([ self.error_string(i, self.errors) for i in range(len(self.errors)) ])
        # self._crop_grid.set_col_titles("bottom", error_strings)
        # self._crop_grid.layout.set_padding(column=1, row=1)
        # self._crop_grid.layout.set_col_titles("bottom", fontsize=8, field_size_mm=2.8, offset_mm=0.5)

        # If given, show method names on top
        # TODO combine with error values, and always show both or neither
        # if method_names is not None:
        #     self._crop_grid.set_col_titles("top", method_names)
        #     self._crop_grid.layout.set_col_titles("top", fontsize=8, field_size_mm=2.8, offset_mm=0.25)

        # self._ref_grid.copy_layout(self._crop_grid)
        # self._ref_grid.layout.set_padding(right=1)
        # TODO set appropriate paddings for alignment etc

    def tonemap(self, img):
        return fig.JPEG(image.lin_to_srgb(img), quality=80)

    @property
    def error_metric_name(self) -> str:
        return "relMSE"

    def compute_error(self, reference_image, method_image) -> Tuple[str, List[float]]:
        return image.relative_mse(method_image, reference_image)

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
    def figure(self) -> List[List[fig.Grid]]:
        if self._crops_below:
            return [ self._ref_grid, self._crop_grid ]
        else:
            grids = []
            for i in range(len(self._method_images) + 1):
                grids.append(self._ref_grid[i])
                grids.append(self._crop_grid[i])
            return [ grids ]