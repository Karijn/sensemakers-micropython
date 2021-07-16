#!/opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
LV_DPI=130
LV_VER_RES=240



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
ta = lv.textarea(lv.scr_act())
ta.set_width(150)
ta.set_height(100)
ta.align(lv.ALIGN.TOP_LEFT, 10, 10)
ta.add_event_cb(lambda e: ta_event_cb(e,kb), lv.EVENT.ALL, None)
ta.set_placeholder_text("Hello")

ta = lv.textarea(lv.scr_act())
ta.set_width(150)
ta.set_height(100)
ta.align(lv.ALIGN.TOP_RIGHT, -10, 10)
ta.add_event_cb(lambda e: ta_event_cb(e,kb), lv.EVENT.ALL, None)

kb.set_textarea(ta)


# def event_handler(source, evt):
#     global ta, keyb
#     source.def_event_cb(evt)
#     print("evt: ", evt )
#     if  evt == lv.EVENT.VALUE_CHANGED:
#         print("- Value:", ta.get_text())

    
    
# # create screen
# scr = lv.scr_act()
# #scr = lv.obj()   # needs: lv.scr_load(scr) 

# # set Background screen 
# # scr.set_style_local_bg_color(scr.PART.MAIN, lv.STATE.DEFAULT, lv.color_hex(0x000000))


# # create a keyboard and apply the styles
# keyb = lv.keyboard(scr)
# #keyb.set_cursor_manage(True)

# #Create a text area. The keyboard will write here
# ta=lv.textarea(scr)
# #ta.align(None,lv.ALIGN.,0,LV_DPI//16)
# ta.set_text("")
# max_h = LV_VER_RES // 2 - LV_DPI // 8
# if ta.get_height() > max_h:
#     ta.set_height(max_h)

# #keyb.add_flag(lv.FLAG.EVENT_BUBBLE)
# #keyb.set_event_cb(event_handler)

# # Assign the text area to the keyboard*/
# keyb.set_textarea(ta)    

# # load the screen
# #lv.scr_load(scr)