import framebuf
from lib.display.ili934xnew import color565
from math import cos, sin, pi, radians
import lib.fonts.glcdfont

class FFrameBuffer(framebuf.FrameBuffer):
  def __init__(self, buf = None, width = 240, height=320, colorscheme = framebuf.RGB565):
    self.width = width
    self.height = height
    self._colorscheme = colorscheme
    if buf is None:
      buf = bytearray(width * heigth * 2)
    super(FFrameBuffer, self).__init__(buf, w, h, colorscheme)
    self.buf = buf
     
class DisplayExt():
  
  def __init__(self, base = None, width = 240, height = 320, colorscheme = framebuf.RGB565):
    self._width = width
    self._height = height
    if base is None:
      buf = bytearray(width * height * 2)
      base = FFrameBuffer(buf, width, height, colorscheme)
    self.base = base
    self.colorscheme = colorscheme
    self._scroll = 0
    self.fcolor = 0xffff
    self.bcolor = 0x0000
    self._x = 0
    self._y = 0
    self._font = lib.fonts.glcdfont
    self.scrolling = False

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

  def fill_rect(self, x, y, w, h, c):
    return self.base.fill_rect(x, y, w, h, c)

  def text(self, s, x, y, c = None):
    return self.base.text(s, x, y, c)

  def scroll(self, xstep, ystep):
    """Shift the contents of the FrameBuffer by the given vector. 
    This may leave a footprint of the previous colors in the FrameBuffer."""
    return self.base.scroll(xstep, ystep)

  def blit(self, fbuf, x, y, key = None):
    """Draw another FrameBuffer on top of the current one at the given coordinates. 
    If key is specified then it should be a color integer and the corresponding color will be considered transparent: 
    all pixels with that color value will not be drawn.

    This method works between FrameBuffer instances utilising different formats, 
    but the resulting colors may be unexpected due to the mismatch in color formats."""

    self.base.blit(fbuf, x, y, key)


