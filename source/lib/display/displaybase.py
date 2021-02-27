
import framebuf

class FrameBufferEx(framebuf.FrameBuffer):
  def __init__(self, width=240, height=320):
    print('init FrameBufferEx {}, {}'.format(width, height))
    self.width = width
    self.height = height
    self._buffer = bytearray(self.width * self.height * 2)
    super().__init__(self._buffer, self.width, self.height, framebuf.RGB565)

  def clear(self, color=0):
    """Clear display.

    Args:
      color (Optional int): RGB565 color value (Default: 0 = Black).
    """
    self.fill(color)

  def show(self):
    pass

class SwappedFrameBuffer(framebuf.FrameBuffer):

  def __init__(self, width=240, height=320):
    print('init SwappedFrameBuffer {}, {}'.format(width, height))
    self.width = width
    self.height = height
    self._buffer = bytearray(self.width * self.height * 2)
    super().__init__(self._buffer, self.width, self.height, framebuf.RGB565)

  def fill(self, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().fill(c)

  def pixel(self, x, y, c = None):
    if ( c is None):
      c = super().pixel(x, y)
      return ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().pixel(x, y, c)

  def hline(self, x, y, w, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().hline(x, y, w, c)

  def vline(self, x, y, h, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().vline(x, y, h, c)

  def line(self, x1, y1, x2, y2, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().line(x1, y1, x2, y2, c)

  def rect(self, x, y, w, h, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().rect(x, y, w, h, c)

  def fill_rect(self, x, y, w, h, c):
    c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
    super().fill_rect(x, y, w, h, c)

  def text(self, s, x, y, c = None):
    if c is not None:
      c = ((c & 0xff ) << 8) | ((c & 0xff00 ) >> 8)
      super().text(s, x, y, c)
    else:
      super().text(s, x, y)

  # def scrollself, (xstep, ystep):
  #   super().scroll(xstep, ystep)

  def blit(self, fbuf, x, y, key = None):
    if key is not None:
      key = ((key & 0xff ) << 8) | ((key & 0xff00 ) >> 8)
      super().blit(fbuf, x, y, key)
    else:
      super().blit(fbuf, x, y)

  def clear(self, color=0):
    """Clear display.

    Args:
      color (Optional int): RGB565 color value (Default: 0 = Black).
    """
    self.fill(color)

  def show(self):
    pass
