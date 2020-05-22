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
    "elements": grid_2x2, 
    "row_titles": {}, 
    "column_titles": {}, 
    "titles": {}, 
    "layout": "layout.json",
    "type": "grid" 
}

m_left = { 
    "elements": grid, 
    "row_titles": {}, 
    "column_titles": {}, 
    "titles": {}, 
    "layout": "layout.json",
    "type": "grid"
}

modules = [
    m_left,
    m_right
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., backend='tikz')