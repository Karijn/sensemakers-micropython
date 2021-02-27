from math import sin, cos, radians
import utime as time
from machine import Pin, I2C
import framebuf
import gc

from lib.display.DISPLAY import *
from lib.debug.timings import timed_function
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
r3 = 73
r4 = 78

currenttime=(0, 0, 0, 0, 0, -1, 0)
secs_lines = [[cc_x, cc_y], [cc_x, cc_y]]
mins_lines = [[cc_x, cc_y], [cc_x, cc_y]]
hour_lines = [[cc_x, cc_y], [cc_x, cc_y]]

temps = None
hums = None
tempAvg = None
humAvg = None



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

@timed_function
def create_clock_sprite():
  color = color565(255, 255, 0)
  clock_sprite = FbSprite(r4*2, r4*2)
  clock_sprite.draw_circle(r4, r4, 3, color)
  clock_sprite.draw_circle(r4, r4, r1 - 1, color)
  #clock_sprite.draw_circle(r4, r4, r4 - 1, color)

  for a in range(0, 360 , 6):
    xa = cos(radians(a))
    ya = sin(radians(a))
    rl = r2
    if a % 30 == 0:
      rl = r3
    if a % 45 == 0:
      rl = r4 - 1
    clock_sprite.line( r4 + int(xa * r1), r4 + int(ya * r1), r4 + int(xa * rl), r4 + int(ya * rl), color)
  return clock_sprite

@timed_function
def show_clock(display, clock_sprite, x, y):
  display.blit( clock_sprite, x, y)

@timed_function
def show_clock_hands(display, t, x, y):
  nsecs_lines = rotate_polygon(def_secs_lines, 180 + t[5] * 6, center_point=(x, y))
  nmins_lines = rotate_polygon(def_mins_lines, 180 + t[4] * 6, center_point=(x, y))
  nhour_lines = rotate_polygon(def_hour_lines, 180 + t[3] * 30, center_point=(x, y))
  display.draw_lines(nsecs_lines, color565(0, 255, 0))
  display.draw_lines(nmins_lines, color565(0, 255, 0))
  display.draw_lines(nhour_lines, color565(0, 255, 0))

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

@timed_function
def show_temp_hum(display, sht):
  global temps
  global hums
  global tempAvg
  global humAvg

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
    display.draw_lines(tpoints, color=color565(63, 63, 255))
    display.draw_lines(hpoints, color=color565(255, 63, 63))

    display.text('T:{}'.format(str(mintemp/100)), 2, 255, color565(63, 63, 255))
    display.text('T:{}'.format(str(maxtemp/100)), 2, 215, color565(63, 63, 255))

    display.text('H:{}'.format(str(minhum/100)), 2, 305, color565(255, 63, 63))
    display.text('H:{}'.format(str(maxhum/100)), 2, 265, color565(255, 63, 63))

@timed_function
def clear_screen(display):
  display.fill(0)

def clock():
  global temps
  global hums
  global tempAvg
  global humAvg

  display = getbuffereddisplay(2)

  i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
  sht = sht30.SHT30(i2c, i2c_address=0x45)

  sht.measure_int()

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

  clock_sprite = create_clock_sprite()

  while True:
    gc.collect()
    t = time.localtime(time.time())
    if t[5] != currenttime[5]:
      print('------------------------------')

      starttime = time.ticks_us()

      clear_screen(display)

      display.text('{:02d}-{:02d}-{:04d}  {:02d}:{:02d}:{:02d}'.format(t[2], t[1], t[0], t[3], t[4], t[5]), 32, 5, LemonChiffon)
      show_clock(display, clock_sprite, cc_x - r4, cc_y - r4)

      currenttime = t

      show_clock_hands(display, t, cc_x, cc_y)

      show_temp_hum(display, sht)
      display.show()
      delta = time.ticks_diff(time.ticks_us(), starttime)
      print('{:7.3f} ms  loop'.format(delta/1000))


clock()
