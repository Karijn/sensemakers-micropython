# test of printing multiple fonts to the ILI9341 on an M5Stack using H/W SP
# MIT License; Copyright (c) 2017 Jeffrey N. Magee
# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board
from lib.display.DISPLAY import color565, getdisplay
from machine import Pin, PWM
import lib.fonts.glcdfont
import lib.fonts.tt14
import lib.fonts.tt24
import lib.fonts.tt32
from time import sleep_ms

# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board

display = getdisplay()

fonts = [lib.fonts.glcdfont, lib.fonts.tt14, lib.fonts.tt24, lib.fonts.tt32]
colors = [color565(255,0,0), color565(0,255,0),color565(0,0,255),color565(150,150,0)]

text = 'Now is the time for all Sensemakers to come to the aid of the party.'

display.clear()
display.set_pos(0, 0)

bg_led = PWM(Pin(4))
bg_led.freq(1000)
bg_led.duty(750)

for ff, col in zip(fonts, colors):
    display.set_color(col, 0)
    display.set_font(ff)
    display.print(text)

while True:
    for lum in range(50):
        bg_led.duty(lum*20)
        sleep_ms(25)
    for lum in reversed(range(50)):
        bg_led.duty(lum*20)
        sleep_ms(25)