###########################################

  def draw_lines(self, coords, color):
    """Draw multiple lines.

    Args:
      coords ([[int, int],...]): Line coordinate X, Y pairs
      color (int): RGB565 color value.
    """
    # Starting point
    x1, y1 = coords[0]
    # Iterate through coordinates
    for i in range(1, len(coords)):
      x2, y2 = coords[i]
      self.base.line(x1, y1, x2, y2, color)
      x1, y1 = x2, y2
  
  def draw_circle(self, x0, y0, r, color):
    """Draw a circle.

    Args:
      x0 (int): X coordinate of center point.
      y0 (int): Y coordinate of center point.
      r (int): Radius.
      color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r
    self.base.pixel(x0, y0 + r, color)
    self.base.pixel(x0, y0 - r, color)
    self.base.pixel(x0 + r, y0, color)
    self.base.pixel(x0 - r, y0, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      self.base.pixel(x0 + x, y0 + y, color)
      self.base.pixel(x0 - x, y0 + y, color)
      self.base.pixel(x0 + x, y0 - y, color)
      self.base.pixel(x0 - x, y0 - y, color)
      self.base.pixel(x0 + y, y0 + x, color)
      self.base.pixel(x0 - y, y0 + x, color)
      self.base.pixel(x0 + y, y0 - x, color)
      self.base.pixel(x0 - y, y0 - x, color)

  def fill_circle(self, x0, y0, r, color):
    """Draw a filled circle.

    Args:
      x0 (int): X coordinate of center point.
      y0 (int): Y coordinate of center point.
      r (int): Radius.
      color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r
    self.base.vline(x0, y0 - r, 2 * r + 1, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      self.base.vline(x0 + x, y0 - y, 2 * y + 1, color)
      self.base.vline(x0 - x, y0 - y, 2 * y + 1, color)
      self.base.vline(x0 - y, y0 - x, 2 * x + 1, color)
      self.base.vline(x0 + y, y0 - x, 2 * x + 1, color)

  def fill_ellipse(self, x0, y0, a, b, color):
    """Draw a filled ellipse.

    Args:
      x0, y0 (int): Coordinates of center point.
      a (int): Semi axis horizontal.
      b (int): Semi axis vertical.
      color (int): RGB565 color value.
    Note:
      The center point is the center of the x0,y0 pixel.
      Since pixels are not divisible, the axes are integer rounded
      up to complete on a full pixel.  Therefore the major and
      minor axes are increased by 1.
    """
    a2 = a * a
    b2 = b * b
    twoa2 = a2 + a2
    twob2 = b2 + b2
    x = 0
    y = b
    px = 0
    py = twoa2 * y
    # Plot initial points
    self.base.line(x0, y0 - y, x0, y0 + y, color)
    # Region 1
    p = round(b2 - (a2 * b) + (0.25 * a2))
    while px < py:
      x += 1
      px += twob2
      if p < 0:
        p += b2 + px
      else:
        y -= 1
        py -= twoa2
        p += b2 + px - py
      self.base.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
      self.base.line(x0 - x, y0 - y, x0 - x, y0 + y, color)
    # Region 2
    p = round(b2 * (x + 0.5) * (x + 0.5) +
          a2 * (y - 1) * (y - 1) - a2 * b2)
    while y > 0:
      y -= 1
      py -= twoa2
      if p > 0:
        p += a2 - py
      else:
        x += 1
        px += twob2
        p += a2 - py + px
      self.base.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
      self.base.line(x0 - x, y0 - y, x0 - x, y0 + y, color)

  def draw_ellipse(self, x0, y0, a, b, color):
    """Draw an ellipse.

    Args:
      x0, y0 (int): Coordinates of center point.
      a (int): Semi axis horizontal.
      b (int): Semi axis vertical.
      color (int): RGB565 color value.
    Note:
      The center point is the center of the x0,y0 pixel.
      Since pixels are not divisible, the axes are integer rounded
      up to complete on a full pixel.  Therefore the major and
      minor axes are increased by 1.
    """
    a2 = a * a
    b2 = b * b
    twoa2 = a2 + a2
    twob2 = b2 + b2
    x = 0
    y = b
    px = 0
    py = twoa2 * y
    # Plot initial points
    self.base.pixel(x0 + x, y0 + y, color)
    self.base.pixel(x0 - x, y0 + y, color)
    self.base.pixel(x0 + x, y0 - y, color)
    self.base.pixel(x0 - x, y0 - y, color)
    # Region 1
    p = round(b2 - (a2 * b) + (0.25 * a2))
    while px < py:
      x += 1
      px += twob2
      if p < 0:
        p += b2 + px
      else:
        y -= 1
        py -= twoa2
        p += b2 + px - py
      self.base.pixel(x0 + x, y0 + y, color)
      self.base.pixel(x0 - x, y0 + y, color)
      self.base.pixel(x0 + x, y0 - y, color)
      self.base.pixel(x0 - x, y0 - y, color)
    # Region 2
    p = round(b2 * (x + 0.5) * (x + 0.5) +
          a2 * (y - 1) * (y - 1) - a2 * b2)
    while y > 0:
      y -= 1
      py -= twoa2
      if p > 0:
        p += a2 - py
      else:
        x += 1
        px += twob2
        p += a2 - py + px
      self.base.pixel(x0 + x, y0 + y, color)
      self.base.pixel(x0 - x, y0 + y, color)
      self.base.pixel(x0 + x, y0 - y, color)
      self.base.pixel(x0 - x, y0 - y, color)

  def draw_rrectangle(self, x0=50, y0=50, w=30, h=50, r=10, color=color565(64, 64, 255)):
    """Draw a circle.

    Args:
      x0 (int): X coordinate of center point.
      y0 (int): Y coordinate of center point.
      r (int): Radius.
      color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r

    self.base.hline(x0 + r, y0    , 2 + w - 2 * r, color)
    self.base.hline(x0 + r, y0 + h - 1, 2 + w - 2 * r, color)
    self.base.vline(x0    , y0 + r, 2 + h - 2 * r, color)
    self.base.vline(x0 + w - 1, y0 + r, 2 + h - 2 * r, color)

    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx

      # Top-Left
      self.base.pixel(x0 - x + r, y0 - y + r, color)
      self.base.pixel(x0 - y + r, y0 - x + r, color)

      # Top-Right
      self.base.pixel(x0 + w + x - r - 1, y0 - y + r, color)
      self.base.pixel(x0 + w + y - r - 1, y0 - x + r, color)

      # Bottom-Left
      self.base.pixel(x0 - x + r, y0 + h + y - r - 1, color)
      self.base.pixel(x0 - y + r, y0 + h + x - r - 1, color)

      # Bottom-Right
      self.base.pixel(x0 + w + x - r - 1, y0 + h + y - r - 1, color)
      self.base.pixel(x0 + w + y - r - 1, y0 + h + x - r - 1, color)

  def fill_rrectangle(self, x0=100, y0=200, w=50, h=70, r=10, color=color565(64, 64, 255)):
    """Draw a filled circle.

    Args:
      x0 (int): X coordinate of center point.
      y0 (int): Y coordinate of center point.
      r (int): Radius.
      color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r
    
    w2 = int(w - 2 * r)
    h2 = int(h - 2 * r)

    self.base.fill_rect(x0 + r, y0, w2, h, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      
      # Left
      self.base.vline(x0 - x + r, y0 - y + r, h2 + 2 * y, color)
      self.base.vline(x0 - y + r, y0 - x + r, h2 + 2 * x, color)

      #right 1
      self.base.vline(x0 + w + x - r - 1, y0 - y + r, h2 + 2 * y, color)
      #right 2
      self.base.vline(x0 + w + y - r - 1, y0 - x + r, h2 + 2 * x, color)

  def fill_polygon(self, sides, x0, y0, r, color, rotate=0):
    """Draw a filled n-sided regular polygon.

    Args:
      sides (int): Number of polygon sides.
      x0, y0 (int): Coordinates of center point.
      r (int): Radius.
      color (int): RGB565 color value.
      rotate (Optional float): Rotation in degrees relative to origin.
    Note:
      The center point is the center of the x0,y0 pixel.
      Since pixels are not divisible, the radius is integer rounded
      up to complete on a full pixel.  Therefore diameter = 2 x r + 1.
    """
    # Determine side coordinates
    coords = []
    theta = radians(rotate)
    n = sides + 1
    for s in range(n):
      t = 2.0 * pi * s / sides + theta
      coords.append([int(r * cos(t) + x0), int(r * sin(t) + y0)])
    # Starting point
    x1, y1 = coords[0]
    # Minimum Maximum X dict
    xdict = {y1: [x1, x1]}
    # Iterate through coordinates
    for row in coords[1:]:
      x2, y2 = row
      xprev, yprev = x2, y2
      # Calculate perimeter
      # Check for horizontal side
      if y1 == y2:
        if x1 > x2:
          x1, x2 = x2, x1
        if y1 in xdict:
          xdict[y1] = [min(x1, xdict[y1][0]), max(x2, xdict[y1][1])]
        else:
          xdict[y1] = [x1, x2]
        x1, y1 = xprev, yprev
        continue
      # Non horizontal side
      # Changes in x, y
      dx = x2 - x1
      dy = y2 - y1
      # Determine how steep the line is
      is_steep = abs(dy) > abs(dx)
      # Rotate line
      if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
      # Swap start and end points if necessary
      if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
      # Recalculate differentials
      dx = x2 - x1
      dy = y2 - y1
      # Calculate error
      error = dx >> 1
      ystep = 1 if y1 < y2 else -1
      y = y1
      # Calcualte minimum and maximum x values
      for x in range(x1, x2 + 1):
        if is_steep:
          if x in xdict:
            xdict[x] = [min(y, xdict[x][0]), max(y, xdict[x][1])]
          else:
            xdict[x] = [y, y]
        else:
          if y in xdict:
            xdict[y] = [min(x, xdict[y][0]), max(x, xdict[y][1])]
          else:
            xdict[y] = [x, x]
        error -= abs(dy)
        if error < 0:
          y += ystep
          error += dx
      x1, y1 = xprev, yprev
    # Fill polygon
    for y, x in xdict.items():
      self.base.hline(x[0], y, x[1] - x[0] + 2, color)

  def draw_polygon(self, sides, x0, y0, r, color, rotate=0):
    """Draw an n-sided regular polygon.

    Args:
      sides (int): Number of polygon sides.
      x0, y0 (int): Coordinates of center point.
      r (int): Radius.
      color (int): RGB565 color value.
      rotate (Optional float): Rotation in degrees relative to origin.
    Note:
      The center point is the center of the x0,y0 pixel.
      Since pixels are not divisible, the radius is integer rounded
      up to complete on a full pixel.  Therefore diameter = 2 x r + 1.
    """
    coords = []
    theta = radians(rotate)
    n = sides + 1
    for s in range(n):
      t = 2.0 * pi * s / sides + theta
      coords.append([int(r * cos(t) + x0), int(r * sin(t) + y0)])

    # Cast to python float first to fix rounding errors
    self.base.draw_lines(coords, color=color)

  def load_sprite(self, path, w, h):
    """Load sprite image.

    Args:
      path (string): Image file path.
      w (int): Width of image.
      h (int): Height of image.
    Notes:
      w x h cannot exceed 2048
    """
    buf_size = w * h * 2
    with open(path, "rb") as f:
      return bytearray(f.read(buf_size))

  def draw_sprite(self, buf, x, y, w, h):
    """Draw a sprite (optimized for horizontal drawing).

    Args:
      buf (bytearray): Buffer to draw.
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of drawing.
      h (int): Height of drawing.
    """
    s = framebuf.FrameBuffer(buf, w, h, self.colorscheme)
    self.blit(s, x, y, 0)

  # def draw_image(self, path, x=0, y=0, w=320, h=240):
  #   """Draw image from flash.

  #   Args:
  #     path (string): Image file path.
  #     x (int): X coordinate of image left.  Default is 0.
  #     y (int): Y coordinate of image top.  Default is 0.
  #     w (int): Width of image.  Default is 320.
  #     h (int): Height of image.  Default is 240.
  #   """
  #   x2 = x + w - 1
  #   y2 = y + h - 1
  #   if self.base.is_off_grid(x, y, x2, y2):
  #     return
  #   with open(path, "rb") as f:
  #     chunk_height = 1024 // w
  #     chunk_count, remainder = divmod(h, chunk_height)
  #     chunk_size = chunk_height * w * 2
  #     chunk_y = y
  #     if chunk_count:
  #       for c in range(0, chunk_count):
  #         buf = f.read(chunk_size)
  #         self.base._writeblock(x, chunk_y,
  #                x2, chunk_y + chunk_height - 1,
  #                buf)
  #         chunk_y += chunk_height
  #     if remainder:
  #       buf = f.read(remainder * w * 2)
  #       self._writeblock(x, chunk_y,
  #              x2, chunk_y + remainder - 1,
  #              buf)


###############################################
###############################################
  def set_color(self,fg,bg):
    self.bcolor = bg
    self.fcolor = fg

  def set_pos(self,x,y):
    self._x = x
    self._y = y

  def reset_scroll(self):
    self.scrolling = False
    self._scroll = 0
    #self.scroll_y(0)

  def set_font(self, font):
    ret = self._font
    self._font = font
    return ret

  def chars(self, str, x, y):
    str_w = self._font.get_width(str)
    div, rem = divmod(self._font.height(),8)
    nbytes = div+1 if rem else div
    pos = 0
    #mx = 0
    #my = 0
    for ch in str:
      glyph, char_w = self._font.get_ch(ch)
      for row in range(nbytes):
        start = 0
        end = 8
        if (row+1) * 8 > self._font.height():
          end = rem
        for bit in range(start, end):
          for i in range(char_w):
            if (glyph[nbytes*i+row] & (1 << bit)):
              if self.fcolor is not None:
                self.base.pixel(pos + i, y + (row * 8) + bit, self.fcolor)
            else:
              if self.bcolor is not None:
                self.base.pixel(pos + i, y + (row * 8) + bit, self.bcolor)
            #mx = max(mx, i)
            #my = max(my, row * 8 + bit)
      pos += char_w
    #print('pos = ({}, {})'.format(mx, my))
    return x + str_w

  # def scroll_y(self, dy):
  #   self._scroll = (self._scroll + dy) % self._height
  #   self.write_cmd(self.VSCRSADD, ustruct.pack(">H", self._scroll))

  def next_line(self, cury, char_h):
    # global scrolling
    # if not self.scrolling:
    res = cury + char_h
    #   self.scrolling = (res >= self._height)
    # if self.scrolling:
    #   self.scroll_y(char_h)
    #   res = (self._height - char_h + self._scroll) % self._height
    #   self.base.fill_rect(0, res, self._width, self._font.height())
    return res

  def write(self, text): #does character wrap, compatible with stream output
    curx = self._x; cury = self._y
    char_h = self._font.height()
    width = 0
    written = 0
    for pos, ch in enumerate(text):
      if ch == '\n':
        if pos>0:
          self.chars(text[written:pos],curx,cury)
        curx = 0; written = pos+1; width = 0
        cury = self.next_line(cury,char_h)
      else:
        char_w = self._font.get_width(ch)
        if curx + width + char_w >= self._width:
          self.chars(text[written:pos], curx,cury)
          curx = 0 ; written = pos; width = char_h
          cury = self.next_line(cury,char_h)
        else:
          width += char_w
    if written<len(text):
      curx = self.chars(text[written:], curx,cury)
    self._x = curx; self._y = cury

  def print(self, text): #does word wrap, leaves self._x unchanged
    cury = self._y
    curx = self._x
    char_h = self._font.height()
    char_w = self._font.max_width()
    lines = text.split('\n')
    for line in lines:
      words = line.split(' ')
      for word in words:
        if curx + self._font.get_width(word) >= self._width:
          curx = self._x
          cury = self.next_line(cury,char_h)
          while self._font.get_width(word) > self._width:
            self.chars(word[:self._width//char_w],curx,cury)
            word = word[self._width//char_w:]
            cury = self.next_line(cury,char_h)
        if len(word)>0:
          curx = self.chars(word + ' ', curx, cury)
      curx = self._x
      cury = self.next_line(cury, char_h)
    self._y = cury

  def get_stringsize(self, s):
      hor = 0
      for c in s:
          fontptr, vert, cols = self._font.get_ch(ord(c))
          hor += cols
      return hor, vert

  def print_centered(self, x, y, s):
      length, height = self.get_stringsize(s)
      self.set_pos(x - length // 2, y - height // 2)
      self.print(s)

  def get_screensize(self):
    return self._width, self._height 

  def is_off_grid(self, xmin, ymin, xmax, ymax):
    """Check if coordinates extend past display boundaries.

    Args:
      xmin (int): Minimum horizontal pixel.
      ymin (int): Minimum vertical pixel.
      xmax (int): Maximum horizontal pixel.
      ymax (int): Maximum vertical pixel.
    Returns:
      boolean: False = Coordinates OK, True = Error.
    """
    if xmin < 0:
      print('x-coordinate: {0} below minimum of 0.'.format(xmin))
      return True
    if ymin < 0:
      print('y-coordinate: {0} below minimum of 0.'.format(ymin))
      return True
    if xmax >= self._width:
      print('x-coordinate: {0} above maximum of {1}.'.format(
        xmax, self._width - 1))
      return True
    if ymax >= self._height:
      print('y-coordinate: {0} above maximum of {1}.'.format(
        ymax, self._height - 1))
      return True
    return False

