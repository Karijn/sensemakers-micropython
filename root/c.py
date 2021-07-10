

from lib.display.DISPLAY import *
from lib.display.displayext import DisplayExt
from lib.debug.timings import timed_function

@timed_function
def create():
  display = getbuffereddisplay(2)
  return display

@timed_function
def clear(display):
  display.fill(12345)

@timed_function
def line(display):
    display.line(10, 10, 100, 100, color565(255, 0, 0))

@timed_function
def show(display):
  display.show()

def test():
  display = create()
  clear(display)
  line(display)
  show(display)

  display = create()
  clear(display)
  line(display)
  show(display)


test()

