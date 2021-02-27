from machine import Pin, SPI
from lib.display.ili934xnew import ILI9341FB, ILI9341, ILI9341FB
from lib.display.displayext import *
from lib.display.displaybase import *

_oldrotation = -1
_rotation = 0
_speed = 0
_spi = None
_display = None
_touch = None
SLOW_SPI = const(1)
FAST_SPI = const(2)

_debugspi = False

def color565(r, g, b):
  return (r & 0xf8) << 8 | (g & 0xfc) << 3 | (b & 0xff) >> 3

def setdebugspi(enable):
  global _debugspi
  _debugspi = enable

def setrotation(rotation):
  global _rotation
  if rotation is not None:
    _rotation = rotation

def gettouch():
  global _touch
  global _spi
  global _speed
  global _rotation

  if _spi is None or _speed != SLOW_SPI:
    _spi = getspi(SLOW_SPI)
  if _touch is None:
    print('get new TOUCH, rotation = ', _rotation)
    from lib.display.xpt2046 import TOUCH
    _touch = TOUCH(spi=_spi, rotation=_rotation)
  else:
    _touch.spi = _spi
  _touch.set_rotation(_rotation)
  return _touch

def getdisplay(rotation=None):
  global _spi
  global _display
  global _speed   
  global _rotation
  global _oldrotation
  if _spi is None or _speed != FAST_SPI:
    _spi = getspi(FAST_SPI)

  if rotation != None:
    _rotation=rotation

  if _display is None:
    print('get new display, rotation = ', _rotation)
    _display = ILI9341(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
  else:
    _display.spi = _spi
    if _rotation != _oldrotation:
      print('get new display, rotation = ', _rotation)
      _display = ILI9341(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
  _oldrotation = _rotation
  return _display

def getbuffereddisplay(rotation=None):
  global _spi
  global _display
  global _speed   
  global _rotation
  global _oldrotation
  if _spi is None or _speed != FAST_SPI:
    _spi = getspi(FAST_SPI)

  if rotation != None:
    _rotation=rotation

  if _display is None:
    print('get new display, rotation = ', _rotation)
    _display = ILI9341FBEx(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
  else:
    if _rotation != _oldrotation:
      print('get new display, rotation = ', _rotation)

      _display = ILI9341FBEx(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=240, height=320, rotation=_rotation)
    else:
      _display.spi = _spi

  _oldrotation = _rotation
  return _display

class FbSprite(SwappedFrameBuffer, DispExt):

  def __init__(self, width=240, height=320):
    SwappedFrameBuffer.__init__(self, width=240, height=320)

  def fill(self, c):
    SwappedFrameBuffer.fill(self, c)

  def pixel(self, x, y, c):
    SwappedFrameBuffer.pixel(self, x, y, c)

  def hline(self, x, y, w, c):
    SwappedFrameBuffer.hline(self, x, y, w, c)

  def vline(self, x, y, h, c):
    SwappedFrameBuffer.vline(self, x, y, h, c)

  def line(self, x1, y1, x2, y2, c):
    SwappedFrameBuffer.line(self, x1, y1, x2, y2, c)

  def rect(self, x, y, w, h, c):
    SwappedFrameBuffer.rect(self, x, y, w, h, c)

  def fill_rect(self, x, y, w, h, c):
    SwappedFrameBuffer.fill_rect(self, x, y, w, h, c)

  def text(self, s, x, y, c = None):
    SwappedFrameBuffer.text(self, s, x, y, c)

  def scroll(self, xstep, ystep):
    SwappedFrameBuffer.scroll(self, xstep, ystep)

  def blit(self, fbuf, x, y, key = None):
    SwappedFrameBuffer.blit(self, fbuf, x, y, key)



class ILI9341FBEx(ILI9341FB, DispExt):

  def __init__(self, spi, cs, dc, rst, width=240, height=320, rotation=0):
    ILI9341FB.__init__(self, spi, cs, dc, rst, width, height, rotation)

  def fill(self, c):
    ILI9341FB.fill(self, c)

  def pixel(self, x, y, c):
    ILI9341FB.pixel(self, x, y, c)

  def hline(self, x, y, w, c):
    ILI9341FB.hline(self, x, y, w, c)

  def vline(self, x, y, h, c):
    ILI9341FB.vline(self, x, y, h, c)

  def line(self, x1, y1, x2, y2, c):
    ILI9341FB.line(self, x1, y1, x2, y2, c)

  def rect(self, x, y, w, h, c):
    ILI9341FB.rect(self, x, y, w, h, c)

  def fill_rect(self, x, y, w, h, c):
    ILI9341FB.fill_rect(self, x, y, w, h, c)

  def text(self, s, x, y, c = None):
    ILI9341FB.text(self, s, x, y, c)

  def scroll(self, xstep, ystep):
    ILI9341FB.scroll(self, xstep, ystep)

  def blit(self, fbuf, x, y, key = None):
    ILI9341FB.blit(self, fbuf, x, y, key)

  # def __init__(self, width=240, height=320):
  #   SwappedFrameBuffer.__init__(self, width, height)

# def getbuffereddisplay(rotation=None):
#   global _spi
#   global _display
#   global _speed   
#   global _rotation
#   global _oldrotation
#   if _spi is None or _speed != FAST_SPI:
#     _spi = getspi(FAST_SPI)

#   from lib.display.ili934xnew import ILI9341, ILI9341Buffered

#   if rotation != None:
#     _rotation=rotation

#   if _display is None:
#     print('get new display, rotation = ', _rotation)
#     _display = ILI9341Buffered(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
#   else:
#     _display.ILI9341Bufferedspi = _spi
#     if _rotation != _oldrotation:
#       print('get new display, rotation = ', _rotation)
#       _display = (_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
#   _oldrotation = _rotation
#   return _display

def getspi(speed = FAST_SPI):
  global _spi
  global _speed
  global _debugspi
  if _spi is None or _speed != speed:
    if speed == FAST_SPI:
      if _debugspi:
        print("SWITCH SPI to FAST")
      #_spi = SPI(2, baudrate=20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
      _spi = SPI(2, baudrate=15000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    else: # if speed == SLOW_SPI:
      if _debugspi:
        print("SWITCH SPI to SLOW")
      #_spi = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
      _spi = SPI(2, baudrate=2000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    _speed = speed
  return _spi
