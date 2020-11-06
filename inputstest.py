


#    spi = SPI(2, baudrate=30000000, miso=Pin(12), mosi=Pin(23), sck=Pin(18))
#    display = ILI9341(spi, cs=Pin(27), dc=Pin(32), rst=Pin(5), w=320, h=240, r=rotation)
#    4 display led
# 0-19, 21-23, 25-27, 32-39



"""
input functions
"""

# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board
import time
from ili934xnew import color565
from machine import Pin
import fonts.tt24
import fonts.roboto_cond_reg_12
import fonts.roboto_cond_reg_18
from display import create_display

def read_input(input):
  pin = Pin(input, Pin.IN, Pin.PULL_UP)
  return pin.value()

def read_inputs(inputs):
  r = {}
  for p in inputs:
    r[p] = read_input(p)

  return r

def test():
    """
    continues scan for inputs
    """

    display = create_display()
    last_len = 0

    display.set_font(fonts.roboto_cond_reg_18)
    
    col = color565(255, 0, 0)

    inputpins = ( 21, 22, 25, 26, 33, 34, 35, 36, 37, 38, 39)

    oldvals = read_inputs(inputpins)

    while True:
      if col == color565(255, 0, 0):
          col = color565(0, 255, 0)
      else:
          col = color565(255, 0, 0)

      display.set_pos(0, 0)
      display.set_color(col, 0)

      newvals = read_inputs(inputpins)

      for p in inputpins:
        s = str(p) + " " + str(oldvals[p]) + "  " + str(newvals[p]) + ( "  " if oldvals[p] == newvals[p] else "*") + "\n"
        display.write(s)
#        if last_len < len(addresses):
#            display.erase()

      oldvals = newvals
      time.sleep_ms(500)

if __name__ == "__main__":
    inputtester()
