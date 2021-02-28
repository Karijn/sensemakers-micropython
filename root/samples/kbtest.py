from lib.display.DISPLAY import *
from lib.display.touch_keyboard import TouchKeyboard
from lib.fonts import roboto_cond_reg_24
from time import ticks_ms, ticks_diff, sleep_ms

#roboto_cond_reg_24
#opensans_24
#free_sans_oblique_24

getdisplay(3).set_font(roboto_cond_reg_24)
getdisplay().clear()
t = TouchKeyboard(roboto_cond_reg_24)
t.load_keyboard()
text = 'Hoi Piepeloi !'
t.set_text(text)
showmessage = False

while True:
    pos = gettouch().get_touch(initial=False, wait=False)
    if pos is not None:
        print('touch at {}'.format(pos))
        ret = t.handle_keypress(pos[1], pos[0], False)
        # if ret:
        #     if showmessage:
        #         getdisplay().set_color(0xffff, 0)
        #         t.set_text(text)
        #         showmessage = False
        #     else:
        #         text = t.kb_text
        #         t.show_message('Hallo', 12345)
        #         showmessage = True
    sleep_ms(50)