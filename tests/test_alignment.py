import unittest
import figuregen
import numpy as np

from figuregen.newimpl import TikzBackend, figure

colors = [
    [232, 181, 88], #yellow
    [5, 142, 78], #green
    [94, 163, 188], #light-blue
    [181, 63, 106], #pink
    [82, 110, 186], #blue
    [186, 98, 82] #orange-crab
]

class TestAlignment(unittest.TestCase):
    def test_single_grid_single_image(self):
        grid = figuregen.Grid(1, 1)

        img_blue = np.tile([x / 255 for x in colors[2]], (32, 64, 1))
        grid[0, 0].image = figuregen.PNG(img_blue)

        backend = TikzBackend()
        sz = backend.compute_aligned_sizes([grid], 13)

        self.assertAlmostEqual(sz[0].width_mm, 13)
        self.assertAlmostEqual(sz[0].height_mm, 13 / 2)

if __name__ == "__main__":
    unittest.main()