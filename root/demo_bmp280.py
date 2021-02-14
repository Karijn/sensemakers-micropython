# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board
from lib.display.DISPLAY import color565, getdisplay
from machine import Pin, I2C
import fonts.roboto_cond_reg_16
from sensors.bmp280 import BMP280

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
bmp = BMP280(i2c)

display = getdisplay()

display.set_font(fonts.roboto_cond_reg_16)
display.set_color(color565(255, 255, 0), color565(0, 0, 127))
display.clear()
display.set_pos(0, 0)
display.print("env: bmp280")

display.print("temperature:" + str(bmp.temperature) + "C")
display.print("pressure:   " + str(bmp.pressure))
