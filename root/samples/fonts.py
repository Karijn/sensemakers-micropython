from lib.display.DISPLAY import *

import lib.fonts.freesans_36
import lib.fonts.free_sans_oblique_20
import lib.fonts.opensans_12
import lib.fonts.free_sans_bold_24
import lib.fonts.free_sans_bold_20

def test():
  #display = getbuffereddisplay(2)
  display = getdisplay(2)
  display.fill(0)

  text = 'Hoi Piepeloi !'

  display.set_font(lib.fonts.freesans_36)
  len, hi = display.get_stringsize(text)
  display.fill_rect(10, 10, len, 3, color565(255, 0, 0))
  display.fill_rect(10, 13, len, 3, color565(181, 63, 0))
  display.fill_rect(10, 16, len, 3, color565(127, 127, 0))
  display.fill_rect(10, 19, len, 3, color565(63, 181, 0))
  display.fill_rect(10, 22, len, 3, color565(0, 255, 0))
  display.fill_rect(10, 25, len, 3, color565(0, 181, 63))
  display.fill_rect(10, 28, len, 3, color565(0, 127, 127))
  display.fill_rect(10, 31, len, 3, color565(0, 63, 181))
  display.fill_rect(10, 34, len, 3, color565(0, 0, 255))
  display.fill_rect(10, 37, len, 3, color565(63, 0, 181))
  display.fill_rect(10, 40, len, 3, color565(127, 0, 127))
  display.set_color(None, color565(0, 0, 0))
  display.chars(text, 10, 10)

  display.set_font(lib.fonts.free_sans_bold_20)
  display.set_color(color565(0, 255, 0), color565(0, 0, 255))
  display.chars(text, 10, 60)
  
  display.set_font(lib.fonts.opensans_12)
  display.set_color(color565(0, 0, 255), color565(255, 0, 0))
  display.chars(text, 10, 110)
  
  display.set_font(lib.fonts.free_sans_bold_24)
  display.set_color(color565(0, 0, 255), color565(0, 255, 0))
  display.chars(text, 10, 160)

  # sprite = display.load_sprite('images/Python41x49.raw', 41, 49)
  # display.draw_sprite(sprite, 20, 200, 41, 49)
  # display.draw_sprite(buf, 0, 0, 240, 320)
  #sprites = [sprite]
  # for i in range(1, 45):
  #   print ('load sprite {:02d}'.format(i))
  #   sbuf = bytearray(getdisplay().load_sprite( 'animation/anim{:02d}.raw'.format(i), 135, 135))
  #   sprit = framebuf.FrameBuffer(sbuf, 135, 135, framebuf.RGB565)
  #   sprites.append(sprit)
  # while True:

  # for sprite in sprites:
  #   fbuf.fill(color565(0, 0, 0))
  #   #fbuf.blit(sprit, 20, 20, 0)
  #   fbuf.draw_sprite(sprite, 20, 20, 41, 49)
  #   display.draw_sprite(buf, 0, 0, 240, 320)
  display.show()


test()
