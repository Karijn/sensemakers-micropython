"""
display routines
"""
# test of printing multiple fonts to the ILI9341 on an M5Stack using H/W SP
# MIT License; Copyright (c) 2017 Jeffrey N. Magee
# Adapted for Sensemakers. Changed pins for the TTGO T4-V1.3 board

from ili934xnew import ILI9341
from machine import Pin, SPI, PWM

bg_led = None

def create_display(rotation=0):
    """
    Create a connection with the display
    """

    global bg_led
    bg_led = PWM(Pin(4))
    bg_led.freq(1000)
    bg_led.duty(750)

    spi = SPI(2, baudrate=30000000, miso=Pin(12), mosi=Pin(23), sck=Pin(18))
    display = ILI9341(spi, cs=Pin(27), dc=Pin(32), rst=Pin(5), w=320, h=240, r=rotation)

    display.erase()
    display.set_pos(0, 0)

    return display
