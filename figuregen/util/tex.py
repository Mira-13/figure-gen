
def outline(text: str, outline_clr=[10,10,10], text_clr=[250,250,250]) -> str:
    """ Creates a colored outline around the given text.

    Requires the "contour" package in the preamble, preferably with the [outline] option. That is:
    \usepackage[outline]{contour}

    Currently, this package is not included by default - might change in the future.

    Args:
        text: The text to outline
        outline_clr: Color of the outline as an sRGB triple
        text_clr: Color of the text as an sRGB triple

    Returns:
        LaTeX code to render the outlined text with the specified colors.
    """
    if outline_clr is None:
        res = "\\definecolor{FillClr}{RGB}{" + f"{text_clr[0]},{text_clr[1]},{text_clr[2]}" + "}"
        return res + "\\textcolor{FillClr}{" + text + "}"

    res = "\\DeclareDocumentCommand{\\Outlined}{ O{black} O{white} O{0.55pt} m }{"\
            "\\contourlength{#3}"\
            "\\contour{#2}{\\textcolor{#1}{#4}}"\
        "}"
    res += "\\definecolor{FillClr}{RGB}{" + f"{text_clr[0]},{text_clr[1]},{text_clr[2]}" + "}"
    res += "\\definecolor{StrokeClr}{RGB}{" + f"{outline_clr[0]},{outline_clr[1]},{outline_clr[2]}" + "}"

    res += "\\Outlined[FillClr][StrokeClr][0.55pt]{"+ text + "}"
    return res