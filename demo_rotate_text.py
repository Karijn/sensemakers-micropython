from display import create_display
import fonts.opensans_16
from time import sleep

text = 'Hoi Piepeloi!'

for rot in range(8):
  display = create_display(rotation=rot)

  display.set_font(fonts.opensans_16)
  display.set_pos(40, 20)
  display.print(text)
  sleep(2)


display = create_display()

display.set_font(fonts.opensans_16)
display.set_pos(40, 20)
display.print('Ready!')
