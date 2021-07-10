#!/opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
import time
import math
from lv_colors import lv_colors

disp = lv.scr_act().get_disp()
CANVAS_WIDTH = disp.driver.hor_res
CANVAS_HEIGHT = disp.driver.ver_res
    
start_time = time.ticks_ms()

colors = [lv_colors.SILVER,lv_colors.RED,lv_colors.MAROON,lv_colors.YELLOW,lv_colors.OLIVE,
          lv_colors.LIME,lv_colors.GREEN,lv_colors.CYAN,lv_colors.AQUA,lv_colors.BLUE,
          lv_colors.GRAY,lv_colors.TEAL,lv_colors.NAVY,lv_colors.MAGENTA,lv_colors.PURPLE,
          lv_colors.ORANGE,lv_colors.WHITE]
def clear():
    canvas.fill_bg(lv_colors.BLACK, lv.OPA.COVER)
    
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

def testlines(canvas,color):
    print("Test lines")
    p1=lv.point_t()
    p2=lv.point_t()
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    line_dsc.color = color
    line_dsc.opa = lv.OPA.COVER
    
    clear()
    
    # from top left corner
    for x in range(0, CANVAS_WIDTH, 6):
        p1.x = 0
        p1.y = 0
        p2.x = x
        p2.y = CANVAS_HEIGHT - 1
        point_array=[p1,p2]
        canvas.draw_line(point_array,2,line_dsc)
        
    for y in range(0, CANVAS_HEIGHT, 6):
        p2.x = CANVAS_WIDTH- 1
        p2.y = y
        canvas.draw_line(point_array,2,line_dsc)
    time.sleep(1)
    clear()
        
    # from bottom left corner
    for x in range(0, CANVAS_WIDTH, 6):
        p1.x = 0
        p1.y = CANVAS_HEIGHT- 1
        p2.x = x
        p2.y = 0
        canvas.draw_line(point_array,2,line_dsc)

    for y in range(0, CANVAS_HEIGHT, 6):
        p2.x = CANVAS_WIDTH- 1
        p2.y = y
        canvas.draw_line(point_array,2,line_dsc)
        
    time.sleep(1)
    clear()

    # from bottom right corner 
    for x in range(0, CANVAS_WIDTH, 6):
        p1.x = CANVAS_WIDTH-1
        p1.y = CANVAS_HEIGHT-1
        p2.x = x
        p2.y = 0
        canvas.draw_line(point_array,2,line_dsc)
        
    for y in range(0, CANVAS_HEIGHT, 6):
        p2.x = 0
        p2.y = y
        canvas.draw_line(point_array,2,line_dsc)
            
    time.sleep(1)
    clear()

    # from top right corner
    for x in range(0, CANVAS_WIDTH, 6):
        p1.x = CANVAS_WIDTH-1
        p1.y = 0
        p2.x = x
        p2.y = CANVAS_HEIGHT-1
        canvas.draw_line(point_array,2,line_dsc)

    for y in range(0, CANVAS_HEIGHT, 6):
        p2.x = 0
        p2.y = y
        canvas.draw_line(point_array,2,line_dsc)
    
def testfastlines(canvas,color1,color2):
    # there are no hline and vline calls in the lvgl display driver
    # replace them by normal lines
    
    p1=lv.point_t()
    p2=lv.point_t()
    point_array=[p1,p2]
    
    # style for horizontal lines
    hline_dsc = lv.draw_line_dsc_t()
    hline_dsc.init()
    hline_dsc.color = color1
    hline_dsc.opa = lv.OPA.COVER
    
    # style for vertical lines    
    vline_dsc = lv.draw_line_dsc_t()
    vline_dsc.init()
    vline_dsc.color = color2
    vline_dsc.opa = lv.OPA.COVER
    
    print("Test horizontal and vertical fast lines")
    
    p1.x = 0
    p2.x = CANVAS_WIDTH-1
    for y in range(0, CANVAS_HEIGHT-1, 5):
        p1.y = y
        p2.y = y
        canvas.draw_line(point_array,2,hline_dsc)
    p1.y=0
    p2.y=CANVAS_HEIGHT-1
    for x in range(0, CANVAS_WIDTH-1, 5):
        p1.x = x
        p2.x = x       
        canvas.draw_line(point_array,2,vline_dsc)
        
