from typing import Union
from .backend import *
from concurrent.futures import ThreadPoolExecutor, Future

class HtmlBackend(Backend):
    def __init__(self, inline=False, custom_head: str = "", id_prefix=""):
        """
        Creates a new HTML backend that emits a static webpage with embedded base64 images.

        Args:
            inline: boolean, if true does not generate <html>, <head>, <body> tags
            custom_head: additonal lines to add to the <head>, ignored if inline = False
            id_prefix: additional text in front of the figure's elements, useful if multiple figures are in on .html
        """
        self._inline = inline
        self._custom_head = custom_head
        self._prefix = id_prefix
        self._thread_pool = ThreadPoolExecutor()

    @property
    def style(self) -> str:
        """ The required CSS style for the figure to display correctly. """
        return "\n".join([
            '<style type="text/css">',
            '.figure { position: relative; }',
            '.title-container { position: absolute; margin: 0; }',
            '.title-content { margin: 0; }',
            '.element { position: absolute; }',
            '.topalign { display: flex; justify-content: flex-start; flex-direction: column; } ',
            '.botalign { display: flex; justify-content: flex-end; flex-direction: column;  } ',
            '.centeralign { display: flex; justify-content: center; flex-direction: column;  } ',
            'body { margin: 0; }'
            '</style>',
        ])

    def _html_color(self, rgb) -> str:
        return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"

    def _make_image(self, c: ImageComponent, dims, pos, elem_id):
        # Generate the image data
        elem_idx = self._prefix + "img-" + elem_id
        imgtag = c.data.make_html(c.bounds.width, c.bounds.height)

        html_code = f"<div class='element' id='{elem_idx}' style='"
        html_code += dims + pos

        # Check if there is a frame and emit the correct command
        frame = ""
        if c.has_frame:
            frame += f"<div style='position: absolute; top: 0; left: 0; " + dims
            frame += f"border: {c.frame_linewidth}pt solid "
            frame += f"{self._html_color(c.frame_color)}; box-sizing: border-box;'></div>"

        html_code += "' >" + imgtag + frame + "</div>"
        return html_code

    def assemble_grid(self, components: List[Component], output_dir: str):
        html_lines = []
        for c in components:
            elem_id = f"fig{c.figure_idx}-grid{c.grid_idx}"
            if c.row_idx >= 0:
                elem_id += f"-row{c.row_idx}"
            if c.col_idx >= 0:
                elem_id += f"-col{c.col_idx}"

            # Position arguments are the same for all components
            if c.bounds is not None:
                pos = f"top: {c.bounds.top}mm; left: {c.bounds.left}mm; "
                dims = f"width: {c.bounds.width}mm; height: {c.bounds.height}mm;"

            if isinstance(c, ImageComponent):
                html_lines.append(self._thread_pool.submit(self._make_image, c, dims, pos, elem_id))

            if isinstance(c, TextComponent):
                elem_idx = self._prefix + c.type + "-" + elem_id

                color = "color: " + self._html_color(c.color) + "; "
                fontsize = "font-size: " + f'{c.fontsize}pt' + "; "
                horz_align = "text-align: " + c.horizontal_alignment + "; "

                rotation = ""
                if c.rotation == -90:
                    rotation = f"transform: rotate(90deg) translateX({-c.bounds.width}mm);"
                    rotation += "transform-origin: bottom left;"
                elif c.rotation == 90:
                    rotation = f"transform: rotate(-90deg) translateX({-c.bounds.height}mm);"
                    rotation += "transform-origin: top left;"

                # Need to flip the dimensions if we rotate
                if rotation != "":
                    dims = f"width: {c.bounds.height}mm; height: {c.bounds.width}mm;"

                if c.background_color is not None:
                    bgn = "background-color: " + self._html_color(c.background_color) + "; "
                else:
                    bgn = ""
                pad = f"padding-top: {c.padding.height_mm}mm; padding-bottom: {c.padding.height_mm}mm; "
                pad += f"padding-left: {c.padding.width_mm}mm; padding-right: {c.padding.width_mm}mm; "
                pad += "box-sizing: border-box; "

                aligncls = "centeralign"
                if c.vertical_alignment == "top":
                    aligncls = "topalign"
                elif c.vertical_alignment == "bottom":
                    aligncls = "botalign"

                html_lines.append("\n".join([
                    f"<div class='title-container {aligncls}' id='{elem_idx}' style='" + dims + pos
                        + pad + bgn + rotation + "' >",
                    "<p class='title-content' style='" + color + fontsize + horz_align + "'>",
                    c.content.replace('\\\\', '<br/>'),
                    "</p>",
                    "</div>"
                ]))

            if isinstance(c, RectangleComponent):
                html_code = "<div style='position: absolute; " + dims + pos
                html_code += f"border: {c.linewidth}pt {self._html_color(c.color)}"
                html_code += 'dashed' if c.dashed else 'solid' + "; "
                html_code += "'></div>"
                html_lines.append(html_code)

            if isinstance(c, LineComponent):
                html_code = f'<div class="svg-container" style="position: absolute; {dims + pos}">'
                html_code += f'<svg style="{dims}">'
                html_code += f'<line x1="{c.from_x - c.bounds.left}mm" y1="{c.from_y - c.bounds.top}mm" '
                html_code += f'x2="{c.to_x - c.bounds.left}mm" y2="{c.to_y - c.bounds.top}mm" '
                html_code += f'style="stroke:{self._html_color(c.color)}; stroke-width:{c.linewidth}pt" />'
                html_code += '</svg></div>'
                html_lines.append(html_code)

        return html_lines

    def combine_grids(self, data: List[List[Union[str, Future]]], idx: int, bounds: Bounds) -> List[Union[str, Future]]:
        # Create a container div for each row
        figure_id = self._prefix + "figure-" + str(idx)
        pos = f"top: {bounds.top}mm; left: {bounds.left}mm; "
        dims = f"width: {bounds.width}mm; height: {bounds.height}mm; "

        # Flatten the inner lines and combine
        result = ["<div id='" + figure_id + "' style='" + pos + dims + "'>"]
        for grid in data:
            for line in grid:
                result.append(line)
        result.append("</div>")

        return result

    def combine_rows(self, data: List[List[Union[str, Future]]], bounds: Bounds) -> str:
        # Create a container div to make sure that everything can be moved around on a final page
        pos = f"top: {bounds.top}mm; left: {bounds.left}mm; "
        dims = f"width: {bounds.width}mm; height: {bounds.height}mm; "

        # Synchronize all export tasks
        html_code = "<div class='figure' style='" + pos + dims + "'>\n"
        for row in data:
            for line in row:
                if isinstance(line, Future):
                    html_code += line.result() + "\n"
                else:
                    html_code += line + "\n"
        html_code += "</div>\n"
        return html_code

    def write_to_file(self, data: str, filename: str):
        with open(filename, "w") as f:
            if not self._inline:
                f.writelines([
                    "<!DOCTYPE html>",
                    "<html>",
                    "<head>",
                ])
                f.write(self.style)
                f.write(self._custom_head)
                f.writelines([
                    "</head>"
                    "<body>"
                ])

            f.write(data)

            if not self._inline:
                f.write("</body>")
