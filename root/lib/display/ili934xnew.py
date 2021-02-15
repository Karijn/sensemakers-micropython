# This is an adapted version of the ILI934X driver as below.
# It works with multiple fonts and also works with the esp32 H/W SPI implementation
# Also includes a word wrap print function
# Proportional fonts are generated by Peter Hinch's Font-to-py
# MIT License; Copyright (c) 2017 Jeffrey N. Magee

# This file is part of MicroPython ILI934X driver
# Copyright (c) 2016 - 2017 Radomir Dopieralski, Mika Tuupola
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
# Project home:
#   https://github.com/tuupola/micropython-ili934x

import time
import ustruct
import fonts.glcdfont
import framebuf
from micropython import const
from math import cos, sin, pi, radians

_RDDSDR = const(0x0f) # Read Display Self-Diagnostic Result

_DTCTRLA = const(0xe8) # Driver Timing Control A
_DTCTRLB = const(0xea) # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7) # Pump Ratio Control
_PWCTRL1 = const(0xc0) # Power Control 1
_PWCTRL2 = const(0xc1) # Power Control 2
_VMCTRL1 = const(0xc5) # VCOM Control 1
_VMCTRL2 = const(0xc7) # VCOM Control 2
_FRMCTR1 = const(0xb1) # Frame Rate Control 1
_DISCTRL = const(0xb6) # Display Function Control
_ENA3G = const(0xf2) # Enable 3G
_PGAMCTRL = const(0xe0) # Positive Gamma Control
_NGAMCTRL = const(0xe1) # Negative Gamma Control

_CHUNK = const(1024) #maximum number of pixels per spi write

def color565(r, g, b):
  return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

