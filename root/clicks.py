from time import ticks_ms, ticks_diff
from lib.display.xpt2046 import *
from lib.display.DISPLAY import *



class CLICKS:
  def __init__(self, click=None, 
              button_down=None, button_up=None, button_repeat=None, 
              repeat_timeout=250):
    self._last = None
    self._time_down      = 0
    self._click          = click
    self._button_down    = button_down
    self._button_up      = button_up
    self._button_repeat  = button_repeat
    self._repeat_timeout = repeat_timeout
    self._repeat_count   = 0

  def update(self):
    t = gettouch().get_touch(initial=False, wait=False)
    ms = ticks_ms()

    if t is None and self._last is not None and self._button_up is not None:
      self._button_up(self._last, self._repeat_count)

    if t is not None and self._last is None:
      self._time_down = ms
      self._repeat_count = 0
      if self._button_down is not None:
        self._button_down(t)
    
    if t is not None and self._last is not None and self._button_repeat is not None and ticks_diff(ms, self._time_down) > self._repeat_timeout:
      self._time_down = ms
      self._repeat_count += 1
      self._button_repeat(t, self._repeat_count)

    self._last = t


def test():
  def button_up(pos, cnt):
    print('button up at ', end='')
    print(cnt, end='')
    print(' times at ', end='')
    print(pos)

  def button_down(pos):
    print('button down at ', end='')
    print(pos)
    
  def button_repeat(pos, cnt):
    print('button repeat ', end='')
    print(cnt, end='')
    print(' times at ', end='')
    print(pos)
  c = CLICKS( button_down=button_down, button_up = button_up, button_repeat=button_repeat)
  while True:
    c.update()
