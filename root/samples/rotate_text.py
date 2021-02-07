#from display import create_display
import lib.fonts.opensans_16
from lib.display.DISPLAY import *
from time import sleep

text = 'Hoi Piepeloi!'

for rot in range(8):
  print('rotation = ', rot)
  display = getdisplay(rotation=rot)
  display.erase()
  display.set_font(lib.fonts.opensans_16)
  display.set_pos(40, 20)
  display.print(text)
  sleep(2)


display = getdisplay(0)

display.erase()
display.set_font(lib.fonts.opensans_16)
display.set_pos(40, 20)
display.print('Ready!')
