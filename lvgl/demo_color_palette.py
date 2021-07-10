#!//opt/bin/lv_micropython -i
"""SSD1351 demo (shapes)."""

import lvgl as lv
import display_driver
from utime import sleep
from math import cos, sin, pi, radians, floor
from lv_colors import lv_colors,LV_COLOR_MAKE

def clear(color=lv_colors.BLACK):
    canvas.fill_bg(color, lv.OPA.COVER)
    
def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

class coloredCircle(lv.obj):
    
    def __init__(self,parent,x0,y0,radius,color):
        super().__init__(parent)

        self.set_width(2*radius)
        self.set_height(2*radius)
        self.set_x(x0-radius)
        self.set_y(y0-radius)
        # color the box
        circle_style = lv.style_t()
        circle_style.init()
        circle_style.set_bg_color(lv.STATE.DEFAULT, color)
        circle_style.set_border_width(lv.STATE.DEFAULT, 0)
        circle_style.set_radius(lv.STATE.DEFAULT, radius)
        self.add_style(lv.obj.PART.MAIN, circle_style)

def test():
    """Test code."""
    
    CANVAS_WIDTH = lv.scr_act().get_disp().driver.hor_res
    CANVAS_HEIGHT = lv.scr_act().get_disp().driver.ver_res
    # black screen color
    scr_style = lv.style_t()
    scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
    lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)
    
    radius = CANVAS_HEIGHT//16
    offset = (CANVAS_WIDTH-CANVAS_HEIGHT)//2
    c = 0
    for x in range(0, CANVAS_HEIGHT, 2*radius):
        for y in range(0, CANVAS_HEIGHT, 2*radius):
            color = LV_COLOR_MAKE(*hsv_to_rgb(c / 64, 1, 1))
            circle = coloredCircle(lv.scr_act(),x+radius+offset ,y+radius, radius, color)
            c += 1
        
test()
