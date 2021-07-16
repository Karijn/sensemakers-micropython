#!/opt/bin/lv_micropython -i
import utime as time
import lvgl as lv
import display_driver


display_driver.getdisplay_landscape()

cw = lv.colorwheel(lv.scr_act(), True)
cw.set_size(200, 200)
cw.center()