class ILI9341:

  # Command constants from ILI9341 datasheet
  NOP = const(0x00)  # No-op
  SWRESET = const(0x01)  # Software reset
  RDDID = const(0x04)  # Read display ID info
  RDDST = const(0x09)  # Read display status
  SLPIN = const(0x10)  # Enter sleep mode
  SLPOUT = const(0x11)  # Exit sleep mode
  PTLON = const(0x12)  # Partial mode on
  NORON = const(0x13)  # Normal display mode on
  RDMODE = const(0x0A)  # Read display power mode
  RDMADCTL = const(0x0B)  # Read display MADCTL
  RDPIXFMT = const(0x0C)  # Read display pixel format
  RDIMGFMT = const(0x0D)  # Read display image format
  RDSELFDIAG = const(0x0F)  # Read display self-diagnostic
  INVOFF = const(0x20)  # Display inversion off
  INVON = const(0x21)  # Display inversion on
  GAMMASET = const(0x26)  # Gamma set
  DISPLAY_OFF = const(0x28)  # Display off
  DISPLAY_ON = const(0x29)  # Display on
  SET_COLUMN = const(0x2A)  # Column address set
  SET_PAGE = const(0x2B)  # Page address set
  WRITE_RAM = const(0x2C)  # Memory write
  READ_RAM = const(0x2E)  # Memory read
  PTLAR = const(0x30)  # Partial area
  VSCRDEF = const(0x33)  # Vertical scrolling definition
  MADCTL = const(0x36)  # Memory access control
  VSCRSADD = const(0x37)  # Vertical scrolling start address
  PIXFMT = const(0x3A)  # COLMOD: Pixel format set
  FRMCTR1 = const(0xB1)  # Frame rate control (In normal mode/full colors)
  FRMCTR2 = const(0xB2)  # Frame rate control (In idle mode/8 colors)
  FRMCTR3 = const(0xB3)  # Frame rate control (In partial mode/full colors)
  INVCTR = const(0xB4)  # Display inversion control
  DFUNCTR = const(0xB6)  # Display function control
  PWCTR1 = const(0xC0)  # Power control 1
  PWCTR2 = const(0xC1)  # Power control 2
  PWCTRA = const(0xCB)  # Power control A
  PWCTRB = const(0xCF)  # Power control B
  VMCTR1 = const(0xC5)  # VCOM control 1
  VMCTR2 = const(0xC7)  # VCOM control 2
  RDID1 = const(0xDA)  # Read ID 1
  RDID2 = const(0xDB)  # Read ID 2
  RDID3 = const(0xDC)  # Read ID 3
  RDID4 = const(0xDD)  # Read ID 4
  GMCTRP1 = const(0xE0)  # Positive gamma correction
  GMCTRN1 = const(0xE1)  # Negative gamma correction
  DTCA = const(0xE8)  # Driver timing control A
  DTCB = const(0xEA)  # Driver timing control B
  POSC = const(0xED)  # Power on sequence control
  ENABLE3G = const(0xF2)  # Enable 3 gamma control
  PUMPRC = const(0xF7)  # Pump ratio control

  def __init__(self, spi, cs, dc, rst, width=240, height=320, rotation=0):
    self.spi = spi
    self.cs = cs
    self.dc = dc
    self.rst = rst
    self._init_width = width
    self._init_height = height
    self.width = width
    self.height = height
    self.rotation = rotation
    self.cs.init(self.cs.OUT, value=1)
    self.dc.init(self.dc.OUT, value=0)
    self.rst.init(self.rst.OUT, value=0)
    self.reset()
    self.init()
    self._scroll = 0
    self._buf = bytearray(_CHUNK * 2)
    self._colormap = bytearray(b'\x00\x00\xFF\xFF') #default white foregraound, black background
    self._x = 0
    self._y = 0
    self._font = fonts.glcdfont
    self.scrolling = False

  def init(self):
    for command, data in (
      (_RDDSDR, b"\x03\x80\x02"),
      (self.PWCTRB, b"\x00\xc1\x30"),
      (_PWRONCTRL, b"\x64\x03\x12\x81"),
      (_DTCTRLA, b"\x85\x00\x78"),
      (self.PWCTRA, b"\x39\x2c\x00\x34\x02"),
      (_PRCTRL, b"\x20"),
      (_DTCTRLB, b"\x00\x00"),
      (_PWCTRL1, b"\x23"),
      (_PWCTRL2, b"\x10"),
      (_VMCTRL1, b"\x3e\x28"),
      (_VMCTRL2, b"\x86")):
      self .write_cmd(command, data)

    if self.rotation == 0:          # 0 deg
      self .write_cmd(self.MADCTL, b"\x48")
      self.width = self._init_height
      self.height = self._init_width
    elif self.rotation == 1:        # 90 deg
      self .write_cmd(self.MADCTL, b"\x28")
      self.width = self._init_width
      self.height = self._init_height
    elif self.rotation == 2:        # 180 deg
      self .write_cmd(self.MADCTL, b"\x88")
      self.width = self._init_height
      self.height = self._init_width
    elif self.rotation == 3:        # 270 deg
      self .write_cmd(self.MADCTL, b"\xE8")
      self.width = self._init_width
      self.height = self._init_height
    elif self.rotation == 4:        # Mirrored + 0 deg
      self .write_cmd(self.MADCTL, b"\xC8")
      self.width = self._init_height
      self.height = self._init_width
    elif self.rotation == 5:        # Mirrored + 90 deg
      self .write_cmd(self.MADCTL, b"\x68")
      self.width = self._init_width
      self.height = self._init_height
    elif self.rotation == 6:        # Mirrored + 180 deg
      self .write_cmd(self.MADCTL, b"\x08")
      self.width = self._init_height
      self.height = self._init_width
    elif self.rotation == 7:        # Mirrored + 270 deg
      self .write_cmd(self.MADCTL, b"\xA8")
      self.width = self._init_width
      self.height = self._init_height
    else:
      self .write_cmd(self.MADCTL, b"\x08")

    for command, data in (
      (self.PIXFMT, b"\x55"),
      (_FRMCTR1, b"\x00\x18"),
      (_DISCTRL, b"\x08\x82\x27"),
      (_ENA3G, b"\x00"),
      (self.GAMMASET, b"\x01"),
      (_PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
      (_NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
      self .write_cmd(command, data)
    self .write_cmd(self.SLPOUT)
    time.sleep_ms(120)
    self .write_cmd(self.DISPLAY_ON)

########################################################################################################
###################################        Lowlevel functions        ###################################
########################################################################################################

  def write_cmd(self, command, data=None):
    self.dc(0)
    self.cs(0)
    self.spi.write(bytearray([command]))
    self.cs(1)
    if data is not None:
      self.write_data(data)

  def write_cmd_args(self, command, *args):
    """Write command to OLED (MicroPython).

    Args:
      command (byte): ILI9341 command code.
      *args (optional bytes): Data to transmit.
    """
    self.dc(0)
    self.cs(0)
    self.spi.write(bytearray([command]))
    self.cs(1)
    # Handle any passed data
    if len(args) > 0:
      self.write_data(bytearray(args))

  def write_data(self, data):
    self.dc(1)
    self.cs(0)
    self.spi.write(data)
    self.cs(1)

  def _writeblock(self, x0, y0, x1, y1, data=None):
    self.write_cmd(self.SET_COLUMN, ustruct.pack(">HH", x0, x1))
    self.write_cmd(self.SET_PAGE, ustruct.pack(">HH", y0, y1))
    self.write_cmd(self.WRITE_RAM, data)

  def _readblock(self, x0, y0, x1, y1):
    self .write_cmd(self.SET_COLUMN, ustruct.pack(">HH", x0, x1))
    self .write_cmd(self.SET_PAGE, ustruct.pack(">HH", y0, y1))
    #if data is None:
    return self._read(self.READ_RAM, (x1 - x0 + 1) * (y1 - y0 + 1) * 3)

  def _read(self, command, count):
    self.dc(0)
    self.cs(0)
    self.spi.write(bytearray([command]))
    data = self.spi.read(count)
    self.cs(1)
    return data

  def reset(self):
    self.rst(0)
    time.sleep_ms(50)
    self.rst(1)
    time.sleep_ms(50)



########################################################################################################
################################### FrameBuffer compatible functions ###################################
########################################################################################################

  def fill(self, c):
    self.clear(c)

  def pixel(self, x, y, color=None):
    if color is None:
      r, b, g = self._readblock(x, y, x, y)
      return color565(r, g, b)
    if not 0 <= x < self.width or not 0 <= y < self.height:
      return
    self._writeblock(x, y, x, y, ustruct.pack(">H", color))

  def hline(self, x, y, w, color):
    """Draw a horizontal line.

    Args:
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of line.
      color (int): RGB565 color value.
    """
    if x < 0 or y < 0 or (x + w - 1) > self.width:
      print("hline({}, {}) params out of screen".format(x, y))
      return

    line = color.to_bytes(2, 'big') * w
    self._writeblock(x, y, x + w - 1, y, line)

  def vline(self, x, y, h, color):
    """Draw a vertical line.

    Args:
      x (int): Starting X position.
      y (int): Starting Y position.
      h (int): Height of line.
      color (int): RGB565 color value.
    """
    # Confirm coordinates in boundary
    if x < 0 or y < 0 or (y + h - 1) > self.height:
      print("vline({}, {}) params out of screen".format(x, y))
      return
    line = color.to_bytes(2, 'big') * h
    self._writeblock(x, y, x, y + h - 1, line)

  def line(self, x1, y1, x2, y2, color):
    """Draw a line using Bresenham's algorithm.

    Args:
      x1, y1 (int): Starting coordinates of the line
      x2, y2 (int): Ending coordinates of the line
      color (int): RGB565 color value.
    """
    # Check for horizontal line
    if y1 == y2:
      if x1 > x2:
        x1, x2 = x2, x1
      self.hline(x1, y1, x2 - x1 + 1, color)
      return
    # Check for vertical line
    if x1 == x2:
      if y1 > y2:
        y1, y2 = y2, y1
      self.vline(x1, y1, y2 - y1 + 1, color)
      return
    # Confirm coordinates in boundary
    if self.is_off_grid(min(x1, x2), min(y1, y2),
              max(x1, x2), max(y1, y2)):
      return
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
    for x in range(x1, x2 + 1):
      # Had to reverse HW ????
      if not is_steep:
        self.pixel(x, y, color)
      else:
        self.pixel(y, x, color)
      error -= abs(dy)
      if error < 0:
        y += ystep
        error += dx

  def rect(self, x, y, w, h, color):
    """Draw a rectangle.

    Args:
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of rectangle.
      h (int): Height of rectangle.
      color (int): RGB565 color value.
    """
    x2 = x + w - 1
    y2 = y + h - 1
    self.hline(x, y, w, color)
    self.hline(x, y2, w, color)
    self.vline(x, y, h, color)
    self.vline(x2, y, h, color)

  def fill_rect(self, x, y, w, h, color=None):
    x = min(self.width - 1, max(0, x))
    y = min(self.height - 1, max(0, y))
    w = min(self.width - x, max(1, w))
    h = min(self.height - y, max(1, h))
    if color:
      color = ustruct.pack(">H", color)
    else:
      color = self._colormap[0:2] #background
    for i in range(_CHUNK):
      self._buf[2*i]=color[0]
      self._buf[2*i+1]=color[1]
    chunks, rest = divmod(w * h, _CHUNK)
    self._writeblock(x, y, x + w - 1, y + h - 1, None)
    if chunks:
      for count in range(chunks):
        self.write_data(self._buf)
    if rest != 0:
      mv = memoryview(self._buf)
      self.write_data(mv[:rest*2])

  def text(self, s, x, y, c=None):
    """
    Write text to the FrameBuffer using the the coordinates as the upper-left corner of the text. 
    The color of the text can be defined by the optional argument but is otherwise a default value of 1. 
    All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
    """
    pass

  def scroll(self, xstep, ystep):
    """
    Shift the contents of the FrameBuffer by the given vector. 
    This may leave a footprint of the previous colors in the FrameBuffer.
    """
    pass

  def blit(self, fbuf, x, y, key=None):
    """
    Draw another FrameBuffer on top of the current one at the given coordinates. If key is specified then it should be a color integer and the corresponding color will be considered transparent: all pixels with that color value will not be drawn.

    This method works between FrameBuffer instances utilising different formats, but the resulting colors may be unexpected due to the mismatch in color formats.
    """
    pass

############################################

  def set_color(self,fg,bg):
    self._colormap[0] = bg>>8
    self._colormap[1] = bg & 255
    self._colormap[2] = fg>>8
    self._colormap[3] = fg & 255

  def set_pos(self,x,y):
    self._x = x
    self._y = y

  def reset_scroll(self):
    self.scrolling = False
    self._scroll = 0
    self.scroll(0)

  def set_font(self, font):
    ret = self._font
    self._font = font
    return ret

  def clear(self, color=0):
    """Clear display.

    Args:
      color (Optional int): RGB565 color value (Default: 0 = Black).
    """
    w = self.width
    h = self.height
    # Clear display in 1024 byte blocks
    if color:
      line = color.to_bytes(2, 'big') * (w * 8)
    else:
      line = bytearray(w * 16)
    for y in range(0, h, 8):
      self._writeblock(0, y, w - 1, y + 7, line)

  def blit_buf(self, bitbuff, x, y, w, h):
    x = min(self.width - 1, max(0, x))
    y = min(self.height - 1, max(0, y))
    w = min(self.width - x, max(1, w))
    h = min(self.height - y, max(1, h))
    chunks, rest = divmod(w * h, _CHUNK)
    self._writeblock(x, y, x + w - 1, y + h - 1, None)
    written = 0
    for iy in range(h):
      for ix in range(w):
        index = ix+iy*w - written
        if index >=_CHUNK:
          self.write_data(self._buf)
          written += _CHUNK
          index   -= _CHUNK
        c = bitbuff.pixel(ix,iy)
        self._buf[index*2] = self._colormap[c*2]
        self._buf[index*2+1] = self._colormap[c*2+1]
    rest = w*h - written
    if rest != 0:
      mv = memoryview(self._buf)
      self.write_data(mv[:rest*2])

  def chars(self, str, x, y):
    str_w = self._font.get_width(str)
    div, rem = divmod(self._font.height(),8)
    nbytes = div+1 if rem else div
    buf = bytearray(str_w * nbytes)
    pos = 0
    for ch in str:
      glyph, char_w = self._font.get_ch(ch)
      for row in range(nbytes):
        index = row*str_w + pos
        for i in range(char_w):
          buf[index+i] = glyph[nbytes*i+row]
      pos += char_w
    fb = framebuf.FrameBuffer(buf,str_w, self._font.height(), framebuf.MONO_VLSB)
    self.blit_buf(fb, x, y, str_w, self._font.height())
    return x+str_w

  def scroll(self, dy):
    self._scroll = (self._scroll + dy) % self.height
    self .write_cmd(self.VSCRSADD, ustruct.pack(">H", self._scroll))

  def next_line(self, cury, char_h):
    global scrolling
    if not self.scrolling:
      res = cury + char_h
      self.scrolling = (res >= self.height)
    if self.scrolling:
      self.scroll(char_h)
      res = (self.height - char_h + self._scroll)%self.height
      self.fill_rect(0, res, self.width, self._font.height())
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
        if curx + width + char_w >= self.width:
          self.chars(text[written:pos], curx,cury)
          curx = 0 ; written = pos; width = char_h
          cury = self.next_line(cury,char_h)
        else:
          width += char_w
    if written<len(text):
      curx = self.chars(text[written:], curx,cury)
    self._x = curx; self._y = cury

  def print(self, text): #does word wrap, leaves self._x unchanged
    cury = self._y; curx = self._x
    char_h = self._font.height()
    char_w = self._font.max_width()
    lines = text.split('\n')
    for line in lines:
      words = line.split(' ')
      for word in words:
        if curx + self._font.get_width(word) >= self.width:
          curx = self._x; cury = self.next_line(cury,char_h)
          while self._font.get_width(word) > self.width:
            self.chars(word[:self.width//char_w],curx,cury)
            word = word[self.width//char_w:]
            cury = self.next_line(cury,char_h)
        if len(word)>0:
          curx = self.chars(word + ' ', curx, cury)
      curx = self._x; cury = self.next_line(cury, char_h)
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
    return self.width, self.height 

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
    if xmax >= self.width:
      print('x-coordinate: {0} above maximum of {1}.'.format(
        xmax, self.width - 1))
      return True
    if ymax >= self.height:
      print('y-coordinate: {0} above maximum of {1}.'.format(
        ymax, self.height - 1))
      return True
    return False

  def set_scroll_window(self, top, bottom):
    """Set the height of the top and bottom scroll margins.

    Args:
      top (int): Height of top scroll margin
      bottom (int): Height of bottom scroll margin
    """
    if top + bottom <= self.height:
      middle = self.height - (top + bottom)
      self.write_cmd_args(self.VSCRDEF,
               top >> 8,
               top & 0xFF,
               middle >> 8,
               middle & 0xFF,
               bottom >> 8,
               bottom & 0xFF)

  def scroll_window(self, y):
    """Scroll display vertically.

    Args:
      y (int): Number of pixels to scroll display.
    """
    self.write_cmd_args(self.VSCRSADD, y >> 8, y & 0xFF)


##################

  def fill_vrect(self, x, y, w, h, color):
    """Draw a filled rectangle (optimized for vertical drawing).

    Args:
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of rectangle.
      h (int): Height of rectangle.
      color (int): RGB565 color value.
    """
    if self.is_off_grid(x, y, x + w - 1, y + h - 1):
      return
    chunk_width = 1024 // h
    chunk_count, remainder = divmod(w, chunk_width)
    chunk_size = chunk_width * h
    chunk_x = x
    if chunk_count:
      buf = color.to_bytes(2, 'big') * chunk_size
      for c in range(0, chunk_count):
        self._writeblock(chunk_x, y,
               chunk_x + chunk_width - 1, y + h - 1,
               buf)
        chunk_x += chunk_width

    if remainder:
      buf = color.to_bytes(2, 'big') * remainder * h
      self._writeblock(chunk_x, y,
             chunk_x + remainder - 1, y + h - 1,
             buf)

  def fill_hrect(self, x, y, w, h, color):
    """Draw a filled rectangle (optimized for horizontal drawing).

    Args:
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of rectangle.
      h (int): Height of rectangle.
      color (int): RGB565 color value.
    """
    if self.is_off_grid(x, y, x + w - 1, y + h - 1):
      return
    chunk_height = 1024 // w
    chunk_count, remainder = divmod(h, chunk_height)
    chunk_size = chunk_height * w
    chunk_y = y
    if chunk_count:
      buf = color.to_bytes(2, 'big') * chunk_size
      for c in range(0, chunk_count):
        self._writeblock(x, chunk_y,
               x + w - 1, chunk_y + chunk_height - 1,
               buf)
        chunk_y += chunk_height

    if remainder:
      buf = color.to_bytes(2, 'big') * remainder * w
      self._writeblock(x, chunk_y,
             x + w - 1, chunk_y + remainder - 1,
             buf)

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
    self.pixel(x0, y0 + r, color)
    self.pixel(x0, y0 - r, color)
    self.pixel(x0 + r, y0, color)
    self.pixel(x0 - r, y0, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      self.pixel(x0 + x, y0 + y, color)
      self.pixel(x0 - x, y0 + y, color)
      self.pixel(x0 + x, y0 - y, color)
      self.pixel(x0 - x, y0 - y, color)
      self.pixel(x0 + y, y0 + x, color)
      self.pixel(x0 - y, y0 + x, color)
      self.pixel(x0 + y, y0 - x, color)
      self.pixel(x0 - y, y0 - x, color)

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
    self.vline(x0, y0 - r, 2 * r + 1, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      self.vline(x0 + x, y0 - y, 2 * y + 1, color)
      self.vline(x0 - x, y0 - y, 2 * y + 1, color)
      self.vline(x0 - y, y0 - x, 2 * x + 1, color)
      self.vline(x0 + y, y0 - x, 2 * x + 1, color)

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
    self.line(x0, y0 - y, x0, y0 + y, color)
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
      self.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
      self.line(x0 - x, y0 - y, x0 - x, y0 + y, color)
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
      self.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
      self.line(x0 - x, y0 - y, x0 - x, y0 + y, color)

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
    self.pixel(x0 + x, y0 + y, color)
    self.pixel(x0 - x, y0 + y, color)
    self.pixel(x0 + x, y0 - y, color)
    self.pixel(x0 - x, y0 - y, color)
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
      self.pixel(x0 + x, y0 + y, color)
      self.pixel(x0 - x, y0 + y, color)
      self.pixel(x0 + x, y0 - y, color)
      self.pixel(x0 - x, y0 - y, color)
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
      self.pixel(x0 + x, y0 + y, color)
      self.pixel(x0 - x, y0 + y, color)
      self.pixel(x0 + x, y0 - y, color)
      self.pixel(x0 - x, y0 - y, color)

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

    self.hline(x0 + r, y0    , 2 + w - 2 * r, color)
    self.hline(x0 + r, y0 + h - 1, 2 + w - 2 * r, color)
    self.vline(x0    , y0 + r, 2 + h - 2 * r, color)
    self.vline(x0 + w - 1, y0 + r, 2 + h - 2 * r, color)

    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx

      # Top-Left
      self.pixel(x0 - x + r, y0 - y + r, color)
      self.pixel(x0 - y + r, y0 - x + r, color)

      # Top-Right
      self.pixel(x0 + w + x - r - 1, y0 - y + r, color)
      self.pixel(x0 + w + y - r - 1, y0 - x + r, color)

      # Bottom-Left
      self.pixel(x0 - x + r, y0 + h + y - r - 1, color)
      self.pixel(x0 - y + r, y0 + h + x - r - 1, color)

      # Bottom-Right
      self.pixel(x0 + w + x - r - 1, y0 + h + y - r - 1, color)
      self.pixel(x0 + w + y - r - 1, y0 + h + x - r - 1, color)

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

    self.fill_rect(x0 + r, y0, w2, h, color)
    while x < y:
      if f >= 0:
        y -= 1
        dy += 2
        f += dy
      x += 1
      dx += 2
      f += dx
      
      # Left
      self.vline(x0 - x + r, y0 - y + r, h2 + 2 * y, color)
      self.vline(x0 - y + r, y0 - x + r, h2 + 2 * x, color)

      #right 1
      self.vline(x0 + w + x - r - 1, y0 - y + r, h2 + 2 * y, color)
      #right 2
      self.vline(x0 + w + y - r - 1, y0 - x + r, h2 + 2 * x, color)

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
      self.hline(x[0], y, x[1] - x[0] + 2, color)

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
    self.draw_lines(coords, color=color)

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
      self.line(x1, y1, x2, y2, color)
      x1, y1 = x2, y2

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
      return f.read(buf_size)

  def draw_sprite(self, buf, x, y, w, h):
    """Draw a sprite (optimized for horizontal drawing).

    Args:
      buf (bytearray): Buffer to draw.
      x (int): Starting X position.
      y (int): Starting Y position.
      w (int): Width of drawing.
      h (int): Height of drawing.
    """
    x2 = x + w - 1
    y2 = y + h - 1
    if self.is_off_grid(x, y, x2, y2):
      return
    self._writeblock(x, y, x2, y2, buf)

  def draw_image(self, path, x=0, y=0, w=320, h=240):
    """Draw image from flash.

    Args:
      path (string): Image file path.
      x (int): X coordinate of image left.  Default is 0.
      y (int): Y coordinate of image top.  Default is 0.
      w (int): Width of image.  Default is 320.
      h (int): Height of image.  Default is 240.
    """
    x2 = x + w - 1
    y2 = y + h - 1
    if self.is_off_grid(x, y, x2, y2):
      return
    with open(path, "rb") as f:
      chunk_height = 1024 // w
      chunk_count, remainder = divmod(h, chunk_height)
      chunk_size = chunk_height * w * 2
      chunk_y = y
      if chunk_count:
        for c in range(0, chunk_count):
          buf = f.read(chunk_size)
          self._writeblock(x, chunk_y,
                 x2, chunk_y + chunk_height - 1,
                 buf)
          chunk_y += chunk_height
      if remainder:
        buf = f.read(remainder * w * 2)
        self._writeblock(x, chunk_y,
               x2, chunk_y + remainder - 1,
               buf)






######################

  # def fill_rect(self, x, y, w, h, color):
  #   """Draw a filled rectangle.

  #   Args:
  #     x (int): Starting X position.
  #     y (int): Starting Y position.
  #     w (int): Width of rectangle.
  #     h (int): Height of rectangle.
  #     color (int): RGB565 color value.
  #   """
  #   if self.is_off_grid(x, y, x + w - 1, y + h - 1):
  #     return
  #   if w > h:
  #     self.fill_hrect(x, y, w, h, color)
  #   else:
  #     self.fill_vrect(x, y, w, h, color)
