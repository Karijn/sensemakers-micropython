




class DisplayExt():
  def __init__(self, base):
    self.base = base

  def fill(self, c):
    """Fill the entire FrameBuffer with the specified color."""
    return self.base.fill(c)

  def pixel(self, x, y, c = None):
    """If c is not given, get the color value of the specified pixel. 
    If c is given, set the specified pixel to the given color."""
    return self.base.pixel(x, y, c)

  def hline(self, x, y, w, c):
    return self.base.hline(x, y, w, c)

  def vline(self, x, y, h, c):
    return self.base.vline(x, y, h, c)

  def line(self, x1, y1, x2, y2, c):
    """Draw a line from a set of coordinates using the given color and a thickness of 1 pixel.
    The line method draws the line up to a second set of coordinates whereas 
    the hline and vline methods draw horizontal and vertical lines respectively up to a given length."""
    return self.base.line(x1, y1, x2, y2, c)

  def rect(self, x, y, w, h, c):
    """fill_rect(x, y, w, h, c)
    Draw a rectangle at the given location, size and color. 
    The rect method draws only a 1 pixel outline whereas the fill_rect method draws both the outline and interior."""
    return self.base.rect(x, y, w, h, c)

  def scroll(self, xstep, ystep):
    "Shift the contents of the FrameBuffer by the given vector. 
    This may leave a footprint of the previous colors in the FrameBuffer.""
    return self.base.scroll(xstep, ystep)

  def blit(self, fbuf, x, y, key = None):
    """Draw another FrameBuffer on top of the current one at the given coordinates. 
    If key is specified then it should be a color integer and the corresponding color will be considered transparent: 
    all pixels with that color value will not be drawn.

    This method works between FrameBuffer instances utilising different formats, 
    but the resulting colors may be unexpected due to the mismatch in color formats."""
    return self.base.blit(fbuf, x, y, key)

