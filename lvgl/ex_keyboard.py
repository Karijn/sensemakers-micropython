#!/opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
LV_DPI=130
LV_VER_RES=240

display_driver.getdisplay_landscape()

def ta_event_cb(e,kb):
    code = e.get_code()
    ta = e.get_target()
    if code == lv.EVENT.FOCUSED:
        kb.set_textarea(ta)
        kb.clear_flag(lv.obj.FLAG.HIDDEN)

    if code == lv.EVENT.DEFOCUSED:
        kb.set_textarea(None)
        kb.add_flag(lv.obj.FLAG.HIDDEN)
        
# Create a keyboard to use it with an of the text areas
kb = lv.keyboard(lv.scr_act())

# Create a text area. The keyboard will write here
ta1 = lv.textarea(lv.scr_act())
ta1.set_width(150)
ta1.set_height(100)
ta1.align(lv.ALIGN.TOP_LEFT, 10, 10)
ta1.add_event_cb(lambda e: ta_event_cb(e,kb), lv.EVENT.ALL, None)
ta1.set_placeholder_text("enter some text here")

ta2 = lv.textarea(lv.scr_act())
ta2.set_width(150)
ta2.set_height(100)
ta2.align(lv.ALIGN.TOP_RIGHT, -10, 10)
ta2.add_event_cb(lambda e: ta_event_cb(e,kb), lv.EVENT.ALL, None)
ta2.set_text("Peekaboe!")
kb.set_textarea(ta1)
