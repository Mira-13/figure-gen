from dataclasses import dataclass, field
from typing import Sequence, Tuple

@dataclass
class TextFieldLayout:
    size: float = 0
    """ Size (height or width, depending on rotation) of this text field. In mm"""
    offset: float = 0
    """ Space between this field and the corresponding grid component (e.g., distance between an image and its caption), in mm """
    rotation: int = 0
    """ Counter clockwise rotation of the text in degrees. Some backends might only support +-90 """
    fontsize: float = 8
    """ Fontsize in pt """
    line_space: float = 1.2
    """ Line spacing for multi-line content, as a multiple of the font size """
    text_color: Tuple[float, float, float] = (0, 0, 0)
    """ Color (sRGB, from 0 to 255) of the text """
    background_colors: Sequence[Sequence[float]] | Sequence[float] | None = None
    """ Background colors (sRGB, from 0 to 255) of the text, can be a list of colors, e.g., one per row, or a single color that will be applied to all """
    vertical_alignment: str | None = None
    """ Vertical text alignment, must be one of: "top", "bottom", "center"; If None, the default alignment based on the type of text field is used """
    horizontal_alignment: str = "center"
    """ Horizontal text alignment, must be one of: "left", "right", "center" """

TOP = "north"
LEFT = "west"
BOTTOM = "south"
RIGHT = "east"

@dataclass
class GridLayout:
    row_space = 0.8
    """ Vertical padding between rows of images in the grid, in mm """

    column_space = 0.8
    """ Horizontal padding between columns of images in the grid, in mm """

    padding: dict[str, float] = field(default_factory=lambda: {
        "north": 0.0,
        "west": 0.0,
        "east": 0.0,
        "south": 0.0
    })
    """ Padding applied to the left, right, top, and bottom of the whole grid, in mm """

    def set_padding(self, left: float | None = None, right: float | None = None, top: float | None = None, bottom: float | None = None, column: float | None = None, row: float | None = None):
        """ Convenience setter to specify multiple paddings at once
        """
        if top != None: self.padding[TOP] = top
        if left != None: self.padding[LEFT] = left
        if right != None: self.padding[RIGHT] = right
        if bottom != None: self.padding[BOTTOM] = bottom
        if column != None: self.column_space = column
        if row != None: self.row_space = row

    captions: dict[str, TextFieldLayout] = field(default_factory=lambda: {
        "north": TextFieldLayout(fontsize=6),
        "south": TextFieldLayout(fontsize=6),
        "east": TextFieldLayout(fontsize=6, rotation=-90),
        "west": TextFieldLayout(fontsize=6, rotation=90)
    })
    """ Layouting properties of the captions to the left, top, right, and bottom of each image """

    titles: dict[str, TextFieldLayout] = field(default_factory=lambda: {
        "north": TextFieldLayout(fontsize=8),
        "south": TextFieldLayout(fontsize=8),
        "east": TextFieldLayout(fontsize=8, rotation=-90),
        "west": TextFieldLayout(fontsize=8, rotation=90)
    })
    """ Layouting properties of the grid titles """

    row_titles: dict[str, TextFieldLayout] = field(default_factory=lambda: {
        "east": TextFieldLayout(fontsize=7, rotation=-90),
        "west": TextFieldLayout(fontsize=7, rotation=90)
    })
    """ Layouting properties of the row titles """

    column_titles: dict[str, TextFieldLayout] = field(default_factory=lambda: {
        "north": TextFieldLayout(fontsize=7),
        "south": TextFieldLayout(fontsize=7)
    })
    """ Layouting properties of the column titles """