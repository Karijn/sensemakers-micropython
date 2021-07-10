
import lvgl as lv
import lvesp32
import display_driver

b = lv.btn(lv.scr_act())
b.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
b.set_drag(True)
l = lv.label(b)
l.set_text("Hello World!")
