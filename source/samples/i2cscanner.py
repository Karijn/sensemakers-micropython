"""
i2c scanner functions
"""

# Adapted for Sensemakers. Changed pins for the TTGO T$-V1.3 board
import time
from lib.display.DISPLAY import getdisplay, color565
from machine import Pin, I2C
import lib.fonts.tt24
import lib.fonts.roboto_cond_reg_12
import lib.fonts.roboto_cond_reg_18


def i2c_scan_once(i2c, twodigit=True):
    """
    scan once for i2c addresses
    """
    address_string = ""
    addresses = i2c.scan()

    for addr in addresses:
        hex_address = str(hex(addr))
        if twodigit and len(hex_address) == 3:
            hex_address = hex_address[:2] + "0" + hex_address[2:]
        address_string = address_string  + hex_address + " "

    return address_string

def i2cscanstring(twodigit=True):
    """
    does one i2c scan and returns a string with addresses
    """
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

    return i2c_scan_once(i2c, twodigit)

def i2cscan(twodigit=True):
    """
    does one i2c scan
    """
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

    display = getdisplay()
    col = color565(255, 0, 0)
    display.set_pos(0, 0)
    display.set_color(col, 0)
    display.set_font(lib.fonts.tt24)

    display.print("I2C Tester")
    display.print(i2c_scan_once(i2c, twodigit))


def i2ctester(twodigit=True):
    """
    continues scan for i2c addresses
    """
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

    display = getdisplay()
    display.clear(0)
    last_len = 0

    col = color565(255, 0, 0)

    while True:
        if col == color565(255, 0, 0):
            col = color565(0, 255, 0)
        else:
            col = color565(255, 0, 0)

        display.set_pos(0, 0)
        display.set_color(col, 0)

        addresses = i2c_scan_once(i2c, twodigit)

        if last_len < len(addresses):
            display.clear()

        last_len = len(addresses)
        display.set_font(lib.fonts.roboto_cond_reg_18)
        display.print("I2C Tester")
        display.set_font(lib.fonts.roboto_cond_reg_12)
        display.print(addresses)

        time.sleep_ms(1000)

i2ctester()
