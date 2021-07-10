#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors

class Meter():
    def __init__(self,x=None,y=None,
                 min_value=0,max_value=100,value=50,divisions=5,
                 legend=None,label_text=None,value_text_format=None,
                 bar_color=lv_colors.BLUE,legend_color=lv_colors.YELLOW,
                 value_color=lv_colors.WHITE,bg_color=lv_colors.BLACK):
        
        self.x = x
        self.y = y
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.width = 40
        self.height = 104
        self.label_text = label_text
        self.value_text_format = value_text_format
        self.bg_color = bg_color
        self.bar_color = bar_color
        self.value_color = value_color
        self.legend_color = legend_color
        self.base = 102
        if legend:
            self.divisions = len(legend) -1
        else:
            self.divisions = divisions
        
        scr_style = lv.style_t()
        scr_style.set_bg_color(lv.STATE.DEFAULT, self.bg_color)
        lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)
        

        
        # create a container

        self.container = lv.cont(lv.scr_act(),None)
        self.container.set_fit(lv.FIT.TIGHT)        
        self.container.align(None, lv.ALIGN.CENTER, 0, 0)
        if self.x:
            self.container.set_x(self.x)
        if self.y:
            self.container.set_y(self.y)            
        self.container.add_style(lv.obj.PART.MAIN,scr_style)
        
        cbuf=bytearray(self.width * self.height * 4)
        
        # create a canvas
        self.canvas = lv.canvas(self.container,None)
        self.canvas.set_buffer(cbuf,self.width,self.height,lv.img.CF.TRUE_COLOR)
        self.canvas.align(self.container,lv.ALIGN.CENTER, 0, -50)
        
        text_style = lv.style_t()
        text_style.init()
        text_style.set_text_color(lv.STATE.DEFAULT,self.legend_color)

        
        if self.value_text_format:
            value_text_style = lv.style_t()
            value_text_style.init()
            value_text_style.set_text_color(lv.STATE.DEFAULT,self.value_color)
            self.value_label = lv.label(self.container)
            self.value_label.add_style(lv.label.PART.MAIN,value_text_style)
            value_text = self.value_text_format.format(self.value)
            self.value_label.set_text(value_text)
            
        if self.label_text:
            self.label = lv.label(self.container)
            self.label.set_text(label_text)
            self.label.align(self.canvas, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

            self.label.add_style(lv.label.PART.MAIN,text_style)
            if self.value_text_format:
                self.value_label.align(self.label, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        else:
            self.value_label.align(self.canvas, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

        #bar = lv_bar(container)
        
        p1=lv.point_t()
        p2=lv.point_t()
        point_array=[p1,p2]
        
        # style for horizontal lines
        self.hline_dsc = lv.draw_line_dsc_t()
        self.hline_dsc.init()
        self.hline_dsc.color = self.legend_color
        self.hline_dsc.opa = lv.OPA.COVER
        
        rect_dsc = lv.draw_rect_dsc_t()
        rect_dsc.init()
        rect_dsc.bg_opa = lv.OPA.TRANSP
        rect_dsc.border_color = self.legend_color
        rect_dsc.bg_color = lv_colors.BLACK
        rect_dsc.border_width = 1
        
        # draw the outline, tock marks, legend and value text
        
        self.canvas.draw_rect(0,0,self.width,self.height,rect_dsc)
        if self.divisions > 0:
            dy = (self.height -4)/ self.divisions # Tick marks
            # print("dy: ",dy)
            for tick in range(self.divisions+1):
                ypos = int(dy * tick)
                p1.x = self.width//5
                p1.y = ypos+2
                p2.x = p1.x+self.width - 2*self.width//5
                p2.y = p1.y
                self.canvas.draw_line(point_array,2,self.hline_dsc)
                
                # print("tick: %d, pos: %d"%(tick,p1.y))
                
                if legend:
                    label = lv.label(self.container)
                    label.align(self.canvas,lv.ALIGN.OUT_RIGHT_TOP,5,ypos-5)
                    label.set_text(legend[self.divisions-tick])
                    label.add_style(lv.label.PART.MAIN,text_style)
        self.base = p1.y
        
        # draw the value rectangle
        # print("max: ",self.max_value)
        value_y = round((self.height -4)/(self.max_value - self.min_value) * self.value)
        rect_dsc.bg_color = self.bar_color
        rect_dsc.bg_opa = lv.OPA.COVER
        rect_dsc.border_width = 0
        # print("Pos of last tick: ",p1.y)
        # print("bar height: ",value_y)
        self.canvas.draw_rect(self.width//5+5,self.base-value_y,2*self.width//5 ,value_y ,rect_dsc)

    def set_value(self,value):
        # print("set value: ",value)
        if self.value == value:
            return
        p1=lv.point_t()
        p2=lv.point_t()
        point_array=[p1,p2]

        rect_dsc = lv.draw_rect_dsc_t()
        rect_dsc.init()
        rect_dsc.bg_opa = lv.OPA.COVER
        rect_dsc.border_width = 0
        
        # draw the new bar

        if value > self.value:
            self.value = value
            value_y = round((self.height -4)/(self.max_value - self.min_value) * self.value)
            rect_dsc.bg_color = self.bar_color
            self.canvas.draw_rect(self.width//5+5,self.base-value_y,2*self.width//5 ,value_y ,rect_dsc)
            
        else:
            # remove the difference from the old value from the bar
            old_value_y = round((self.height -4)/(self.max_value - self.min_value) * self.value)
            self.value = value
            value_y = round((self.height -4)/(self.max_value - self.min_value) * self.value)      
            rect_dsc.bg_color = self.bg_color

            self.canvas.draw_rect(self.width//5+5,self.base-old_value_y,2*self.width//5 ,
                                  old_value_y - value_y,rect_dsc)
    
            if self.divisions > 0:
                dy = (self.height -4)/ self.divisions # Tick marks
                # print("dy: ",dy)
                for tick in range(self.divisions+1):
                    ypos = int(dy * tick)
                    p1.x = self.width//5
                    p1.y = ypos+2
                    p2.x = p1.x+self.width - 2*self.width//5
                    p2.y = p1.y
                    if p1.y >= self.base-old_value_y and p1.y < self.base-value_y:
                        self.canvas.draw_line(point_array,2,self.hline_dsc)
                        break
        
        if self.value_text_format:
            value_text = self.value_text_format.format(self.value)
            self.value_label.set_text(value_text)

    def set_x(self,new_x):
        self.container.set_x(new_x)
    def set_y(self,new_y):
        self.container.set_y(new_y)
        
