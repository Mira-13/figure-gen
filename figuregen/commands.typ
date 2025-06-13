/// Places an image with exact size and position, with an optional frame
#let place-image(size, position, filename, stroke: none) = {
  place(
    dx: position.x, dy: position.y,
    block(
      width: size.width, height: size.height,
      stroke: stroke, outset: if stroke == none {0pt} else {-stroke.thickness*0.5}, clip: true,
      image(filename, fit: "stretch", width: 100%, height: 100%)
    )
  )
}

/// Places a textbox that clips its content to cover the exact specified area
/// Additional styling arguments will be forwarded to `block()`
#let text-box(
  size,
  position,
  text-color,
  fontsize,
  fill-color,
  rotation,
  alignment,
  padding,
  content
) = {
  set text(size: fontsize, fill: text-color, top-edge: "ascender", bottom-edge: "descender")
  let sz = if rotation != 0deg { (size.height, size.width) } else { (size.width, size.height)}
  let shift = if rotation != 0deg { (size.width/2 - size.height/2, size.height/2 - size.width/2) } else { (0pt, 0pt)}
  place(
    dx: position.x, dy: position.y,
    move(dx: shift.at(0), dy: shift.at(1),
      rotate(rotation, origin: center + horizon,
        block(
          fill: fill-color,
          width: sz.at(0), height: sz.at(1),
          align(alignment, content),
          inset: (top: padding.y, bottom: padding.y, left: padding.x, right: padding.x),
          clip: true
        )
      )
    )
  )
}

/// Places a line inside a figure region, clipped to the parent bounds
#let clipped-line(
  size, position,
  start, end, stroke,
) = {
  place(
    dx: position.x, dy: position.y,
    block(
      width: size.width, height: size.height,
      curve(
        stroke: stroke,
        curve.move((start.at(0) - position.x, start.at(1) - position.y)),
        curve.line((end.at(0) - position.x, end.at(1) - position.y)),
      ),
      clip: true,
    )
  )
}

/// Places a rectangle inside a figure region, clipped to the parent bounds
#let clipped-rectangle(
  size, position, stroke: 1pt + black, fill: none
) = {
  place(dx: position.x, dy: position.y, rect(width: size.width, height: size.height, stroke: stroke, fill: fill, outset: -stroke.thickness/2))
}