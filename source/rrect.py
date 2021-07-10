from lib.display.DISPLAY import *
from math import sin, cos, radians
import lib.fonts.roboto_cond_reg_16
import utime as time
from machine import Pin, I2C
from lib.sensors import sht30


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
    
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

sht = sht30.SHT30(i2c, i2c_address=0x45)
sht.is_present()
sht.status()
sht.measure()
sht.measure_int()

font = lib.fonts.roboto_cond_reg_16

setrotation(0)
display=getdisplay()
display.clear(0)
display.set_font(font)

cc_x = 120  # center click
cc_y = 110
sec_l = 50  # length sec
min_l = 40  # length min
min_w = 2   # width min
min_wd = 10 # width offset min
hr_l = 30   # length hour
hr_w = 5    # width hour
hr_wd = 5   # width offset hour

def_secs_lines = [[cc_x, cc_y], [cc_x,         cc_y + sec_l]]
def_mins_lines = [[cc_x, cc_y], [cc_x + min_w, cc_y + min_wd], [cc_x, cc_y + min_l], [cc_x - min_w, cc_y + min_wd], [cc_x, cc_y]] 
def_hour_lines = [[cc_x, cc_y], [cc_x + hr_w,  cc_y + hr_wd],  [cc_x, cc_y + hr_l],  [cc_x - hr_w,  cc_y + hr_wd],  [cc_x, cc_y]] 

r1 = 60
r2 = 70

currenttime=(0, 0, 0, 0, 0, -1, 0)
secs_lines = [[cc_x, cc_y], [cc_x, cc_y]]
mins_lines = [[cc_x, cc_y], [cc_x, cc_y]]
hour_lines = [[cc_x, cc_y], [cc_x, cc_y]]

temps = Avg(60)
hums = Avg(60)
tempAvg = Avg(60)
humAvg = Avg(60)


#display.draw_rrectangle()
#display.fill_rrectangle()

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

def daylight(now,offset):
  rt = time.localtime(now)
  nows = now + (11 - rt[1]) * 2592000 # about mid November
  # work back to find Sunday Oct
  while time.localtime(nows)[1] != 10: #Oct
    nows -= 86400
  while time.localtime(nows)[6] != 6: #Sun
    nows -= 86400
  nowsOct = nows
  # work back to find Sunday Mar
  while time.localtime(nows)[1] != 3: #Mar
    nows -= 86400
  while time.localtime(nows)[6] != 6: #Sun
    nows -= 86400
  nowsMar = nows
  # saving is used between dates
  if (now > nowsMar) and (now < nowsOct):
    now += (3600 * offset)
  return now

def draw_clock(x, y, r1, r2, color):
  for a in range(0, 360 , 6):
    xa = cos(radians(a))
    ya = sin(radians(a))
    r3 = r2
    if a % 30 == 0:
      r3 += 3
    if a % 45 == 0:
      r3 += 4
    display.line( x + int(xa * r1), y + int(ya * r1), x + int(xa * r3), y + int(ya * r3), color)

def draw_scale(x, y, r1, r2, color):
  for a in range(180 - 45, 360 + 46, 5):
    xa = cos(radians(a))
    ya = sin(radians(a))
    r3 = r2
    if a % 15 == 0:
      r3 += 3
    if a % 45 == 0:
      r3 += 4
    display.line( x + int(xa * r1), y + int(ya * r1), x + int(xa * r3), y + int(ya * r3), color)


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


display.clear(0)

draw_clock(cc_x, cc_y, r1, r2, color565(255, 255, 0))

# 1st time init
temp, hum = sht.measure()
tempAvg.Add(int(temp * 100))
humAvg.Add(int(hum * 100))
temps.Add(int(tempAvg.Get()))
hums.Add(int(humAvg.Get()))

is_first_time = True

while True:
  updategraph=is_first_time
  is_first_time = False
  t = time.localtime(time.time())

  if t[5] != currenttime[5]:
    text = '  {}/{}/{} {}:{}:{}  '.format(t[0], t[1], t[2], t[3], t[4], t[5])
    w = font.get_width(text)
    display.set_pos(cc_x - int(w/2), 20)
    display.print(text)

    temp, hum = sht.measure()
    tempAvg.Add(int(temp * 100))
    humAvg.Add(int(hum * 100))

    if t[4] != currenttime[4]:
      display.draw_lines(mins_lines, color=color565(0, 0, 0))

      temps.Add(int(tempAvg.Get()))
      hums.Add(int(humAvg.Get()))

      mintemp = min(temps.All())
      maxtemp = max(temps.All())
      minhum = min(hums.All())
      maxhum = max(hums.All())
      tpoints = make_point_array(temps.All(), mintemp, maxtemp, 250, 210)
      hpoints = make_point_array(hums.All(), minhum, maxhum, 300, 260)
      updategraph = True

    nsecs_lines = rotate_polygon(def_secs_lines, 180 + t[5] * 6, center_point=(cc_x, cc_y))
    nmins_lines = rotate_polygon(def_mins_lines, 180 + t[4] * 6, center_point=(cc_x, cc_y))
    nhour_lines = rotate_polygon(def_hour_lines, 180 + t[3] * 30, center_point=(cc_x, cc_y))

    if t[3] != currenttime[3]:
      display.draw_lines(hour_lines, color=color565(0, 0, 0))
    if t[4] != currenttime[4]:
      display.draw_lines(mins_lines, color=color565(0, 0, 0))
    display.draw_lines(secs_lines, color=color565(0, 0, 0))

    display.draw_lines(nhour_lines, color=color565(255, 0, 0))
    display.draw_lines(nmins_lines, color=color565(0, 255, 0))
    display.draw_lines(nsecs_lines, color=color565(0, 0, 255))

    hour_lines = nhour_lines
    mins_lines = nmins_lines
    secs_lines = nsecs_lines

    if updategraph:
      if len(tpoints) > 1:
        display.fill_rect(0, 200, 240, 115, color565(0, 0, 0))
        display.draw_lines(tpoints, color=color565(128, 128, 255))
        display.draw_lines(hpoints, color=color565(255, 128, 128))

        display.set_color(color565(128, 128, 255), color565(0, 0, 0))
        display.set_pos(2, 235)
        display.print("T: " + str(mintemp/100)) 
        display.set_pos(2, 200)
        display.print("T: " + str(maxtemp/100)) 

        display.set_color(color565(255, 128, 128), color565(0, 0, 0))
        display.set_pos(2, 295)
        display.print("H: " + str(minhum/100)) 
        display.set_pos(2, 260)
        display.print("H: " + str(maxhum/100)) 
    currenttime = t
