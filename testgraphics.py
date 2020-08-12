"""
test graphics functions
"""

# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board
from display import create_display
from ili934xnew import color565

"""
from time import sleep
from display import create_display
from ili934xnew import color565
display = create_display()

display.write('peekaboe!')

display.draw_circle(20, 20, 20, color565(255, 0, 0))
display.draw_circle(30, 30, 20, color565(0, 255, 0))
display.draw_ellipse(40, 40, 40, 10, color565(0, 0, 255))
display.draw_hline(100, 100, 100, color565(255, 255, 0))
display.draw_vline(100, 100, 100, color565(255, 255, 0))
display.draw_line(10, 10, 100, 100, color565(255, 255, 0))
display.draw_line(100, 10, 10, 100, color565(255, 255, 0))

coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
display.draw_lines(coords, color565(0, 255, 255))

display.draw_polygon(3, 120, 100, 30, color565(0, 64, 255), rotate=15)
display.draw_polygon(3, 120, 100, 45, color565(0, 64, 255), rotate=15)
display.fill_polygon(7, 150, 150, 50, color565(0, 64, 255), rotate=15)

display.fill_circle(130, 130, 20, color565(0, 255, 0))
display.fill_ellipse(140, 140, 40, 10, color565(0, 0, 255))

sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
display.draw_sprite(sprite, 100, 100, 41, 49)

display.fill_rectangle(0, 0, 239, 99, color565(27, 72, 156))
display.fill_rectangle(0, 168, 239, 151, color565(220, 27, 72))
display.draw_image('images/Rototron128x26.raw', 56, 120, 128, 26)
display.set_scroll_window(top=152, bottom=100)

spectrum = list(range(152, 221)) + list(reversed(range(152, 220)))
while True:
for y in spectrum:
display.scroll_window(y)
sleep(.1)

"""

def test():
  from time import sleep
  from display import create_display
  from ili934xnew import color565
  display = create_display()

  display.write('peekaboe!')

  display.draw_circle(20, 20, 20, color565(255, 0, 0))
  display.draw_circle(30, 30, 20, color565(0, 255, 0))
  display.draw_ellipse(40, 40, 40, 10, color565(0, 0, 255))
  display.draw_hline(100, 100, 100, color565(255, 255, 0))
  display.draw_vline(100, 100, 100, color565(255, 255, 0))
  display.draw_line(10, 10, 100, 100, color565(255, 255, 0))
  display.draw_line(100, 10, 10, 100, color565(255, 255, 0))

  sleep(1)
  display = create_display()

  coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
  display.draw_lines(coords, color565(0, 255, 255))

  sleep(1)
  display = create_display()

  display.draw_polygon(3, 120, 100, 30, color565(0, 64, 255), rotate=15)
  display.draw_polygon(3, 120, 100, 45, color565(0, 64, 255), rotate=15)
  display.fill_polygon(7, 150, 150, 50, color565(0, 64, 255), rotate=15)

  sleep(1)
  display = create_display()

  display.fill_circle(130, 130, 20, color565(0, 255, 0))
  display.fill_ellipse(140, 140, 40, 10, color565(0, 0, 255))

  sleep(1)
  display = create_display()

  sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
  display.draw_sprite(sprite, 100, 100, 41, 49)

  sleep(1)
  display = create_display()

  display.fill_rectangle(0, 0, 239, 99, color565(27, 72, 156))
  display.fill_rectangle(0, 168, 239, 151, color565(220, 27, 72))
  display.draw_image('images/Rototron128x26.raw', 56, 120, 128, 26)
  display.set_scroll_window(top=152, bottom=100)

  spectrum = list(range(152, 221)) + list(reversed(range(152, 220)))
  for y in spectrum:
    display.scroll_window(y)
    sleep(.1)

  sleep(1)
  display = create_display()


test()