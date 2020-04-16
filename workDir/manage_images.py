import pyexr
import os
import json

def load_exr(path):
    return pyexr.read(path)

def crop(img, left, top, width, height):
    return img[top:top+height,left:left+width,:]

# load images, user needs to provide direct/total path
rimg_path = 'C:/Users/admin/Documents/MasterThesis/mtc/workDir/raw-imgs/'

scenes = [
    'living-room',      # fig3
    'bookshelf',        # fig4
    'glossy-kitchen',   # fig5
    'pool',             # fig6
    'veach-door'        # fig7
]
time_sec = [
    120,
    120,
    90,
    60,
    60
]
crops = [
    [[100, 100, 40, 30], [200, 180, 40, 30]],
    [[369, 191, 40, 30], [238, 108, 40, 30]],
    [[100, 120, 40, 30], [212, 325, 40, 30]],
    [[400, 120, 40, 30], [595, 81, 40, 30]],
    [[246, 268, 40, 30], [504, 65, 40, 30]]
]
methods = [
    'path',
    'radiance',
    'upsmcmc',
    'full'
]

def load_image(scene, method=None):
    global rimg_path
    global scenes
    global time_sec
    global methods

    idx = scenes.index(scene)
    folder_name = scenes[idx] + '-' + str(time_sec[idx]) + 's'
    
    if method is None:
        exr_file = scenes[idx] + '.exr' # load reference
    else:
        methods.index(method) # force that the method is listed
        exr_file = folder_name + '-' + method + '.exr'
    
    return pyexr.read(os.path.join(rimg_path, folder_name, exr_file))

def get_cropped_img(scene, method, crop_num):
    global crop # function
    global crops # values
    img = load_image(scene, method)
    sc_idx = scenes.index(scene)
    crop_args = crops[sc_idx][crop_num]
    return crop(img, crop_args[0], crop_args[1], crop_args[2], crop_args[3])
    
def get_crop_list(scene):
    idx = scenes.index(scene)
    return crops[idx]

def get_time_sec(scene):
    idx = scenes.index(scene)
    return time_sec[idx]

error_path = 'C:/Users/admin/Documents/MasterThesis/mtc/workDir/errors/'

def get_error(scene, method, metric='MRSE*'):
    scene_idx = scenes.index(scene)
    methods.index(method) # simple method check

    p = os.path.join(error_path, scene, scene+'__'+method+'.json')
    with open(p) as json_file:
        data = json.load(json_file)
    idx = data['timesteps'].index(time_sec[scene_idx])
    error = data['data'][idx][metric]
    return error

# TODO remove old code from fig 1- fig3
pool_patht = load_exr(rimg_path + 'pool/path-tracing.exr')
pool_ref = load_exr(rimg_path + 'pool/referenz.exr')
pool_muller = load_exr(rimg_path + 'pool/muller.exr')
pool_osimpl = load_exr(rimg_path + 'pool/ours-simplified.exr')
pool_ofull = load_exr(rimg_path + 'pool/ours-full.exr')

gloskitch120_ref = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen.exr')
gloskitch120_patht = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen-120s-pt.exr')
gloskitch120_bdpt = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen-120s-bdpt.exr')
gloskitch120_radia = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen-120s-radiance.exr')
gloskitch120_upscmc = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen-120s-upsmcmc.exr') 
gloskitch120_ofull = load_exr(rimg_path + 'glossy-kitchen-120s/glossy-kitchen-120s-full.exr')

livroom120_ref = load_exr(rimg_path + 'living-room-120s/living-room.exr')
livroom120_patht = load_exr(rimg_path + 'living-room-120s/living-room-120s-pt.exr')
livroom120_bdpt = load_exr(rimg_path + 'living-room-120s/living-room-120s-bdpt.exr')
livroom120_radia = load_exr(rimg_path + 'living-room-120s/living-room-120s-radiance.exr')
livroom120_upscmc = load_exr(rimg_path + 'living-room-120s/living-room-120s-upsmcmc.exr') 
livroom120_ofull = load_exr(rimg_path + 'living-room-120s/living-room-120s-full.exr')


def make_copies(scene_name):
    # TODO make copies and let the user decide a folder name
    print('TODO make copies')

