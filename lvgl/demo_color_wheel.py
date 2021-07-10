#!//opt/bin/lv_micropython -i
import lvgl as lv
from time import sleep 
import display_driver
from math import sin,cos,pi
from lv_colors import LV_COLOR_MAKE, lv_colors

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res

HALF_WIDTH = CANVAS_WIDTH // 2
HALF_HEIGHT = CANVAS_HEIGHT // 2
CENTER_X = CANVAS_WIDTH // 2 -1
CENTER_Y = CANVAS_HEIGHT // 2 -1
ANGLE_STEP_SIZE = 0.05  # Decrease step size for higher resolution
PI2 = pi * 2

def clear(canvas):
    canvas.fill_bg(lv_colors.BLACK, lv.OPA.COVER)
    
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
 
def test():
    """Test code."""
    cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)
    # create a canvas
    canvas = lv.canvas(lv.scr_act(),None)
    canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
    canvas.align(None,lv.ALIGN.CENTER,0,0)
    
    p1=lv.point_t()
    p2=lv.point_t()
    point_array=[p1,p2]
    
    p2.x = CENTER_X
    p2.y = CENTER_Y
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    line_dsc.opa = lv.OPA.COVER
    x, y = 0, 0
    angle = 0.0
    #  Loop all angles from 0 to 2 * PI radians
    while angle < PI2:
        # Calculate x, y from a vector with known length and angle
        x = int(CENTER_Y * sin(angle) + HALF_WIDTH)
        y = int(CENTER_Y * cos(angle) + HALF_HEIGHT)
        color = LV_COLOR_MAKE(*hsv_to_rgb(angle / PI2, 1, 1))
        line_dsc.color = color;
        p1.x = x
        p1.y = y
        canvas.draw_line(point_array,2, line_dsc)
        angle += ANGLE_STEP_SIZE
        
    sleep(5)
    clear(canvas)
    line_dsc.width=3
    for r in range(CENTER_Y, 0, -1):
        line_dsc.color = LV_COLOR_MAKE(*hsv_to_rgb(r / HALF_HEIGHT, 1, 1))
        
        canvas.draw_arc(CENTER_X, CENTER_Y, r, 0, 360, line_dsc)

    sleep(5)

test()
