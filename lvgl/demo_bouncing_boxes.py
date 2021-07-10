#!//opt/bin/lv_micropython -i 
import lvgl as lv
import display_driver
import time
import math
import sys
from lv_colors import lv_colors
from random import random, seed
from utime import sleep_us, ticks_cpu, ticks_us, ticks_diff

"""lvgl demo (bouncing boxes)."""

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res

def clear():
    canvas.fill_bg(lv_colors.BLACK, lv.OPA.COVER)
        
class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, canvas, x_speed, y_speed, color):
        """Initialize box.

        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            display (SSD1351): OLED display object.
            color (int): RGB565 color value.
        """
        self.canvas = canvas
        self.size = size
        self.w = screen_width
        self.h = screen_height
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed
        
        self.x = self.w / 2.0
        self.y = self.h / 2.0
        self.prev_x = self.x
        self.prev_y = self.y

    def update_pos(self):
        """Update box position and speed."""
        x = self.x
        y = self.y
        size = self.size
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)
        self.prev_x = x
        self.prev_y = y

        if x + size >= w - x_speed:
            self.x_speed = -x_speed
        elif x - size <= x_speed + 1:
            self.x_speed = x_speed

        if y + size >= h - y_speed:
            self.y_speed = -y_speed
        elif y - size <= y_speed + 1:
            self.y_speed = y_speed

        self.x = x + self.x_speed
        self.y = y + self.y_speed

    def draw(self):
        """Draw box."""
        rect_dsc = lv.draw_rect_dsc_t()
        rect_dsc.init()
        rect_dsc.bg_opa = lv.OPA.COVER
        rect_dsc.bg_color = lv_colors.BLACK
        rect_dsc.border_opa = lv.OPA._90
        
        x = int(self.x)
        y = int(self.y)
        size = self.size
        prev_x = int(self.prev_x)
        prev_y = int(self.prev_y)
        
        self.canvas.draw_rect(prev_x - size,
                         prev_y - size,
                              size, size, rect_dsc)
        rect_dsc.bg_color = self.color       
        self.canvas.draw_rect(x - size,
                              y - size,
                              size, size, rect_dsc)


def test(canvas):
    """Bouncing box."""
 
    try:
        clear()
        colors = [lv_colors.RED,
                  lv_colors.GREEN,
                  lv_colors.BLUE,
                  lv_colors.YELLOW,
                  lv_colors.CYAN,
                  lv_colors.MAGENTA]
        
        # Generate non-zero random speeds between -5.0 and 5.0
        seed(ticks_cpu())
        x_speed = []
        y_speed = []
        
        for i in range(6):
            r = random() * 10.0
            if r < 5:
                x_speed.append(r)
            else:
                x_speed.append(r-10)
                
            r = random() * 10.0
            if r < 5:
                y_speed.append(r)
            else:
                y_speed.append(r-10)

            
        # print("speed_x: ",x_speed)
        sizes = [12, 11, 10, 9, 8, 7]
        boxes = [Box(CANVAS_WIDTH, CANVAS_HEIGHT, sizes[i], canvas, x_speed[i], y_speed[i], colors[i]) for i in range(6)]
        
        while True:
            timer = ticks_us()
            for b in boxes:
                b.update_pos()
                b.draw()
            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)

    except KeyboardInterrupt:
        sys.exit()
        
cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)
        
# create a canvas
canvas = lv.canvas(lv.scr_act(),None)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
canvas.align(None,lv.ALIGN.CENTER,0,0)
test(canvas)
