from machine import Pin, SPI
from lib.display.xpt2046 import TOUCH
from lib.display.ili934xnew import ILI9341

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
