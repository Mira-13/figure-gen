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

def vdoor_crop(num, img=[]):
    width, height = 20, 20
    if num == 1:
        left, top = 246, 268
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)
    else:
        left, top = 355, 230
        if img == []:
            return left, top, width, height
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

def pool_crop(num, img=[]):
    width, height = 20, 20
    if num == 1:
        left, top = 400, 120
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)
    else:
        left, top = 607, 81
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)

def livingroom_crop(num, img=[]):
    width, height = 20, 20
    if num == 1:
        left, top = 180, 120
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)
    else:
        left, top = 500, 320
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)

def gkitchen_crop(num, img=[]):
    width, height = 20, 20
    if num == 1:
        left, top = 100, 120
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)
    else:
        left, top = 212, 330
        if img == []:
            return left, top, width, height
        return crop(img, left, top, width, height)


def make_copies(scene_name):
    # TODO make copies and let the user decide a folder name
    print('TODO make copies')

