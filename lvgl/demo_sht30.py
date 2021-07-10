#!/opt/bin/lv_micropython -i
import lvgl as lv
from display_driver_utils import driver,ORIENT_LANDSCAPE
drv = driver(width=320,height=240,orientation=ORIENT_LANDSCAPE)

from lv_colors import lv_colors
from time import sleep
from meterClass import Meter

if drv.type == 'ili9341':
    from sht3x import SHT3X,SHT3XError
    # create a SHT3X object
    try:
        sht30 = SHT3X()
    except SHT3XError as exception:
        if exception.error_code == SHT3XError.BUS_ERROR:
            print("SHT30 module not found on the I2C bus, please connect it")
            sys.exit(-1)
        else:
            raise exception
else:
    from random import random

SCREEN_WIDTH  = lv.scr_act().get_disp().driver.hor_res
SCREEN_HEIGHT = lv.scr_act().get_disp().driver.ver_res
print("screen width: ",SCREEN_WIDTH)

text_style = lv.style_t()
text_style.init()
text_style.set_text_color(lv.STATE.DEFAULT,lv_colors.GREEN)
text_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_24)

label = lv.label(lv.scr_act())
label.set_text('SHT30 Measurements')
label.align(None, lv.ALIGN.OUT_TOP_MID, -50, 30)
label.add_style(lv.label.PART.MAIN,text_style)

if drv.type == 'ili9341':
    temp, humi = sht30.getTempAndHumi(clockStretching=SHT3X.CLOCK_STRETCH,repeatability=SHT3X.REP_S_HIGH)
    # print("Temperature: ",temp,"°C, Humidity: ",humi,"%")
else:
    temp = 23.7
    humi = 65.3

m1 = Meter(max_value=50,x=60,y=120,
           value=temp,legend=('0','10','20','30','40','50'),
           label_text='Temperature',value_text_format="{:.1f} °C")

 
m2 = Meter(x=220, y=120,
           value=humi,legend=('0','20','40','60','80','100'),
           label_text='Humidity',value_text_format="{:.1f} %")

# measure every 2 s and displa the result on the meters
while True:
    if  drv.type == 'ili9341':
        temp, humi = sht30.getTempAndHumi(clockStretching=SHT3X.CLOCK_STRETCH,repeatability=SHT3X.REP_S_HIGH)
    else:
        temp = 20.0 + random() *5
        humi = 55 + random() * 10
    m1.set_value(temp)
    m2.set_value(humi)
    sleep(2)
