import unittest
import numpy as np

import figuregen
import figuregen.calculate as calc
from figuregen.tikz import TikzBackend

colors = [
    [232, 181, 88], #yellow
    [5, 142, 78], #green
    [94, 163, 188], #light-blue
    [181, 63, 106], #pink
    [82, 110, 186], #blue
    [186, 98, 82] #orange-crab
]

class TestAlignment(unittest.TestCase):
    def test_single_image_correct_size(self):
        grid = figuregen.Grid(1, 1)

        img_blue = np.tile([x / 255 for x in colors[2]], (32, 64, 1))
        grid[0, 0].image = figuregen.PNG(img_blue)

        backend = TikzBackend()
        sz = backend.compute_aligned_sizes([grid], 13)

        self.assertAlmostEqual(sz[0][0].width_mm, 13)
        self.assertAlmostEqual(sz[0][0].height_mm, 13 / 2)

        self.assertAlmostEqual(sz[0][1].width_mm, 13)
        self.assertAlmostEqual(sz[0][1].height_mm, 13 / 2)

    def test_image_with_title_correct_pos(self):
        grid = figuregen.Grid(1, 1)

        img_blue = np.tile([x / 255 for x in colors[2]], (32, 64, 1))
        grid[0, 0].image = figuregen.PNG(img_blue)

        grid.set_col_titles("top", ["hi there"])
        grid.layout.set_col_titles("top", 5, 0.5)

        backend = TikzBackend()
        sz = backend.compute_aligned_sizes([grid], 13)

        # grid size should include title
        self.assertAlmostEqual(sz[0][0].width_mm, 13)
        self.assertAlmostEqual(sz[0][0].height_mm, 13 / 2 + 5.5)

        # image size should be same as without title
        self.assertAlmostEqual(sz[0][1].width_mm, 13)
        self.assertAlmostEqual(sz[0][1].height_mm, 13 / 2)

        imgpos = calc.image_pos(grid, sz[0][1], 0, 0)
        self.assertAlmostEqual(imgpos[0], 5.5)
        self.assertAlmostEqual(imgpos[1], 0)

if __name__ == "__main__":
    unittest.main()