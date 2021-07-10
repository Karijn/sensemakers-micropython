
import lvgl as lv
import lvesp32
import display_driver


# load the font file from filesystem
myfont = lv.font_load("S:res/PHT-ASCII-20.bin")  # Refer here to convert your font file: https://github.com/lvgl/lv_font_conv

scr = lv.scr_act()
scr.clean()

style = lv.style_t()
style.init()

label = lv.label(scr)
style.set_text_font(lv.STATE.DEFAULT, myfont)
#label.add_style(label.PART.MAIN, style)

label.set_text("Hi LVGL(Load fonts dynamically)")
label.align(None, lv.ALIGN.CENTER, 0, 0)