def testdrawrects(canvas,color):
    print("Test rectangles")         
    rect_dsc = lv.draw_rect_dsc_t()
    rect_dsc.init()
    rect_dsc.bg_opa = lv.OPA.TRANSP
    rect_dsc.border_opa = lv.OPA._90
    rect_dsc.border_color = color
    rect_dsc.bg_color = lv_colors.BLACK
    rect_dsc.border_width = 1
    for x in range(0,CANVAS_WIDTH-1,6):
        canvas.draw_rect(CANVAS_WIDTH//2-x//2, CANVAS_HEIGHT//2 -x//2, x, x, rect_dsc)
    
def testfillrects(canvas,color1, color2):
    print("Test filled rectangles")
    rect_dsc = lv.draw_rect_dsc_t()
    rect_dsc.init()
    rect_dsc.bg_opa = lv.OPA.COVER
    rect_dsc.bg_color = color1
    rect_dsc.border_opa = lv.OPA._90
    rect_dsc.border_color = color2
    rect_dsc.border_width = 1

    for x in range(CANVAS_WIDTH,0,-6):
        canvas.draw_rect(CANVAS_WIDTH//2-x//2, CANVAS_HEIGHT//2 -x//2, x, x, rect_dsc)

def testtriangles(canvas):
    print("Test triangles")
    offset = (CANVAS_WIDTH-CANVAS_HEIGHT)//2
    p1=lv.point_t()
    p2=lv.point_t()
    point_array=[p1,p2]
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    w = CANVAS_HEIGHT // 2
    x = CANVAS_HEIGHT - 1
    y = 0
    z = CANVAS_HEIGHT -1
    for i in range(0, 15):
        line_dsc.color=colors[i]
        p1.x = w + offset
        p1.y = y
        p2.x = y + offset
        p2.y = x
        canvas.draw_line(point_array,2,line_dsc)
        p1.x = y + offset
        p1.y = x
        p2.x = z + offset
        canvas.draw_line(point_array,2,line_dsc)
        p1.x = z + offset
        p2.x = w + offset
        p2.y = y
        canvas.draw_line(point_array,2,line_dsc)
        x -= 8
        y += 8
        z -= 8

def testdrawcircles(canvas,radius, color):
    print("Test circles")
    circle_dsc = lv.draw_line_dsc_t()
    circle_dsc.init()
    circle_dsc.color = color
    
    for x in range(0, CANVAS_WIDTH + radius, radius * 2):
        for y in range(0, CANVAS_HEIGHT + radius, radius * 2):
            canvas.draw_arc(x, y, radius, 0, 360, circle_dsc)
    
def testfillcircles(canvas, radius, color):
    print("Test filled circles")
    for x in range(radius, CANVAS_WIDTH, radius * 2):
        for y in range(radius, CANVAS_HEIGHT, radius * 2):
            draw_filledCircle(canvas,x, y , radius, color)
            
def testroundrects(canvas):
    print("Test differently colored rectangles")
    rect_dsc = lv.draw_rect_dsc_t()
    rect_dsc.init()
    rect_dsc.radius = 8
    rect_dsc.bg_opa = lv.OPA.COVER
    rect_dsc.bg_color = lv_colors.BLACK
    rect_dsc.border_opa = lv.OPA._90
    rect_dsc.border_width = 1
    
    x = 0
    y = 0
    w = CANVAS_WIDTH - 2
    h = CANVAS_HEIGHT - 2
    
    for i in range(17):
        # print("x: %d, y: %d, w: %d, h: %d"%(x,y,w,h))
        rect_dsc.border_color = colors[i]
        canvas.draw_rect(x, y, w, h, rect_dsc)
        x += 5
        y += 7
        w -= 10
        h -= 14

def text_test(canvas):
    print("Test text printing")
    label_dsc = lv.draw_label_dsc_t()
    label_dsc.init()
    v = 0
    label_dsc.color = lv_colors.RED
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc, " Hello World!", lv.label.ALIGN.LEFT)
    v += 20
    label_dsc.color = lv_colors.GREEN
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc, str(math.pi), lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc," Want pi?" , lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc, hex(8675309) , lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc," Print HEX!" , lv.label.ALIGN.LEFT)
    v += 20
    label_dsc.color = lv_colors.WHITE
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc," Sketch has been" , lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc," running for: " , lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc, str((time.ticks_ms() - start_time)/ 1000), lv.label.ALIGN.LEFT)
    v += 20
    canvas.draw_text(0, v, CANVAS_WIDTH-1, label_dsc," seconds." , lv.label.ALIGN.LEFT)
    
def testtextwrap(label):
    print("Test text wrapping")
    label.set_long_mode(lv.label.LONG.BREAK)
    label.set_align(lv.label.ALIGN.LEFT)
    label.set_width(CANVAS_WIDTH)
    # label.set_text("Hello World")
    label.set_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ")
    
cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 4)
        
# create a canvas
canvas = lv.canvas(lv.scr_act(),None)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
canvas.align(None,lv.ALIGN.CENTER,0,0)

# test lines
testlines(canvas,lv_colors.GREEN)
time.sleep(2)
clear()
# there are no calls to hline and vline, these have been replaced by draw_line
testfastlines(canvas,lv_colors.RED, lv_colors.BLUE)
time.sleep(2)
clear()
# test rectangles
testdrawrects(canvas,lv_colors.GREEN)
time.sleep(2)
clear()
# test filled rectangles
testfillrects(canvas,lv_colors.PURPLE, lv_colors.YELLOW)
time.sleep(2)
clear()
# test rounded multi-color rectangles
testroundrects(canvas)
time.sleep(2)
clear()
# print some text to the canvas
text_test(canvas)
time.sleep(2)
clear()
# test circles
testfillcircles(canvas,10,lv_colors.BLUE)
time.sleep(0.5)
testdrawcircles(canvas,10, lv_colors.WHITE)
time.sleep(2)
clear()
# test triangles
testtriangles(canvas)
time.sleep(2)
canvas.delete()

style = lv.style_t()
style.init()
style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
style.set_bg_opa(lv.STATE.DEFAULT, lv.OPA.COVER)

lv.scr_act().add_style(lv.obj.PART.MAIN,style)

style.set_text_color(lv.label.PART.MAIN,lv_colors.YELLOW)
style.set_text_opa(lv.STATE.DEFAULT,lv.OPA.COVER)

label = lv.label(lv.scr_act(),None)
label.set_recolor(True)
label.add_style(lv.label.PART.MAIN,style)
testtextwrap(label)
