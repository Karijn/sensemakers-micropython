import lvgl as lv
import display_driver
from utime import sleep
from math import cos, sin, pi, radians, floor
from lv_colors import lv_colors,LV_COLOR_MAKE

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res
print("canvas width: %d, canvas_height: %d"%(CANVAS_WIDTH,CANVAS_HEIGHT))


scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text("Hello World!")

# Load the screen

lv.scr_load(scr)
