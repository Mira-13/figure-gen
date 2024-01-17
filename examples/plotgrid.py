import figuregen
import numpy as np
import json

def make_row(method_name, title, mark_strata=False, problem_range=None, show_titles=False):
    with open(f"data/{method_name}.json") as f:
        data = json.load(f)

    grid = figuregen.Grid(num_cols=6, num_rows=1)

    xticks = [0, 1]
    colors = [
        [68, 104, 167],
        [244, 146, 42],
        [211, 95, 85],
        [89, 151, 223],
        [138, 74, 201],
    ]

    # Add the problem overview
    plot = figuregen.PgfLinePlot(aspect_ratio=0.9, data=[
        (data["PdfA"]["X"], data["PdfA"]["Y"]),
        (data["PdfB"]["X"], data["PdfB"]["Y"]),
        (data["Integrand"]["X"], data["Integrand"]["Y"])
    ])
    plot.set_font(fontsize_pt=7)
    plot.set_linewidth(plot_line_pt=1)
    plot.set_axis_properties("x", xticks, range=[0, 1.1], use_log_scale=False)
    plot.set_axis_properties("y", [], range=problem_range, use_log_scale=False)
    plot.set_padding(left_mm=1, bottom_mm=3)
    plot.set_colors(colors)

    if mark_strata:
        marker_width = 0.5
        marker_color = [100, 100, 100]
        marker_style = [1]
        plot.set_v_line(0.25, marker_color, marker_style, marker_width)
        plot.set_v_line(0.50, marker_color, marker_style, marker_width)
        plot.set_v_line(0.75, marker_color, marker_style, marker_width)
        plot.set_v_line(1.00, marker_color, marker_style, marker_width)

    grid.get_element(0, 0).set_image(plot)

    # Add the different methods
    variance_captions = [""]
    def plot_method(name, idx, crop=True):
        plot = figuregen.PgfLinePlot(aspect_ratio=0.9, data=[
            (data[name]["WeightA"]["X"], data[name]["WeightA"]["Y"]),
            (data[name]["WeightB"]["X"], data[name]["WeightB"]["Y"])
        ])
        plot.set_font(fontsize_pt=7)
        plot.set_linewidth(plot_line_pt=1)
        plot.set_padding(left_mm=6 if not crop else 3, bottom_mm=3)
        plot.set_colors(colors)

        if mark_strata:
            plot.set_v_line(0.25, marker_color, marker_style, marker_width)
            plot.set_v_line(0.50, marker_color, marker_style, marker_width)
            plot.set_v_line(0.75, marker_color, marker_style, marker_width)
            plot.set_v_line(1.00, marker_color, marker_style, marker_width)

        if not crop:
            max_val_a = np.max(data[name]["WeightA"]["Y"])
            min_val_a = np.min(data[name]["WeightA"]["Y"])
            max_val_b = np.max(data[name]["WeightB"]["Y"])
            min_val_b = np.min(data[name]["WeightB"]["Y"])
            max_val = max(max_val_a, max_val_b)
            min_val = min(min_val_a, min_val_b)
            lo_tick = int(min_val / 10) * 10
            hi_tick = int(max_val / 10) * 10
            if hi_tick == 0:
                hi_tick = 1
            if lo_tick == 0:
                lo_tick = -1
        else:
            min_val = 0
            max_val = 1
            lo_tick = 0
            hi_tick = 1
        range = [min_val * 1.15, max_val * 1.15]
        plot.set_axis_properties("x", xticks, range=[0, 1.15], use_log_scale=False)
        plot.set_axis_properties("y", [lo_tick, hi_tick], range=range, use_log_scale=False)

        grid.get_element(0, idx).set_image(plot)
        variance_captions.append(f"Variance: {data[name]['Variance']:.4f}")

    plot_method("Average", 1)
    plot_method("RecipVar", 2)
    plot_method("Balance", 3)
    plot_method("VarAware", 4)
    plot_method("Optimal", 5, False)

    # Add titles
    grid.set_row_titles("left", [title])
    grid.layout.row_titles[figuregen.LEFT] = figuregen.TextFieldLayout(size=3, offset=0.5, fontsize=8, rotation=90)
    if show_titles:
        grid.set_col_titles("bottom", [
            "a) Integrand and densities",
            "b) Average",
            "c) Opt. const.",
            "d) Balance heuristic",
            "e) Var-aware",
            "f) Optimal weights"
        ])
        grid.layout.column_titles[figuregen.BOTTOM] = figuregen.TextFieldLayout(size=6, offset=0.5, fontsize=8)

    grid.set_col_titles("top", variance_captions)
    grid.layout.column_titles[figuregen.TOP] = figuregen.TextFieldLayout(size=3, offset=0.5, fontsize=8)

    # Add space between the rows (needs to be removed for the last one)
    grid.layout.set_padding(bottom=2)

    return [grid]

rows = [
    make_row("BalanceOptimal", "1) Product", problem_range=[0,2.5]),
    make_row("Defensive", "2) Defensive", problem_range=[0,2.5]),
    make_row("Stratified", "3) Stratified", True, problem_range=[0,4.5], show_titles=True),
]

# Remove bottom padding from the last row
rows[-1][0].layout.padding[figuregen.BOTTOM] = 0

if __name__ == "__main__":
    import time
    start = time.time()
    figuregen.figure(rows, 15.4, "plotgrid.pdf")
    figuregen.figure(rows, 15.4, "plotgrid.pptx")
    figuregen.figure(rows, 15.4, "plotgrid.html")
    print(time.time() - start)

    try:
        from figuregen.util import jupyter
        jupyter.convert('plotgrid.pdf', 300)
    except:
        print('Warning: pdf could not be converted to png')