import lvgl as lv
#import lvesp32
from ili9XXX import ili9341, LANDSCAPE, PORTRAIT
from xpt2046 import xpt2046

MADCTL_MY = const(0x80)
MADCTL_MX = const(0x40)
MADCTL_ML = const(0x10)
MADCTL_MH = const(0x04)


display = None
touch = None

def getdisplay():
    global display
    global touch
    return getdisplay_landscape()

def getdisplay_landscape():
    global display
    global touch
    # Import ILI9341 driver and initialized it
    #display = ili9341(miso=19, mosi=23, clk=18, cs=26, dc=5, rst=33, power=-1, backlight=-1, mhz=40, factor=4, hybrid=False, rot=LANDSCAPE)
    display = ili9341(miso=19, mosi=23, clk=18, cs=26, dc=5, rst=33, power=-1, backlight=-1, mhz=40, factor=4, hybrid=True, width=320, height=240, rot=LANDSCAPE)

    # Import XPT2046 driver and initalize it
    #touch = xpt2046(cs=27, transpose=False, cal_x0=258, cal_y0=420, cal_x1=3884, cal_y1=3945)
    touch = xpt2046(cs=27, transpose=False, cal_x0=3865, cal_y0=329, cal_x1=399, cal_y1=3870)
    print("Display in landscape mode")

def getdisplay_portrait():
    global display
    global touch
    if display is not None:
        return display
    # Import ILI9341 driver and initialized it
    #display = ili9341(miso=19, mosi=23, clk=18, cs=26, dc=5, rst=33, power=-1, backlight=-1, mhz=40, factor=4, hybrid=True, rot=MADCTL_MY)
    display = ili9341(miso=19, mosi=23, clk=18, cs=26, dc=5, rst=33, power=-1, backlight=-1, mhz=40, factor=4, hybrid=False, rot=MADCTL_MY)

    # Import XPT2046 driver and initalize it
    touch = xpt2046(cs=27, transpose=True, cal_x0=258, cal_y0=420, cal_x1=3884, cal_y1=3945)
    print("Display in portrait mode")

lv.init()


