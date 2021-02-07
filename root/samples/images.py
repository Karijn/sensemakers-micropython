"""ILI9341 demo (images)."""
from time import sleep
from lib.display.DISPLAY import getdisplay, color565
from machine import Pin, SPI


def test():
    """Test code."""
    display = getdisplay()
    display.clear(0)

    display.draw_image('images/RaspberryPiWB128x128.raw', 0, 0, 128, 128)
    sleep(2)

    display.draw_image('images/MicroPython128x128.raw', 0, 129, 128, 128)
    sleep(2)

    display.draw_image('images/Tabby128x128.raw', 112, 0, 128, 128)
    sleep(2)

    display.draw_image('images/Tortie128x128.raw', 112, 129, 128, 128)

    sleep(9)

    display.clear(0)


test()
