import pyexr

def load_exr(path):
    return pyexr.read(path)

def crop(img, left, top, width, height):
    return img[top:top+height,left:left+width,:]

# load images, user needs to provide direct/total path
path = 'C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/'

pool_ref = load_exr(path + 'pool/referenz.exr')
pool_patht = load_exr(path + 'pool/path-tracing.exr')
pool_muller = load_exr(path + 'pool/muller.exr')
pool_osimpl = load_exr(path + 'pool/ours-simplified.exr')
pool_ofull = load_exr(path + 'pool/ours-full.exr')

gloskitch120_ref = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen.exr')
gloskitch120_patht = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen-120s-pt.exr')
gloskitch120_bdpt = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen-120s-bdpt.exr')
gloskitch120_radia = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen-120s-radiance.exr')
gloskitch120_upscmc = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen-120s-upsmcmc.exr') 
gloskitch120_ofull = load_exr(path + 'glossy-kitchen-120s/glossy-kitchen-120s-full.exr')

livroom120_ref = load_exr(path + 'living-room-120s/living-room.exr')
livroom120_patht = load_exr(path + 'living-room-120s/living-room-120s-pt.exr')
livroom120_bdpt = load_exr(path + 'living-room-120s/living-room-120s-bdpt.exr')
livroom120_radia = load_exr(path + 'living-room-120s/living-room-120s-radiance.exr')
livroom120_upscmc = load_exr(path + 'living-room-120s/living-room-120s-upsmcmc.exr') 
livroom120_ofull = load_exr(path + 'living-room-120s/living-room-120s-full.exr')

bookshelf120_ref = load_exr(path + 'bookshelf-120s/bookshelf.exr')
bookshelf120_patht = load_exr(path + 'bookshelf-120s/bookshelf-120s-path.exr')
bookshelf120_radia = load_exr(path + 'bookshelf-120s/bookshelf-120s-radiance.exr')
bookshelf120_upscmc = load_exr(path + 'bookshelf-120s/bookshelf-120s-upsmcmc.exr') 
bookshelf120_ofull = load_exr(path + 'bookshelf-120s/bookshelf-120s-full.exr')

gloskitch90_ref = load_exr(path + 'glossy-kitchen-90s/glossy-kitchen.exr')
gloskitch90_patht = load_exr(path + 'glossy-kitchen-90s/glossy-kitchen-90s-path.exr')
gloskitch90_radia = load_exr(path + 'glossy-kitchen-90s/glossy-kitchen-90s-radiance.exr')
gloskitch90_upscmc = load_exr(path + 'glossy-kitchen-90s/glossy-kitchen-90s-upsmcmc.exr') 
gloskitch90_ofull = load_exr(path + 'glossy-kitchen-90s/glossy-kitchen-90s-full.exr')

pool60_ref = load_exr(path + 'pool-60s/pool.exr')
pool60_patht = load_exr(path + 'pool-60s/pool-60s-path.exr')
pool60_radia = load_exr(path + 'pool-60s/pool-60s-radiance.exr')
pool60_upscmc = load_exr(path + 'pool-60s/pool-60s-upsmcmc.exr') 
pool60_ofull = load_exr(path + 'pool-60s/pool-60s-full.exr')

vdoor60_ref = load_exr(path + 'veach-door-60s/veach-door.exr')
vdoor60_patht = load_exr(path + 'veach-door-60s/veach-door-60s-path.exr')
vdoor60_radia = load_exr(path + 'veach-door-60s/veach-door-60s-radiance.exr')
vdoor60_upscmc = load_exr(path + 'veach-door-60s/veach-door-60s-upsmcmc.exr') 
vdoor60_ofull = load_exr(path + 'veach-door-60s/veach-door-60s-full.exr')

def veachDoorCrop1(img, left=246, top=268, width=20, height=20):
    return crop(img, left, top, width, height)

def veachDoorCrop2(img, left=355, top=230, width=20, height=20):
    return crop(img, left, top, width, height)

def bookshelf_crop(num, img=[]):
    width, height = 20, 20
    if num == 1:
        left, top = 369, 191
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)
    else:
        left, top = 238, 108
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)

# def bookshelfCrop1(img, left=369, top=191, width=20, height=20):
#     return crop(img, left, top, width, height)

# def bookshelfCrop2(img, left=238, top=108, width=20, height=20):
#     return crop(img, left, top, width, height)

def livingRoomInset1(img, left=180, top=120, width=20, height=20):
    return crop(img, left, top, width, height)

def livingRoomInset2(img, left=500, top=320, width=20, height=20):
    return crop(img, left, top, width, height)


def glossyKitchenRef(left=0, top=0, width=640, height=360):
    return crop(gloskitch120_ref, left, top, width, height)

def glossyKitchenInset1(img, left=100, top=120, width=20, height=20):
    return crop(img, left, top, width, height)

def glossyKitchenInset2(img, left=212, top=330, width=20, height=20):
    return crop(img, left, top, width, height)

def make_copies(scene_name):
    # TODO make copies and let the user decide a folder name
    print('TODO make copies')

# in case user needs more structure, this serves as an example
import enum
class Scene(enum.Enum):
    pool = 1
    bathroom = 2

class Method(enum.Enum):
    reference = 0
    pathtracing = 1
    muller = 2
    oursimple = 3
    ourfull = 4

def getScene(scene):
    if scene == Scene.pool:
        return [
            pool_ref, 
            pool_patht, 
            pool_muller, 
            pool_osimpl, 
            pool_ofull
        ]
    else:
        return []


def poolInset1(img, left=400, top=120, width=20, height=20):
    return crop(img, left, top, width, height)

def poolInset2(img, left=607, top=81, width=20, height=20):
    return crop(img, left, top, width, height)

def poolInset3(img, left=210, top=115, width=20, height=20):
    return crop(img, left, top, width, height)