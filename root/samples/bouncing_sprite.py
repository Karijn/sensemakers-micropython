from lib.display.DISPLAY import getdisplay
from machine import Pin, SPI
from utime import sleep_us, ticks_us, ticks_diff


class BouncingSprite(object):
  """Bouncing Sprite."""

  def __init__(self, path, w, h, screen_width, screen_height, speed, display):
    """Initialize sprite.

    Args:
      path (string): Path of sprite image.
      w, h (int): Width and height of image.
      screen_width (int): Width of screen.
      screen_height (int): Width of height.
      size (int): Square side length.
      speed(int): Initial XY-Speed of sprite.
      display (SSD1351): OLED display object.
      color (int): RGB565 color value.
    """
    self.buf = display.load_sprite(path, w, h)
    self.w = w
    self.h = h
    if screen_width == 0:
      self.screen_width = display.width
    else:
      self.screen_width = screen_width
    if screen_height == 0:
      self.screen_height = display.height
    else:
      self.screen_height = screen_height
    self.display = display
    self.x_speed = speed
    self.y_speed = speed
    self.x = self.screen_width // 2
    self.y = self.screen_height // 2
    self.prev_x = self.x
    self.prev_y = self.y

  def update_pos(self):
    """Update sprite speed and position."""
    x = self.x
    y = self.y
    w = self.w
    h = self.h
    x_speed = abs(self.x_speed)
    y_speed = abs(self.y_speed)

    if x + w + x_speed >= self.screen_width:
      self.x_speed = -x_speed
    elif x - x_speed < 0:
      self.x_speed = x_speed

    if y + h + y_speed >= self.screen_height:
      self.y_speed = -y_speed
    elif y - y_speed <= 0:
      self.y_speed = y_speed

    self.prev_x = x
    self.prev_y = y

    self.x = x + self.x_speed
    self.y = y + self.y_speed

  def draw(self):
    """Draw sprite."""
    x = self.x
    y = self.y
    prev_x = self.prev_x
    prev_y = self.prev_y
    w = self.w
    h = self.h
    x_speed = abs(self.x_speed)
    y_speed = abs(self.y_speed)

    # Determine direction and remove previous portion of sprite
    if prev_x > x:
      # Left
      self.display.fill_vrect(x + w, prev_y, x_speed, h, 0)
    elif prev_x < x:
      # Right
      self.display.fill_vrect(x - x_speed, prev_y, x_speed, h, 0)
    if prev_y > y:
      # Upward
      self.display.fill_vrect(prev_x, y + h, w, y_speed, 0)
    elif prev_y < y:
      # Downward
      self.display.fill_vrect(prev_x, y - y_speed, w, y_speed, 0)

    self.display.draw_sprite(self.buf, x, y, w, h)


def test():
  """Bouncing sprite."""
  try:
    display = getdisplay(2)
    display.clear(0)
    
    # Load sprite
    logo = BouncingSprite('images/Python41x49.raw',
                41, 49, 0, 0, 3, display)

    while True:
      timer = ticks_us()
      logo.update_pos()
      logo.draw()
      # Attempt to set framerate to 30 FPS
      timer_dif = 33333 - ticks_diff(ticks_us(), timer)
      if timer_dif > 0:
        sleep_us(timer_dif)

  except KeyboardInterrupt:
    display.cleanup()


test()