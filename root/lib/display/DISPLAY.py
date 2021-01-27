from machine import Pin, SPI
from lib.display.xpt2046 import *
from lib.display.ili934xnew import ILI9341, color565

_rotation = 0
_speed = 0
_spi = None
_display = None
_touch = None
SLOW_SPI = const(1)
FAST_SPI = const(2)


def color(r, g, b):
  return color565(r, g, b)

def gettouch():
    global _touch
    global _spi
    global _speed
    global _rotation
    if _spi is None or _speed != SLOW_SPI:
        _spi = getspi(SLOW_SPI)
    if _touch is None :
        _touch = TOUCH(spi=_spi)
    else:
        _touch.spi = _spi
    _touch.set_rotation(_rotation)
    return _touch

def getdisplay(rotation=None):
    global _spi
    global _display
    global _speed   
    global _rotation
    if _spi is None or _speed != FAST_SPI:
        _spi = getspi(FAST_SPI)

    if _display is None or rotation is not None:
        if rotation is not None:
            _rotation = rotation
        _display = ILI9341(_spi, cs=Pin(26), dc=Pin(5), rst=Pin(33), width=320, height=240, rotation=_rotation)
    else:
        _display.spi = _spi
    return _display

def getspi(speed = FAST_SPI):
    global _spi
    global _speed
    if _spi is None or _speed != speed:
        if speed == SLOW_SPI:
            #print("SWITCH SPI to SLOW")
            #_spi = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
            _spi = SPI(2, baudrate=2000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        if speed == FAST_SPI:
            #print("SWITCH SPI to FAST")
            _spi = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        _speed = speed
    return _spi
    