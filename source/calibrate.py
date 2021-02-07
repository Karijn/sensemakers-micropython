#
# Some sample code
#
import os, gc
from uctypes import addressof
from lib.display.DISPLAY import *
from time import sleep_ms
import lib.fonts.opensans_16

def draw_crosshair(tft, x, y):
    tft.draw_hline(x - 10, y, 20, color565(255, 0, 0))
    tft.draw_vline(x, y - 10, 20, color565(255, 0, 0))

def calibrate():

    width, height = getdisplay().get_screensize()

    gettouch().touch_parameter(confidence=20, margin = 40) # make it slow & precise
    getdisplay().set_font(lib.fonts.opensans_16)

    getdisplay().clear()
    getdisplay().set_pos(40, 36)
    getdisplay().print('Touch the crosshair in the upper left corner')

    draw_crosshair(getdisplay(), 10, 10)
    x1, y1 = gettouch().get_touch(raw = True) # need the raw values here

    getdisplay().clear()
    getdisplay().set_pos(40, 36)
    getdisplay().print('Touch the crosshair in the upper right corner')

    draw_crosshair(getdisplay(), width - 11, 10)
    x2, y2 = gettouch().get_touch(raw = True) # need the raw values here

    getdisplay().clear()
    getdisplay().set_pos(40, 36)
    getdisplay().print('Touch the crosshair in the lower left corner')

    draw_crosshair(getdisplay(), 10, height - 11)
    x3, y3 = gettouch().get_touch(raw = True) # need the raw values here

    getdisplay().clear()
    getdisplay().set_pos(40, 36)
    getdisplay().print('Touch the crosshair in the lower right corner')

    draw_crosshair(getdisplay(), width - 11, height - 11)
    x4, y4 = gettouch().get_touch(raw = True) # need the raw values here

    xmul_top = (width - 20) / (x2 - x1)
    xadd_top = int(-x1 + 10 / xmul_top)
    xmul_bot = (width - 20) / (x4 - x3)
    xadd_bot = int(-x3 + 10 / xmul_bot)
    ymul_left = (height - 20) / (y3 - y1)
    yadd_left = int(-y1 + 10 / ymul_left)
    ymul_right = (height - 20) / (y4 - y2)
    yadd_right = int(-y2 + 10 / ymul_right)
    res = "({},{:6.4},{},{:6.4},{},{:6.4},{},{:6.4})".format(
            xadd_top, xmul_top, xadd_bot, xmul_bot, yadd_left, ymul_left, yadd_right, ymul_right)

    getdisplay().clear()
    getdisplay().set_pos(10, 120)
    getdisplay().print('Calibration = ' )
    getdisplay().print( res )

    calibration = (xadd_top, xmul_top, xadd_bot, xmul_bot, yadd_left, ymul_left, yadd_right, ymul_right)
    gettouch().touch_parameter(confidence = 5, margin = 20, calibration = calibration)

#        getdisplay().set_pos(10, 120)
#        getdisplay().print('Now you may touch for testing' )
#    else:
#        getdisplay().set_pos(10, 120)
#        getdisplay().print('Please touch me!' )

#    while True:
#        res = gettouch().get_touch()
#        if res:
#            getdisplay().fill_circle(res[0], res[1], 5, color565(255,255, 0))
    return calibration

