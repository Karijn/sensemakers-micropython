import lvgl as lv
import display_driver

display_driver.getdisplay_landscape()

### Make style 1
style1 = lv.style_t()
style1.init()
style1.set_radius(5)

# Make a gradient
style1.set_bg_opa(lv.OPA.COVER)
style1.set_bg_color(lv.palette_lighten(lv.PALETTE.GREY, 1))
style1.set_bg_grad_color(lv.palette_main(lv.PALETTE.BLUE))
style1.set_bg_grad_dir(lv.GRAD_DIR.VER)

# Shift the gradient to the bottom
style1.set_bg_main_stop(128)
style1.set_bg_grad_stop(192)


### Make style 2
style2 = lv.style_t()
style2.init()
style2.set_radius(5)

# Make a gradient
style2.set_bg_opa(lv.OPA.COVER)
style2.set_bg_color(lv.palette_lighten(lv.PALETTE.YELLOW, 1))
style2.set_bg_grad_color(lv.palette_main(lv.PALETTE.RED))
style2.set_bg_grad_dir(lv.GRAD_DIR.HOR)

# Shift the gradient to the bottom
style2.set_bg_main_stop(50)
style2.set_bg_grad_stop(200)

# Create an object with the new style1
obj = lv.obj(lv.scr_act())
obj.add_style(style1, 0)
obj.center()

lv.scr_act().add_style(style2, 0)