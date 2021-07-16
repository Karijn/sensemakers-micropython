#!/opt/bin/lv_micropython -i
import utime as time
import lvgl as lv
import display_driver


display_driver.getdisplay_landscape()


# Create a spinner
spinner = lv.spinner(lv.scr_act(), 1000, 60)
spinner.set_size(100, 100)
spinner.center()


