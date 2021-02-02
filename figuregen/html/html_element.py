import base64
from . import calculate

class Error(Exception):
    def __init__(self, message):
        self.message = message

def gen_module_unit_mm(width, height, offset_top=0, offset_left=0):
    m = '<div class="module" style="top: '+str(offset_top)+'mm; left: '+str(offset_left)+'mm; width: '+str(width)+'mm; height: '+str(height)+'mm;">'
    return m + '\n'

def _gen_rectangle(pos_top, pos_left, width, height, line_width_pt, color):
    lw_mm = calculate.pt_to_mm(line_width_pt)
    result = '<div class="element" style="top: '+str(pos_top)+'mm; left: '+str(pos_left)+'mm; '
    result +='width: '+str(width - lw_mm*2.)+'mm; height: '+str(height - lw_mm*2.)+'mm; '
    result += 'border: '+str(line_width_pt)+'pt solid '+css_color(color)+'"></div>' + '\n'
    return result

def _gen_border(element, width, height, pos_top, pos_left):
    try:
        frame = element['frame']
    except:
        return ''

    return _gen_rectangle(pos_top, pos_left, width, height, frame['line_width'], frame['color'])

def _embed_png(filename, width, height, pos_top, pos_left):
    img_block = f'<img class="element" style="top: {pos_top}mm; left: {pos_left}mm;'\
                f'height: {height}mm; width: {width}mm;"'
    b64data = base64.b64encode(open(filename, "rb").read()).decode()
    if filename[-4:] == ".png":
        src = ' src="' + "data:image/png;base64," + b64data + '"'
    elif filename[-4:] == ".jpg":
        src = ' src="' + "data:image/jpeg;base64," + b64data + '"'
    else:
        raise Error('HTML could not embed the following image format: ' + filename) 
    return img_block + src + '/>' +'\n'

def _embed_pdf(filename, width, height, pos_top, pos_left):
    div_open = f'<div class="element" style="top: {pos_top}mm; left: {pos_left}mm; height: {height}mm; width: {width}mm;">' + '\n'
    embed = f'<embed src="{filename}#view=FitH&scrollbar=0&toolbar=0&statusbar=0&messages=0&navpanes=0" width="100%" height="100%">' + '\n'
    div_end = '</div>' + '\n'
    return div_open + embed + div_end

def _embed_html(filename, width, height, pos_top, pos_left):
    div_open = f'<div class="element" style="top: {pos_top}mm; left: {pos_left}mm; height: {height}mm; width: {width}mm;">' + '\n'
    iframe = f'<iframe src="{filename}" width="100%" height="100%" marginwidth="0" marginheight="0" frameborder="0" hspace="0" vspace="0"></iframe>'
    div_end = '</div>' + '\n'
    return div_open + iframe + div_end

def _gen_image(element, width, height, pos_top, pos_left):
    filename = element['image']
    extension = filename[-4:]
    if extension == '.pdf':
        return _embed_pdf(filename, width, height, pos_top, pos_left)
    elif extension == 'html':
        return _embed_html(filename, width, height, pos_top, pos_left)
    else:
        return _embed_png(filename, width, height, pos_top, pos_left)

def _gen_label(img_pos_top, img_pos_left, img_width, img_height, cfg, label_pos):
    try:
        cfg = cfg[label_pos]
    except KeyError:
        return ''

    alignment = label_pos.split('_')[-1]
    is_top = (label_pos.split('_')[0] == 'top')

    rect_width, rect_height = cfg['width_mm'], cfg['height_mm']

    # determine the correct offsets depending on wether it is in the corner or center
    if alignment == 'center':
        offset_w, offset_h = 0, cfg['offset_mm']
    else:
        offset_w = cfg['offset_mm'][0]
        offset_h = cfg['offset_mm'][1]

    # determine pos_top of rectangle
    if is_top:
        pos_top = img_pos_top + offset_h
    else:
        pos_top = img_pos_top + img_height - rect_height - offset_h

    # determine pos_left of rectangle based on alignment
    if alignment == 'center':
        pos_left = img_pos_left + (img_width * 1/2.) - (rect_width * 1/2.)
    elif alignment == 'left':
        pos_left = img_pos_left + offset_w
    else: # right
        pos_left = img_pos_left + img_width - rect_width - offset_w

    result = _title_container((pos_top, pos_left), (rect_width, rect_height), rotation=0, bg_color=cfg['background_color'], alignment=alignment)
    result += _title_content(cfg['text'], cfg['fontsize'], cfg['text_color'], cfg['padding_mm'], alignment)
    return result

def _gen_labels(element, img_width, img_height, img_pos_top, img_pos_left):
    try:
        cfg = element['label']
    except:
        return ''

    result = ''
    for label_pos in ['top_center', 'top_left', 'top_right', 'bottom_center', 'bottom_left', 'bottom_right']:
        result += _gen_label(img_pos_top, img_pos_left, img_width, img_height, cfg, label_pos)
    return result

def _gen_markers(element, img_pos_top, img_pos_left, img_width_px, img_height_px, img_used_width, img_used_height):
    try:
        markers = element['marker']
    except:
        return ''

    result = ''
    w_scale, h_scale = calculate.relative_position(img_width_px, img_height_px, img_used_width, img_used_height)

    for m in markers:
        if m['lw'] > 0.0:
            pos_top = img_pos_top + (m['pos'][1] * h_scale)
            pos_left = img_pos_left + (m['pos'][0] * w_scale)
            result += _gen_rectangle(pos_top, pos_left,
                                    width = m['size'][0] * w_scale, height = m['size'][1] * h_scale,
                                    line_width_pt = m['lw'], color = m['color'])
    return result

