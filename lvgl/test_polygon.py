#!//opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
import time
import math
from lv_colors import lv_colors

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res
def clear():
    canvas.fill_bg(lv_colors.BLACK, lv.OPA.COVER)
    
cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)
        
# create a canvas
canvas = lv.canvas(lv.scr_act(),None)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
canvas.align(None,lv.ALIGN.CENTER,0,0)

print("Triangle")

p1=lv.point_t()
p2=lv.point_t()
p3=lv.point_t()
p4=lv.point_t()
p5=lv.point_t()
p6=lv.point_t()
p7=lv.point_t()
p8=lv.point_t()

point_array=[p1,p2,p3]

rect_dsc = lv.draw_rect_dsc_t()
rect_dsc.init()
rect_dsc.bg_color = lv_colors.BLUE
rect_dsc.bg_opa = lv.OPA.COVER
rect_dsc.border_color = lv_colors.WHITE
rect_dsc.border_width = 1

p1.x = CANVAS_WIDTH//2
p1.y = 0
p2.x = 0
p2.y = CANVAS_HEIGHT-1
p3.x = CANVAS_WIDTH-1
p3.y = CANVAS_HEIGHT-1
canvas.draw_polygon(point_array,3,rect_dsc)
time.sleep(1)
clear()

print("rectangle")
p1.x = 0
p1.y = 0

p2.x = 0
p2.y = CANVAS_HEIGHT-1

p3.x = CANVAS_WIDTH-1
p3.y = CANVAS_HEIGHT-1

p4.x = CANVAS_WIDTH-1
p4.y = 0

point_array=[p1,p2,p3,p4]
canvas.draw_polygon(point_array,4,rect_dsc)

time.sleep(1)
clear()

print("octagon")
offset = (CANVAS_WIDTH-CANVAS_HEIGHT)//2
p1.x = 80+offset
p1.y = 0

p2.x = 0+offset
p2.y = 80

p3.x = 0+offset
p3.y = 160

p4.x = 80+offset
p4.y = 239

p5.x = 160+offset
p5.y = 239

p6.x = 240+offset
p6.y = 160

p7.x = 240+offset
p7.y = 80

p8.x = 160+offset
p8.y = 0
point_array=[p1,p2,p3,p4,p5,p6,p7,p8]
canvas.draw_polygon(point_array,8,rect_dsc)

