#!/opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
import time,sys
from lv_colors import lv_colors

LV_ANIM_REPEAT_INFINITE = -1

class BouncingSprite():
    """Bouncing Sprite."""
    def __init__(self, img, w, h, speed):
        """Initialize sprite.

        Args:
            path (string): Path of sprite image.
            w, h (int): Width and height of image.
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            speed(int): Initial XY-Speed of sprite.
            display (SSD1351): OLED display object.
            color (int): RGB565 color value.
        """

        self.img = img
        self.w = w
        self.h = h
        self.screen_width =lv.scr_act().get_disp().driver.hor_res 
        self.screen_height = lv.scr_act().get_disp().driver.ver_res
        self.x_speed = speed
        self.y_speed = speed
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        
        self.img_anim = lv.anim_t()
        self.img_anim.init()
        self.img_anim.set_custom_exec_cb(lambda a, val: self.img_anim_cb(a,img,val))
        # self.img_anim.set_time(4000)
        # self.img_anim.set_playback_time(1000)
        self.img_anim.set_repeat_count(LV_ANIM_REPEAT_INFINITE)
        lv.anim_t.start(self.img_anim)

    def img_anim_cb(self,a,image,value):
        self.update_pos()
        # print("width: %d, height: %d, x: %d, y: %d" % (self.w,self.h,self.x,self.y))
        image.set_x(self.x)
        image.set_y(self.y)
        
    def update_pos(self):
        """Update sprite speed and position."""
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        x_speed = abs(self.x_speed)
        y_speed = abs(self.y_speed)

        if x + w + x_speed >= self.screen_width:
            self.x_speed = -x_speed
        elif x - x_speed < 0:
            self.x_speed = x_speed

        if y + h + y_speed >= self.screen_height:
            self.y_speed = -y_speed
        elif y - y_speed <= 0:
            self.y_speed = y_speed

        self.prev_x = x
        self.prev_y = y

        self.x = x + self.x_speed
        self.y = y + self.y_speed

# Display a raw image
scr_style = lv.style_t()
scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)

SDL     = 0
ILI9341 = 1
try:
    with open('../assets/Python41x49_argb8888.bin','rb') as f:
        img_data = f.read()
        driver = SDL
except:
    try:
        with open('/assets/Python41x49_rgb565.bin','rb') as f:
            img_data = f.read()
            driver=ILI9341        
    except:
        print("Could not open image file")
        sys.exit()
    
scr = lv.scr_act()
img = lv.img(scr)
img.align(scr, lv.ALIGN.CENTER, 0, 0)

if driver == SDL:
    img_dsc = lv.img_dsc_t(
        {
            "header": {"always_zero": 0, "w": 41, "h": 49, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
            "data_size": len(img_data),
            "data": img_data,
        }
    )
else:
    img_dsc = lv.img_dsc_t(
        {
            "header": {"always_zero": 0, "w": 41, "h": 49, "cf": lv.img.CF.TRUE_COLOR},
            "data_size": len(img_data),
            "data": img_data,
        }
    )
    
img.set_src(img_dsc)
sprite = BouncingSprite(img,41,49,2)

