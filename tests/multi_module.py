import copy
import single_module
import generator
import generator.util

elem2 = [ # rows
    [ # first row
        {
            "image": single_module.images[1],
            "crop_marker": {
                "line_width": 1.0, "dashed": False, 
                "list": [
                    { "pos": [32,12], "size": [15,10], "color": [242, 113, 250] }
                ]
            }
        },
        {
            "image": single_module.images[0],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 1.0, "color": [50,230,10] },
        },
    ], # end first row
    [ # second row
        {
            "image": single_module.images[0],
            "crop_marker": {
                "line_width": 1.0, "dashed": True, 
                "list": [
                    { "pos": [32,12], "size": [15,10], "color": [242, 113, 250] }
                ]
            }
        },
        {
            "image": single_module.images[1],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 1.0, "color": [50,230,10] },
        },
    ], # end second row
]

column_titles = {
    "south": { 
        "text_color": [0,0,0],
        "background_colors": [[10, 10, 200], [255, 200, 10]],
        "content": [ "Blue", "Yellow" ]
    }
}

row_titles = {
    "east": { 
        "text_color": [0,0,0],
        "background_colors": [255, 255, 255],
        "content": [ "Awesome pictures 1", "Awesome pictures 2" ]
    }
}

titles = {
    "north": "North Title",
    "south": "South Title",
    "east": "East Title",
    "west": "West Title"
}

m2 = { 
    "type": "grid",
    "elements": elem2, 
    "row_titles": row_titles, 
    "column_titles": column_titles, 
    "titles": titles, 
    "layout": "layout.json" 
}

m3 = {
    "type": "grid",
    "elements":[[{ "image": single_module.images[0]}]],
    "row_titles": row_titles, 
    "column_titles": column_titles, 
    "titles": titles, 
    "layout": "layout.json" 
}

modules = [
    copy.deepcopy(single_module.modules[0]),
    m2,
    m3
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., backend='pptx', out_dir=".")
    generator.horizontal_figure(modules, width_cm=18., backend='tikz', out_dir=".")
    generator.horizontal_figure(modules, width_cm=18., backend='html', out_dir=".")