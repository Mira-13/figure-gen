import pyexr

def load_exr(path):
    return pyexr.read(path)

def zoom(img, left, top, width, height):
    return img[top:top+height,left:left+width,:]

# load images, user needs to provide direct/total path
pool_ref = load_exr('C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/pool/referenz.exr')
pool_patht = load_exr('C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/pool/path-tracing.exr')
pool_muller = load_exr('C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/pool/muller.exr')
pool_osimpl = load_exr('C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/pool/ours-simplified.exr')
pool_ofull = load_exr('C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/pool/ours-full.exr')

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


def poolInset1(img, left=575, top=20, width=20, height=20):
    return zoom(img, left, top, width, height)

def poolInset2(img, left=465, top=130, width=20, height=20):
    return zoom(img, left, top, width, height)

def poolInset3(img, left=210, top=15, width=20, height=20):
    return zoom(img, left, top, width, height)