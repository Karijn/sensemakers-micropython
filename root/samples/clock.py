from lib.display.DISPLAY import *
from lib.display.displayext import DisplayExt
from math import sin, cos, radians
import utime as time
from machine import Pin, I2C
import framebuf

#import lib.fonts.roboto_cond_reg_16
from lib.sensors import sht30

from lib.display.colors import *


class Avg:
  def __init__(self, maxItems):
    self._avgArray = []
    self._add = 0
    self._maxItems = maxItems

  def Add(self, val):
    self._avgArray.append(val)
    self._add += val
    if(len(self._avgArray) > self._maxItems):
      m = self._avgArray.pop(0)
      self._add -= m

  def Get(self):
    l = len(self._avgArray)
    if l == 0:
      return 0
    return self._add / l 

  def All(self):
    return self._avgArray
    


#seed(ticks_cpu())

cc_x = 120  # center click
cc_y = 110
sec_l = 50  # length sec
min_l = 45  # length min
min_w = 2   # width min
min_wd = 15 # width offset min
hr_l = 40   # length hour
hr_w = 5    # width hour
hr_wd = 10   # width offset hour

def_secs_lines = [[cc_x, cc_y + 5], [cc_x,         cc_y + sec_l]]
def_mins_lines = [[cc_x, cc_y + 5], [cc_x + min_w, cc_y + min_wd], [cc_x, cc_y + min_l], [cc_x - min_w, cc_y + min_wd], [cc_x, cc_y + 5]] 
def_hour_lines = [[cc_x, cc_y + 5], [cc_x + hr_w,  cc_y + hr_wd],  [cc_x, cc_y + hr_l],  [cc_x - hr_w,  cc_y + hr_wd],  [cc_x, cc_y + 5]] 

r1 = 60
r2 = 70

currenttime=(0, 0, 0, 0, 0, -1, 0)
secs_lines = [[cc_x, cc_y], [cc_x, cc_y]]
mins_lines = [[cc_x, cc_y], [cc_x, cc_y]]
hour_lines = [[cc_x, cc_y], [cc_x, cc_y]]

def rotate_point(point, angle, center_point=(0, 0)):
  """Rotates a point around center_point(origin by default)
  Angle is in degrees.
  Rotation is counter-clockwise
  """
  angle_rad = radians(angle % 360)
  # Shift the point so that center_point becomes the origin
  new_point = (point[0] - center_point[0], point[1] - center_point[1])
  new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
  # Reverse the shifting we have done
  new_point = (int(new_point[0] + center_point[0]), int(new_point[1] + center_point[1]))
  return new_point

def rotate_polygon(polygon, angle, center_point=(0, 0)):
  """Rotates the given polygon which consists of corners represented as (x,y)
  around center_point (origin by default)
  Rotation is counter-clockwise
  Angle is in degrees
  """
  rotated_polygon = []
  for corner in polygon:
    rotated_corner = rotate_point(corner, angle, center_point)
    rotated_polygon.append(rotated_corner)
  return rotated_polygon

def draw_clock(surface, x, y, r1, r2, color):
  surface.draw_circle(cc_x, cc_y, 3, color)
  surface.draw_circle(cc_x, cc_y, r1 - 1, color)
  surface.draw_circle(cc_x, cc_y, r2 + 8, color)

  for a in range(0, 360 , 6):
    xa = cos(radians(a))
    ya = sin(radians(a))
    r3 = r2
    if a % 30 == 0:
      r3 += 3
    if a % 45 == 0:
      r3 += 4
    surface.line( x + int(xa * r1), y + int(ya * r1), x + int(xa * r3), y + int(ya * r3), color)

def map(x, in_min, in_max, out_min, out_max):
  div = (in_max - in_min) 
  if div == 0:
    div = 1
  out = (x - in_min) * (out_max - out_min) / div + out_min
  #print ('{} = map({}, {}, {}, {}, {}) (div = {})'.format(out, x, in_min, in_max, out_min, out_max, div))
  return out

def make_point_array(values, minval, maxval, top, bottom):
  index = 60
  pointsval = []
  for val in values:
    v = map(val, in_min = minval, in_max = maxval, out_min = top, out_max = bottom)
    pointsval.append([index, int(v)])
    index += 2
  return pointsval

def test():
  display = getdisplay(2)

  i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
  sht = sht30.SHT30(i2c, i2c_address=0x45)
  # sht.is_present()
  # sht.status()
  # sht.measure()
  sht.measure_int()

  buf = bytearray(display.width * display.height * 2)
  fbuf = DisplayExt(framebuf.FrameBuffer(buf, display.width, display.height, framebuf.RGB565), framebuf.RGB565)

  currenttime = [0, 0, 0, 0, 0, 0]
  # 1st time init
  temps = Avg(60)
  hums = Avg(60)
  tempAvg = Avg(60)
  humAvg = Avg(60)

  temp, hum = sht.measure()
  tempAvg.Add(int(temp * 100))
  humAvg.Add(int(hum * 100))
  temps.Add(int(tempAvg.Get()))
  hums.Add(int(humAvg.Get()))

  is_first_time = True

  while True:
    t = time.localtime(time.time())
    if t[5] != currenttime[5]:

      fbuf.fill(color565(0, 0, 0))
      fbuf.text('{:02d}-{:02d}-{:04d}  {:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[3], t[4], t[5]), 32, 5, LemonChiffon)
      draw_clock(fbuf, cc_x, cc_y, 60, 80, color565(255, 255, 255))

      currenttime = t

      nsecs_lines = rotate_polygon(def_secs_lines, 180 + t[5] * 6, center_point=(cc_x, cc_y))
      nmins_lines = rotate_polygon(def_mins_lines, 180 + t[4] * 6, center_point=(cc_x, cc_y))
      nhour_lines = rotate_polygon(def_hour_lines, 180 + t[3] * 30, center_point=(cc_x, cc_y))

      fbuf.draw_lines(nsecs_lines, color565(0, 255, 0))
      fbuf.draw_lines(nmins_lines, color565(0, 255, 0))
      fbuf.draw_lines(nhour_lines, color565(0, 255, 0))

      temp, hum = sht.measure()
      tempAvg.Add(int(temp * 100))
      humAvg.Add(int(hum * 100))

      temps.Add(int(tempAvg.Get()))
      hums.Add(int(humAvg.Get()))

      mintemp = min(temps.All())
      maxtemp = max(temps.All())
      minhum = min(hums.All())
      maxhum = max(hums.All())
      tpoints = make_point_array(temps.All(), mintemp, maxtemp, 255, 215)
      hpoints = make_point_array(hums.All(), minhum, maxhum, 305, 265)

      if len(tpoints) > 1:
        #fbuf.fill_rect(0, 200, 240, 115, color565(0, 0, 0))
        fbuf.draw_lines(tpoints, color=color565(63, 63, 255))
        fbuf.draw_lines(hpoints, color=color565(255, 63, 63))

        fbuf.text('T:{}'.format(str(mintemp/100)), 2, 255, color565(63, 63, 255))
        fbuf.text('T:{}'.format(str(maxtemp/100)), 2, 215, color565(63, 63, 255))

        fbuf.text('H:{}'.format(str(minhum/100)), 2, 305, color565(255, 63, 63))
        fbuf.text('H:{}'.format(str(maxhum/100)), 2, 265, color565(255, 63, 63))

      display.draw_sprite(buf, 0, 0, display.width, display.height)

test()
