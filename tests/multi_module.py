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
    "layout": {
      "padding.right": 0.1,
      "padding.top": 0.5,
      "titles.north.height": 8,
      "titles.north.background_color": [ 29, 60, 100 ],
      "titles.north.text_color": [ 255, 255, 250 ],
      "column_titles.north.width": 4,
      "column_titles.north.offset": 2,

      "column_space": 1,
      "row_space": 2
    }
}

m3 = {
    "type": "grid",
    "elements":[[{ "image": single_module.images[0]}]],
    "row_titles": row_titles, 
    "column_titles": column_titles, 
    "titles": titles, 
    "layout": {
      "padding.east": 0.1,
      "padding.north": 0.5,
      "titles.north.height": 8,
      "titles.north.background_color": [ 29, 60, 100 ],
      "titles.north.text_color": [ 255, 255, 250 ],
      "column_titles.north.width": 4,
      "column_titles.north.offset": 2,

      "column_space": 1,
      "row_space": 2
    }
}

modules = [
    copy.deepcopy(single_module.modules[0]),
    m2,
    m3
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pdf')
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pptx')
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.html')