#!//opt/bin/lv_micropython -i
"""SSD1351 demo (shapes)."""

import lvgl as lv
import display_driver
from utime import sleep
from math import cos, sin, pi, radians, floor
from lv_colors import lv_colors,LV_COLOR_MAKE

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res
print("canvas width: %d, canvas_height: %d"%(CANVAS_WIDTH,CANVAS_HEIGHT))

def clear(color=lv_colors.BLACK):
    canvas.fill_bg(color, lv.OPA.COVER)

def draw_lines(canvas,points,color):
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    line_dsc.color = color
    line_dsc.opa = lv.OPA.COVER
    
    print(len(points))
    for i in range(len(points)-1):
        point_array = [points[i],points[i+1]]
        canvas.draw_line(point_array,2,line_dsc)
        
    
def test(canvas):
    """Test code."""
    print('display started')


    clear(lv_colors.GREEN)
    sleep(1)

    clear()
    
    p1=lv.point_t()
    p2=lv.point_t()
    point_array=[p1,p2]
    
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    line_dsc.color = lv_colors.MAGENTA
    line_dsc.opa = lv.OPA.COVER

    p1.x = 10
    p1.y = CANVAS_HEIGHT-1
    p2.x = p1.x + CANVAS_WIDTH //2
    p2.y = p1.y
    canvas.draw_line(point_array, 2, line_dsc)
    sleep(1)

    p1.y = 0
    p2.x = p1.x
    p2.y = CANVAS_HEIGHT-1
    line_dsc.color = lv_colors.CYAN
    canvas.draw_line(point_array, 2, line_dsc)
    sleep(1)
    
    rect_dsc = lv.draw_rect_dsc_t()
    rect_dsc.init()
    rect_dsc.bg_opa = lv.OPA.COVER
    rect_dsc.bg_color = lv_colors.WHITE

    canvas.draw_rect(round(CANVAS_WIDTH/5.56),round(CANVAS_HEIGHT/2.56),round(CANVAS_WIDTH/4.2),round(CANVAS_HEIGHT/1.7),rect_dsc)
    sleep(1)

    p1.x = 0
    p1.y = 0
    p2.x = CANVAS_WIDTH-1
    p2.y = p1.y
    line_dsc.color = lv_colors.RED
    canvas.draw_line(point_array, 2, line_dsc)
    
    sleep(1)
    p1.x = CANVAS_WIDTH-1
    p1.y = 0
    p2.x = CANVAS_WIDTH//2
    p2.y = CANVAS_HEIGHT
    line_dsc.color = lv_colors.YELLOW
    canvas.draw_line(point_array, 2, line_dsc)
    sleep(1)
    clear() 

    coords = [{"x":0,                        "y":round(CANVAS_WIDTH*0.65)},
              {"x":round(CANVAS_WIDTH*0.52), "y":round(CANVAS_HEIGHT*0.83)},
              {"x":round(CANVAS_WIDTH*0.95), "y":round(CANVAS_HEIGHT*0.96)},
              {"x":round(CANVAS_WIDTH*0.41), "y":round(CANVAS_HEIGHT*0.52)},
              {"x":round(CANVAS_WIDTH*0.61), "y":round(CANVAS_HEIGHT*0.15)},
              {"x":0,                        "y":round(CANVAS_HEIGHT*0.65)}]
    
    draw_lines(canvas,coords,lv_colors.YELLOW)
    sleep(1)
    clear()

    offset = (CANVAS_WIDTH-CANVAS_HEIGHT)//2 
    sides = 7
    rotate = 0
    x0 = CANVAS_HEIGHT//2    # center position
    y0 = x0
    r = 3*CANVAS_HEIGHT//8   # radius
    theta = radians(rotate)
    n = sides + 1
    point_array=[]
    for s in range(n):
        t = 2.0 * pi * s / sides + theta
        point = lv.point_t()
        point.x = int(r * cos(t) + x0) + offset
        point.y = int(r * sin(t) + y0)
        point_array.append(point)
        
        # coords.append([int(r * cos(t) + x0), int(r * sin(t) + y0)])
        
    rect_dsc.bg_color = lv_colors.GREEN
    canvas.draw_polygon(point_array,8,rect_dsc)
    rect_dsc.bg_color = lv_colors.RED        
    canvas.draw_rect(0, 0, 30, 239, rect_dsc)
    sleep(1)
    
    '''
    offset = (CANVAS_WIDTH-CANVAS_HEIGHT/2)
    coords = [{"x":0,                        "y":round(CANVAS_WIDTH*0.65)},
              {"x":round(CANVAS_WIDTH*0.52), "y":round(CANVAS_HEIGHT*0.83)},
              {"x":round(CANVAS_WIDTH*0.95), "y":round(CANVAS_HEIGHT*0.96)},
              {"x":round(CANVAS_WIDTH*0.41), "y":round(CANVAS_HEIGHT*0.52)},
              {"x":round(CANVAS_WIDTH*0.61), "y":round(CANVAS_HEIGHT*0.15)}]

    
    rect_dsc.bg_color = lv_colors.GREEN
    canvas.draw_polygon(coords,5,rect_dsc.bg_color)
    sleep(1)
    clear()
    '''
    
'''
    display.draw_filledRectangle(23, 50, 30, 75, color565(255, 255, 255))
    sleep(1)

    display.draw_hline(0, 0, 127, color565(255, 0, 0))
    sleep(1)

    display.draw_line(127, 0, 64, 127, color565(255, 255, 0))
    sleep(2)

    display.clear()
    
    coords = [[0, 157], [126, 200], [228, 230], [95, 125], [146, 37], [0, 157]]
    display.draw_lines(coords, color565(0, 255, 255))
    sleep(1)

    display.clear()
    display.draw_filledPolygon(7, 63, 63, 50, color565(0, 255, 0))
    sleep(1)

    display.draw_filledRectangle(0, 0, 15, 127, color565(255, 0, 0))
    sleep(1)

    display.clear()

    display.draw_filledRectangle(0, 0, 63, 63, color565(128, 128, 255))
    sleep(1)

    display.draw_rectangle(0, 64, 63, 63, color565(255, 0, 255))
    sleep(1)

    display.draw_filledRectangle(64, 0, 63, 63, color565(128, 0, 255))
    sleep(1)

    display.draw_polygon(3, 96, 96, 30, color565(0, 64, 255),
                         rotate=15)
    sleep(3)

    display.clear()

    display.draw_filledCircle(32, 32, 30, color565(0, 255, 0))
    sleep(1)

    display.draw_circle(32, 96, 30, color565(0, 0, 255))
    sleep(1)

    display.draw_filledEllipse(96, 32, 30, 16, color565(255, 0, 0))
    sleep(1)

    display.draw_ellipse(96, 96, 16, 30, color565(255, 255, 0))

    sleep(5)
    display.cleanup()
'''
cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)

# create a canvas
canvas = lv.canvas(lv.scr_act(),None)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
canvas.align(None,lv.ALIGN.CENTER,0,0)
test(canvas)
