import simpleimageio as sio
import figuregen
from figuregen.util.templates import CropComparison
from figuregen.util.image import Cropbox

figure = CropComparison(
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
    scene_name="Pool",
    method_names=["Reference", "Path Tracer", "UPS+MCMC", "Radiance-based", "Ours"]
)

figuregen.figure([figure.figure_row], width_cm=17.7, filename="pool_with_template.pdf")

try:
    from figuregen.util import jupyter
    jupyter.convert('pool_with_template.pdf', 300)
except:
    print('Warning: pdf could not be converted to png')
