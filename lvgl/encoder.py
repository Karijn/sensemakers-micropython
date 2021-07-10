from display_driver import *
import lvgl as lv
from lv_colors import lv_colors
import math

def clear(color=lv_colors.BLACK):
  canvas.fill_bg(color, lv.OPA.COVER)

def draw_filledCircle(canvas, x0, y0, r, color):
  """Draw a filled circle.
  
  Args:
     x0 (int): X coordinate of center point.
     y0 (int): Y coordinate of center point.
     r (int): Radius.
     color (int): RGB565 color value.
  """
  p1=lv.point_t()
  p2=lv.point_t()
  point_array=[p1,p2]
  
  line_dsc = lv.draw_line_dsc_t()
  line_dsc.init()
  line_dsc.color = color
  line_dsc.opa = lv.OPA.COVER
  
  f = 1 - r
  dx = 1
  dy = -r - r
  x = 0
  y = r
  p1.x = x0
  p1.y = y0 - r
  p2.x = p1.x
  p2.y = p1.y + 2 * r + 1
  canvas.draw_line(point_array,2, line_dsc)
  while x < y:
    if f >= 0:
      y -= 1
      dy += 2
      f += dy
    x += 1
    dx += 2
    f += dx
    p1.x = x0 + x
    p1.y = y0 - y
    p2.x = p1.x
    p2.y = p1.y +  2 * y + 1
    canvas.draw_line(point_array,2,line_dsc)
    p1.x = x0 - x
    p2.x = p1.x
    canvas.draw_line(point_array,2,line_dsc)
    p1.x = x0 - y
    p1.y = y0 - x
    p2.x = p1.x
    p2.y = p1.y + 2 * x + 1
    canvas.draw_line(point_array,2,line_dsc)
    p1.x = x0 + y
    p2.x = p1.x
    canvas.draw_line(point_array,2,line_dsc)

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res
print("canvas width: %d, canvas_height: %d"%(CANVAS_WIDTH,CANVAS_HEIGHT))


cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)
canvas = lv.canvas(lv.scr_act(),None)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
#canvas.align(None,lv.ALIGN.CENTER,0,0)

#draw_filledCircle(canvas, 120, 120, r, lv_colors.GREEN)
clear()
draw_filledCircle(canvas, 120, 120, 90, lv_colors.GREEN)
draw_filledCircle(canvas, 120, 120, 50, lv_colors.BLACK)

draw_filledCircle(canvas, 120, 120, 5, lv_colors.GREEN)

ap = None
while True:
  coords = touch.get_coords()
  if coords is not None:
    x = coords[0] - 120
    y = coords[1] - 120
    c2 = (x * x) + (y * y) 
    if  2500 <= c2 <= 8100:
      a = int(round(math.degrees(math.atan2(x,y))))
      if ap is not None:
        av = ap - a
        if av > 315:
          av = av - 360
        if av < -315:
          av = av + 360
        av = av // 15
        #print("({}, {}) ==> {} {}°  {} ".format( x, y, c2, a, av ))
        if av != 0:
          print("{:4}".format( av ))
      ap = a
  else:
    ap = None
