import copy
import single_module
from app import generator

elem2 = [ # rows
    [ # first row
        {
            "image": single_module.images[0],
            "crop_marker": {
                "line_width": 1.0, "dashed": False, 
                "list": [
                    { "pos": [32,32], "size": [15,10], "color": [242, 113, 250] }
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
    ], # end first row
    [ # second row
        {
            "image": single_module.images[0],
            "crop_marker": {
                "line_width": 1.0, "dashed": True, 
                "list": [
                    { "pos": [32,32], "size": [15,10], "color": [242, 113, 250] }
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

column_titles = {}

row_titles = {}

titles = {}

m2 = { 
        "elements": elem2, 
        "row_titles": row_titles, 
        "column_titles": column_titles, 
        "titles": titles, 
        "layout": "layout.json" 
}

m3 = {
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
    generator.horizontal_figure(modules, width_cm=18., backend='tikz')