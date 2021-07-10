#!/opt/bin/lv_micropython -i
import utime as time
import lvgl as lv
import display_driver
from lv_colors import lv_colors
try:
    from machine import Pin, ADC
    display_type = 'ili9341'
except:
    display_type = 'SDL'
    
# needle colors
needle_color=[lv_colors.BLUE]
label_style = lv.style_t()
label_style.init()
label_style.set_text_color(lv.STATE.DEFAULT,lv_colors.RED)
label_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_16)

label = lv.label(lv.scr_act())
label.add_style(lv.label.PART.MAIN,label_style)
label.set_text("Voltmeter [mV]")        
label.align(None,lv.ALIGN.IN_TOP_MID,0,5)

value_label = lv.label(lv.scr_act())
value_label.align(None,lv.ALIGN.IN_BOTTOM_RIGHT,-10,-10)

# create the gauge
gauge=lv.gauge(lv.scr_act(),None)
gauge.set_needle_count(1, needle_color)
gauge.set_size(200,200)
gauge.set_range(0,5000)
gauge.set_scale(280,26,6)
gauge.set_critical_value(3300)
gauge.align(None,lv.ALIGN.CENTER,0,8)


if not display_type == 'SDL':
    slider = ADC(Pin(36))  # create ADC object on ADC pin 36
    slider.atten(ADC.ATTN_11DB)

if display_type == 'SDL':
    while True:
        # ramp up the dummy voltage from 5 to 5V 
        for v in range(0,5000,100):
            value_text = "{:.1f} V".format(v/1000)
            value_label.set_text(value_text)
            gauge.set_value(0,v)
            time.sleep_ms(100)
        for v in range (5000,0,-100):            
            value_label.set_text("{:.1f} V".format(v/1000))
            gauge.set_value(0,v)
            time.sleep_ms(100)

else:
    while True:
        # measure the voltage on the ADC and display it on the voltmeter
        v = slider.read()*5/4096
        print("voltage:",v)
        value_label.set_text("{:.1f} V".format(v))
        gauge.set_value(0,round(v*1000))
