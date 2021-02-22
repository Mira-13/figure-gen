import figuregen
import numpy as np

img_blue = np.tile([x / 255 for x in [94, 163, 188]], (32, 64, 1))
img_yellow = np.tile([x / 255 for x in [232, 181, 88]], (32, 64, 1))

grid = figuregen.Grid(1, 2)
grid[0, 0].set_image(figuregen.JPEG(img_blue))
grid[0, 1].set_image(figuregen.JPEG(img_yellow))

figuregen.horizontal_figure([grid], 8, "jpeg_export.pdf")
figuregen.horizontal_figure([grid], 8, "jpeg_export.pptx")
figuregen.horizontal_figure([grid], 8, "jpeg_export.html")

grid = figuregen.Grid(1, 2)
grid[0, 0].set_image(figuregen.PNG(img_blue))
grid[0, 1].set_image(figuregen.PNG(img_yellow))

figuregen.horizontal_figure([grid], 8, "png_export.pdf")
figuregen.horizontal_figure([grid], 8, "png_export.pptx")
figuregen.horizontal_figure([grid], 8, "png_export.html")