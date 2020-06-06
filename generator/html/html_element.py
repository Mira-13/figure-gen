import json
from . import calculate

def gen_module_unit_mm(width, height, offset_top=0, offset_left=0):
    m = '<div class="module" style="top: '+str(offset_top)+'mm; left: '+str(offset_left)+'mm; width: '+str(width)+'mm; height: '+str(height)+'mm;">'
    return m + '\n'

def _gen_border(element):
    # TODO
    try:
        frame = element['frame']
    except:
        return ''
    border_content = 'border="'+str(frame['thickness_pt'])+'pt '+frame['color']+'"'
    return border_content

def _gen_image(element, width, height, pos_top, pos_left):
    img_block = '<img class="element" style="top: '+str(pos_top)+'mm; left: '+str(pos_left)+'mm; height: '+str(height)+'mm; width: '+str(width)+'mm;"' 
    src = ' src="'+element['filename']+'"'
    border = ' ' #'+_gen_border(element)
    return img_block + src + border + '/>' +'\n'

def gen_images(data):
    images = ''
    width = data['element_config']['img_width']
    height = data['element_config']['img_height']

    row_idx = 1
    for row in data['elements_content']:
        col_idx = 1
        for element in row:
            pos_top, pos_left = calculate.img_pos(data, col_idx, row_idx)
            images += _gen_image(element, width, height, pos_top, pos_left)
            col_idx += 1
        row_idx += 1

    return images

def _title_container(position, size, rotation=0, bg_color=None):
    color = ''
    if bg_color is not None:
        color += 'background-color: ' + css_color(bg_color)

    if rotation == 90 or rotation == -90:
        width, height = size[0], size[1]

        # Since we only allow 90° rotations, we can correct for that with a simple translation
        pos_top = position[0] + height / 2. - width / 2.
        pos_left = position[1] - height / 2. + width / 2.
        
        # swap height and width
        height, width = width, height

        container = '<div class="title-container" style="top: '+str(pos_top)+'mm; left: '+str(pos_left)+'mm;'
        container +=' width: '+str(width)+'mm; height: '+str(height)+'mm; transform: rotate('+str(rotation)+'deg);'
        container += color + '">' + '\n'
    else:
        container = '<div class="title-container" style="top: '+str(position[0])+'mm; left: '+str(position[1])+'mm;'
        container +=' width: '+str(size[0])+'mm; height: '+str(size[1])+'mm;'
        container += color + '">' + '\n'
    return container

def _title_content(txt_content, fontsize_pt, txt_color=None):
    if txt_content == '':
        return ''

    color = ''
    if txt_color is not None and txt_color != [0,0,0]:
        color += 'color: '+ css_color(txt_color)+'; '

    font_size = 'font-size: ' + str(fontsize_pt) + 'pt;' # is pt possible?
    result = '<p class="title-content" style="'+ color + font_size +'">'
    result += txt_content +'</p>' + '\n' + '</div>' + '\n'
    return result

def gen_titles(data):
    result = '\n'
    for direction in ['north', 'east', 'south', 'west']:
        position, size = calculate.titles_pos_and_size(data, direction)
        t = data['titles'][direction]
        if (size[0] != 0.0 and size[1] != 0.0) and t['content'] != '':
            result += _title_container(position, size, t['rotation'], t['background_color'])
            result += _title_content(t['content'], t['fontsize'], t['text_color'])
    return result

def css_color(rgb_list):
    r, g, b = rgb_list[0], rgb_list[1], rgb_list[2]
    return 'rgb('+str(r)+','+str(g)+','+str(b)+');' #background-color: rgb(r,g,b)

def _compute_bg_colors(bg_color_properties, num):
    if bg_color_properties is None: # no background color
        return [None for i in range(num)]
    elif not isinstance(bg_color_properties[0], list): # constant color for all
        return [bg_color_properties for i in range(num)]
    else: # individual background colors
        return bg_color_properties

def _row_col_titles(data, direction, title_properties, num, pos_fn):
    result = ''
    if calculate.size_of(title_properties, direction)[0] != 0.0:
        bg_colors = _compute_bg_colors(title_properties[direction]['background_colors'], num)
        t = title_properties[direction]

        for i in range(num):
            pos, size = pos_fn(i)
            if size[0] != 0.0 and size[1] != 0.0:
                #result += add_text(t['fontsize'], t['text_color'] + '\n'
                result += _title_container(pos, size, t['rotation'], bg_colors[i])

                if t['content'][i] != '':
                    result += _title_content(t['content'][i], t['fontsize'], t['text_color'])
                result += '</div>' + '\n'
    return result

def gen_row_titles(data):
    result = ''
    for direction in ['east', 'west']:
        def pos_fn (idx): 
            return calculate.row_titles_pos(data, idx + 1, direction)
        result += _row_col_titles(data, direction, data['row_titles'], data['num_rows'], pos_fn) + '\n'
    return result

def gen_column_titles(data):
    result = ''
    for direction in ['north', 'south']:
        def pos_fn (idx): 
            return calculate.column_titles_pos(data, idx + 1, direction)
        result += _row_col_titles(data, direction, data['column_titles'], data['num_columns'], pos_fn) + '\n'
    return result