import copy
import single_module
import generator
import generator.util

grid = [ # rows
    [ # first row
        {
            "image": single_module.images[0],
        }
    ], # end first row
    #[ # second row
    #    {
    #        "image": single_module.images[0],
    #    }
    #], # end second row
]


grid_2x2 = [ # rows
    [ # first row
        {
            "image": single_module.images[1],
        },
        {
            "image": single_module.images[1],
        },
    ], # end first row
    [ # second row
        {
            "image": single_module.images[1],
        },
        {
            "image": single_module.images[1],
        },
    ], # end second row
]

m_right = { 
    "type": "grid",
    "elements": grid_2x2, 
    "row_titles": {}, 
    "column_titles": {}, 
    "titles": {}, 
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

m_left = {
    "type": "grid",
    "elements": grid, 
    "row_titles": {}, 
    "column_titles": {}, 
    "titles": {}, 
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

modules = [
    m_left,
    m_right
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=28., backend='tikz', out_dir=".")
    generator.horizontal_figure(modules, width_cm=28., backend='pptx', out_dir=".")
    generator.horizontal_figure(modules, width_cm=28., backend='html', out_dir=".")