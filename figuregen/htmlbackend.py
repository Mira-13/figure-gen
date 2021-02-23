from .backend import *

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

    def assemble_grid(self, components: List[Component], output_dir: str):
        html_code = ""
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
                # Generate the image data
                elem_idx = self._prefix + "img-" + elem_id
                imgtag = c.data.make_html(c.bounds.width, c.bounds.height)

                html_code += f"<div class='element' id='{elem_idx}' style='"
                html_code += dims + pos

                # Check if there is a frame and emit the correct command
                frame = ""
                if c.has_frame:
                    frame += f"<div style='position: absolute; top: 0; left: 0; " + dims
                    frame += f"border: {c.frame_linewidth}pt solid "
                    frame += f"{self._html_color(c.frame_color)}; box-sizing: border-box;'></div>"

                html_code += "' >" + imgtag + frame + "</div>\n"

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

                bgn = "background-color: " + self._html_color(c.background_color) + "; "
                pad = f"padding-top: {c.padding.height_mm}mm; padding-bottom: {c.padding.height_mm}mm; "
                pad += f"padding-left: {c.padding.width_mm}mm; padding-right: {c.padding.width_mm}mm; "
                pad += "box-sizing: border-box; "

                aligncls = "centeralign"
                if c.vertical_alignment == "top":
                    aligncls = "topalign"
                elif c.vertical_alignment == "bottom":
                    aligncls = "botalign"

                html_code += "\n".join([
                    f"<div class='title-container {aligncls}' id='{elem_idx}' style='" + dims + pos
                        + pad + bgn + rotation + "' >",
                    "<p class='title-content' style='" + color + fontsize + horz_align + "'>",
                    c.content.replace('\\\\', '<br/>'),
                    "</p>",
                    "</div>",
                    ""
                ])

            if isinstance(c, RectangleComponent):
                html_code += "<div style='position: absolute; " + dims + pos
                html_code += f"border: {c.linewidth}pt {self._html_color(c.color)}"
                html_code += 'dashed' if c.dashed else 'solid' + "; "
                html_code += "'></div>"

            if isinstance(c, LineComponent):
                pass
                # parent_name = "{" + "img-" + elem_id + "}"
                # color = "{" + self._latex_color(c.color) + "}"
                # linewidth = "{" + str(c.linewidth) + "pt}"
                # start = "{" + f"({c.from_x}mm, {-c.from_y}mm)"+ "}"
                # end = "{" + f"({c.to_x}mm, {-c.to_y}mm)"+ "}"
                # tikz_code += "\\makeclippedline" + parent_name + start + end + linewidth + color + "\n"

        return html_code

    def combine_grids(self, data: List[str], idx: int, bounds: Bounds) -> str:
        # Create a container div for each row
        figure_id = self._prefix + "figure-" + str(idx)
        pos = f"top: {bounds.top}mm; left: {bounds.left}mm; "
        dims = f"width: {bounds.width}mm; height: {bounds.height}mm; "

        html_code = "<div id='" + figure_id + "' style='" + pos + dims + "'>\n"
        html_code += '\n'.join(data)
        html_code += "</div>\n"

        return html_code

    def combine_rows(self, data: List[str], bounds: Bounds) -> str:
        # Create a container div to make sure that everything can be moved around on a final page
        pos = f"top: {bounds.top}mm; left: {bounds.left}mm; "
        dims = f"width: {bounds.width}mm; height: {bounds.height}mm; "

        html_code = "<div class='figure' style='" + pos + dims + "'>\n"
        html_code += '\n'.join(data)
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
