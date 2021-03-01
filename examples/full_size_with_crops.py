import simpleimageio as sio
import figuregen
from figuregen.util.templates import FullSizeWithCrops
from figuregen.util.image import Cropbox

figure = FullSizeWithCrops(
    reference_image=sio.read("images/pool/pool.exr"),
    method_images=[
        sio.read("images/pool/pool-60s-path.exr"),
        sio.read("images/pool/pool-60s-upsmcmc.exr"),
        sio.read("images/pool/pool-60s-radiance.exr"),
        sio.read("images/pool/pool-60s-full.exr"),
    ],
    crops=[
        Cropbox(top=100, left=200, height=96, width=128, scale=5),
        Cropbox(top=100, left=450, height=96, width=128, scale=5),
    ],
    method_names=["Reference", "Path Tracer", "UPS+MCMC", "Radiance-based", "Ours"]
).figure

figuregen.figure(figure, width_cm=17.7, filename="full_size_with_crops.pdf")

try:
    from figuregen.util import jupyter
    jupyter.convert('full_size_with_crops.pdf', 300)
except:
    print('Warning: pdf could not be converted to png')

# Create the same figure again, but this time with the crops on the right hand side of each image
figure = FullSizeWithCrops(
    reference_image=sio.read("images/pool/pool.exr"),
    method_images=[
        sio.read("images/pool/pool-60s-path.exr"),
        sio.read("images/pool/pool-60s-radiance.exr"),
        sio.read("images/pool/pool-60s-full.exr"),
    ],
    crops=[
        Cropbox(top=100, left=200, height=96, width=128, scale=5),
        Cropbox(top=100, left=450, height=96, width=128, scale=5),
    ],
    method_names=["Reference", "Path Tracer", "UPS+MCMC", "Radiance-based", "Ours"],
    crops_below=False
).figure

figuregen.figure(figure, width_cm=17.7, filename="full_size_with_crops_side.pdf")

try:
    from figuregen.util import jupyter
    jupyter.convert('full_size_with_crops_side.pdf', 300)
except:
    print('Warning: pdf could not be converted to png')