def _add_lines(element, img_pos_top, img_pos_left, img_width_px, img_height_px, img_used_width, img_used_height):
    try:
        lines = element['lines']
    except:
        return ''

    w_scale, h_scale = calculate.relative_position(img_width_px, img_height_px, img_used_width, img_used_height)

    if lines != []:
        div = f'<div class="svg-container" style="position: absolute; top: {img_pos_top}mm; left: {img_pos_left}mm; '\
            f'height: {img_used_height}mm; width: {img_used_width}mm;">'
        svg = f'<svg style="height: {img_used_height}mm; width: {img_used_width}mm;">'
        svg_lines = ''
        for l in lines:
            start_h = l['from'][0] * h_scale
            start_w = l['from'][1] * w_scale
            end_h = l['to'][0] * h_scale
            end_w = l['to'][1] * w_scale
            rgb = (l['color'][0], l['color'][1], l['color'][2])
            svg_lines += f'<line x1="{start_w}mm" y1="{start_h}mm" x2="{end_w}mm" y2="{end_h}mm" style="stroke:rgb{rgb};stroke-width:{l["lw"]}pt" />\n'
        return div + svg + svg_lines + '</svg>' + '</div>'+'\n'
    return ''

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
            images += _add_lines(element, pos_top, pos_left, data['img_width_px'], data['img_height_px'], width, height)
            images += _gen_border(element, width, height, pos_top, pos_left)
            images += _gen_labels(element, width, height, pos_top, pos_left)
            images += _gen_markers(element, pos_top, pos_left, data['img_width_px'], data['img_height_px'], width, height)
            col_idx += 1
        row_idx += 1

    return images

def _title_container(position, size, rotation=0, bg_color=None, alignment='center'):
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
        container +=' width: '+str(width)+'mm; height: '+str(height)+'mm; transform: rotate('+str(-rotation)+'deg);'
        container += color + '">' + '\n'
    else:
        # only in this case we consider alignment and padding
        align = ''
        if alignment is not None and alignment != 'center':
            if alignment == 'left':
                align = 'justify-content: flex-start; '
            else:
                align = 'justify-content: flex-end; '

        container = '<div class="title-container" style="top: '+str(position[0])+'mm; left: '+str(position[1])+'mm;'
        container +=' width: '+str(size[0])+'mm; height: '+str(size[1])+'mm;' + align
        container += color + '">' + '\n'
    return container

def _title_content(txt_content, fontsize_pt, txt_color=None, padding=None, alignment='center'):
    if txt_content == '':
        return '</div>' + '\n'

    color = ''
    if txt_color is None:
        txt_color = [0,0,0]
    color += 'color: '+ css_color(txt_color)+'; '

    txt_pad = ''
    if padding is not None and padding != 0.0:
        txt_pad = '<p style="width: '+str(padding)+'mm"></p>' + '\n'

    txt_align = 'text-align: ' + alignment +'; '

    font_size = 'font-size: ' + str(fontsize_pt) + 'pt;'

    result = ''
    if alignment=='left':
        result += txt_pad
    result += '<p class="title-content" style="'+ txt_align + color + font_size +'">' + txt_content.replace('\\\\', '<br/>') +'</p>' + '\n'
    if alignment=='right':
        result += txt_pad
    result += '</div>' + '\n'

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

def _row_col_titles(direction, title_properties, num, pos_fn):
    result = ''
    if calculate.size_of(title_properties, direction)[0] != 0.0:
        bg_colors = _compute_bg_colors(title_properties[direction]['background_colors'], num)
        t = title_properties[direction]

        for i in range(num):
            pos, size = pos_fn(i)
            if size[0] != 0.0 and size[1] != 0.0:
                if t['content'][i] != '':
                    result += _title_container(pos, size, t['rotation'], bg_colors[i])
                    result += _title_content(t['content'][i], t['fontsize'], t['text_color'])
                result += '\n'
    return result

def gen_row_titles(data):
    result = ''
    for direction in ['east', 'west']:
        def pos_fn (idx):
            return calculate.row_titles_pos(data, idx + 1, direction)
        result += _row_col_titles(direction, data['row_titles'], data['num_rows'], pos_fn) + '\n'
    return result

def gen_column_titles(data):
    result = ''
    for direction in ['north', 'south']:
        def pos_fn (idx):
            return calculate.column_titles_pos(data, idx + 1, direction)
        result += _row_col_titles(direction, data['column_titles'], data['num_columns'], pos_fn) + '\n'
    return result

def gen_south_captions(data):
    '''
    South caption: each image can have it's own caption below the image.
    '''
    result = ''
    capt_prop = data['element_config']['captions']['south']
    size = data['element_config']['img_width'], capt_prop['height']
    if size[0] == 0.0:
        return result

    rowIndex = 1
    for row in data['elements_content']:
        colIndex = 1
        for elem in row:
            pos = calculate.south_caption_pos(data, colIndex, rowIndex)
            txt_content = elem['captions']['south']
            if txt_content != '':
                result += _title_container(pos, size, capt_prop['rotation'], None)
                result += _title_content(txt_content, capt_prop['fontsize'], capt_prop['text_color'])
            result += '\n'

            colIndex += 1
        rowIndex += 1
    return result