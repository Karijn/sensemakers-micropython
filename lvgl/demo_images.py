#!/opt/bin/lv_micropython -i
"""ST7735 demo (images)."""
from time import sleep
import lvgl as lv
import lvesp32
from ili9XXX import ili9341
from xpt2046 import xpt2046

from display_driver_utils import driver, ORIENT_LANDSCAPE
import time,sys
from lv_colors import lv_colors
#drv=driver(width=320,height=240,orientation=ORIENT_LANDSCAPE)
drv = ili9341(miso=19, mosi=23, clk=18, cs=26, dc=5, rst=33, power=-1, backlight=-1, mhz=40, factor=4, hybrid=False, width=320,height=240,orientation=ORIENT_LANDSCAPE)

# Display a raw image
SDL     = 0
ILI9341 = 1

def drawImage(filename):

    img_height = 240
    img_width = 320
    # print("filename: ",filename)
    if '320x240' in filename:
        # print('320x240 image')
        offset = 0
    else:
        offset = (img_width - img_height)//2
        img_width=240

    sdl_filename = '../assets/' + filename + '_argb8888.bin'
    ili3941_filename = '/assets/' + filename + '_rgb565.bin'
    # print("filenames: " + sdl_filename + ", " + ili3941_filename)
    
    try:
        with open(sdl_filename,'rb') as f:
            img_data = f.read()
            # print(sdl_filename + " successfully read")
            driver = SDL
    except:
        try:
            with open(ili3941_filename,'rb') as f:
                img_data = f.read()
                # print(ili3941_filename + " successfully read")
                driver = ILI9341
        except:
            print("Could not open image file")
            sys.exit()

    image = lv.img(lv.scr_act(),None)
    image.set_x(offset)
    if driver == SDL:
        img_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": img_width, "h": img_height,
                           "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data_size": len(img_data),
                "data": img_data,
            }
        )
    else:
        img_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": img_width, "h": img_height,
                           "cf": lv.img.CF.TRUE_COLOR},
                "data_size": len(img_data),
                "data": img_data,
            }
        )
    image.set_src(img_dsc)
    time.sleep(5)
    image.delete()
     
images = ['RaspberryPiWB240x240','python_320x240','Tabby240x240','Tortie240x240']
        
scr_style = lv.style_t()
scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)

while True:
    for filename in images:
        drawImage(filename)
    
