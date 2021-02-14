"""ILI9341 demo (Scrolling Marquee)."""
from lib.display.DISPLAY import getdisplay, color565
from time import sleep
from sys import implementation


def test():
  """Scrolling Marquee."""
  try:
    display = getdisplay()
    display.clear(0)

    # Draw non-moving circles
    display.fill_rect(0, 0, 239, 99, color565(27, 72, 156))
    display.fill_rect(0, 168, 239, 151, color565(220, 27, 72))

    # Load Marquee image
    display.draw_image('images/Rototron128x26.raw', 56, 120, 128, 26)

    # Set up scrolling
    display.set_scroll_window(top=152, bottom=100)

    spectrum = list(range(152, 221)) + list(reversed(range(152, 220)))
    while True:
      for y in spectrum:
        display.scroll_window(y)
        sleep(.1)

  except KeyboardInterrupt:
    display.cleanup()


test()
