
import lvgl as lv
import lvesp32
import display_driver


# kb = lv.keyboard(lv.scr_act(), None)
# kb.set_textarea(lv.scr_act())

# ta = lv.textarea(lv.scr_act(), None)

# ta.align(lv.scr_act(), lv.ALIGN.OUT_RIGHT_TOP, 10, 10)

LV_DPI=130
LV_VER_RES=240

def event_handler(source,evt):
    if  evt == lv.EVENT.VALUE_CHANGED:
        print("Value:",textarea.get_text())
            
# create a keyboard and apply the styles
keyb = lv.keyboard(lv.scr_act(),None)
keyb.set_cursor_manage(True)

#Create a text area. The keyboard will write here
ta=lv.textarea(lv.scr_act(),None)
ta.align(None,lv.ALIGN.IN_TOP_MID,5,LV_DPI//16)
ta.set_text("")
max_h = LV_VER_RES // 2 - LV_DPI // 8
if ta.get_height() > max_h:
    ta.set_height(max_h)

# Assign the text area to the keyboard*/
keyb.set_textarea(ta)    
