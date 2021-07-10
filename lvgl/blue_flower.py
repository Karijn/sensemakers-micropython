#!/opt/bin/lv_micropython -i 
import lvgl as lv
import display_driver
import time,sys

# Display a raw image
SDL     = 0
ILI9341 = 1

try:
  with open('assets/blue_flower_argb8888.bin','rb') as f:
    print('try open ')
    img_data = f.read()
    driver = SDL
except:
  try:
    with open('assets/blue_flower_rgb565.bin','rb') as f:
      img_data = f.read()
      driver = ILI9341
  except:
    print("Could not open image file")
    sys.exit()
    
scr = lv.scr_act()
img = lv.img(scr)
img.align(scr, lv.ALIGN.CENTER, 0, 0)
if driver == SDL:
  img_dsc = lv.img_dsc_t(
    {
      "header": {"always_zero": 0, "w": 100, "h": 75, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
      "data_size": len(img_data),
      "data": img_data,
    }
  )
else:
    img_dsc = lv.img_dsc_t(
    {
      "header": {"always_zero": 0, "w": 100, "h": 75, "cf": lv.img.CF.TRUE_COLOR},
      "data_size": len(img_data),
      "data": img_data,
    }
  )
img.set_src(img_dsc)
img.set_drag(True)


