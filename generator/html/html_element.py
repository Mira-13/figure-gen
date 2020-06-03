import json

def _gen_border(element):
    try:
        frame = element['frame']
    except:
        return ''
    border_content = 'border="'+frame['color']+'"'
    return border_content

def _gen_image(element):
    img_block = '<img src="'+element['filename']+'"'+_gen_border(element)+'>'
    return img_block

def gen_images(module_elements):
    image_grid = ''
    for row in module_elements:
        image_grid += '<div class="row">'
        for element in row:
            image_grid += '<div class="column">'
            image_grid += _gen_image(element)
            image_grid += '</div>'
        image_grid += '</div>'

    return image_grid

def gen_titles(module_titles):
    return '' # TODO

