# asyncio version
# The MIT License (MIT)
#
# Copyright (c) 2016, 2017 Robert Hammelrath (basic driver)
#         2016 Peter Hinch (asyncio extension)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Class supporting the resisitve touchpad of TFT LC-displays
#
#import pyb, stm
from machine import SPI, Pin
#from lib.display.DISPLAY import getspi, SLOW_SPI
from time import sleep_ms

try:
  from config.touch import touch_calibrate
  print('/config/touch.py config loaded: ')
except:
  print('/config/touch.py not found')
  touch_calibrate =  (-331,  0.06685,-366,   0.06873,-432,  0.09323,  -437,  0.09545)

# define constants
#
T_GETX  = const(0xd0)  ## 12 bit resolution
T_GETY  = const(0x90)  ## 12 bit resolution
T_GETZ1 = const(0xb8)  ## 8 bit resolution
T_GETZ2 = const(0xc8)  ## 8 bit resolution
#
X_LOW  = const(10)   ## lowest reasonable X value from the touchpad
Y_HIGH = const(4090)   ## highest reasonable Y value


class TOUCH:
#
# Init just sets the PIN's to In / out as required
# async: set True if asynchronous operation intended
# confidence: confidence level - number of consecutive touches with a margin smaller than the given level
#     which the function will sample until it accepts it as a valid touch
# margin: Distance from mean centre at which touches are considered at the same position
# delay: Delay between samples in ms. (n/a if asynchronous)
#
  #  DEFAULT_CAL = (-3917, -0.127, -3923, -0.1267, -3799, -0.07572, -3738,  -0.07814)
  DEFAULT_CAL = (-331,  0.06685,-366,   0.06873,-432,  0.09323,  -437,  0.09545)

  def __init__(self, controller="XPT2046", asyn=False, *, confidence=5, margin=50, delay=10, spi=None, rotation=None):
    print('int new TOUCH, rotation=', rotation)

    # if spi is None:
    #   self.spi = getspi(SLOW_SPI)
    # else:
    #   self.spi = spi
    self.spi = spi
    self.cs = Pin(17, Pin.OUT)
    self.cs.value(1)
    self.recv = bytearray(3)
    self.xmit = bytearray(3)
    # set default values
    self.ready = False
    self.touched = False
    self.x = 0
    self.y = 0
    self.buf_length = 0
    self.rotation = 1
    cal = touch_calibrate# if calibration is None else calibration
    self.asynchronous = False
    self.touch_parameter(confidence, margin, delay, cal)
    if rotation != None:
      self.rotation=rotation

    if asyn:
      self.asynchronous = True
      import uasyncio as asyncio
      loop = asyncio.get_event_loop()
      loop.create_task(self._main_thread())

  def set_rotation(self, rotation):
    self.rotation = rotation


# set parameters for get_touch()
# res: Resolution in bits of the returned values, default = 10
# confidence: confidence level - number of consecutive touches with a margin smaller than the given level
#     which the function will sample until it accepts it as a valid touch
# margin: Difference from mean centre at which touches are considered at the same position
# delay: Delay between samples in ms.
#
  def touch_parameter(self, confidence=5, margin=50, delay=10, calibration=None):
    if not self.asynchronous: # Ignore attempts to change on the fly.
      confidence = max(min(confidence, 25), 5)
      if confidence != self.buf_length:
        self.buff = [[0,0] for x in range(confidence)]
        self.buf_length = confidence
      self.delay = max(min(delay, 100), 5)
      margin = max(min(margin, 100), 1)
      self.margin = margin * margin # store the square value
      if calibration:
        self.calibration = calibration

# get_touch(): Synchronous use. get a touch value; Parameters:
#
# initital: Wait for a non-touch state before getting a sample.
#       True = Initial wait for a non-touch state
#       False = Do not wait for a release
# wait: Wait for a touch or not?
#     False: Do not wait for a touch and return immediately
#     True: Wait until a touch is pressed.
# raw: Setting whether raw touch coordinates (True) or normalized ones (False) are returned
#    setting the calibration vector to (0, 1, 0, 1, 0, 1, 0, 1) result in a identity mapping
# timeout: Longest time (ms, or None = 1 hr) to wait for a touch or release
#
# Return (x,y) or None
#
  def get_touch(self, initial=True, wait=True, raw=False, timeout=None):
    if self.asynchronous:
      return None # Should only be called in synhronous mode
    if timeout is None:
      timeout = 3600000 # set timeout to 1 hour

    if initial:  ## wait for a non-touch state
      sample = True
      while sample and timeout > 0:
        sample = self.raw_touch()
        #print("get_touch() loop 1 sample = ", sample)
        sleep_ms(self.delay)
        timeout -= self.delay
      if timeout <= 0: # after timeout, return None
        return None
    #
    buff = self.buff
    buf_length = self.buf_length
    buffptr = 0
    nsamples = 0
    while timeout > 0:
      if nsamples == buf_length:
        meanx = sum([c[0] for c in buff]) // buf_length
        meany = sum([c[1] for c in buff]) // buf_length
        dev = sum([(c[0] - meanx)**2 + (c[1] - meany)**2 for c in buff]) / buf_length
        if dev <= self.margin: # got one; compare against the square value
          if raw:
            return (meanx, meany)
          else:
            return self.do_normalize((meanx, meany))
      # get a new value
      sample = self.raw_touch()  # get a touch
      #print("get_touch() loop 2 sample = ", sample)
      if sample is None:
        if not wait:
          return None
        nsamples = 0  # Invalidate buff
      else:
        buff[buffptr] = sample # put in buff
        buffptr = (buffptr + 1) % buf_length
        nsamples = min(nsamples + 1, buf_length)
      #pyb.delay(self.delay)
      sleep_ms(self.delay)
      timeout -= self.delay
    return None

# Asynchronous use: this thread maintains self.x and self.y
  async def _main_thread(self):
    import uasyncio as asyncio
    buff = self.buff
    buf_length = self.buf_length
    buffptr = 0
    nsamples = 0
    await asyncio.sleep(0)
    while True:
      if nsamples == buf_length:
        meanx = sum([c[0] for c in buff]) // buf_length
        meany = sum([c[1] for c in buff]) // buf_length
        dev = sum([(c[0] - meanx)**2 + (c[1] - meany)**2 for c in buff]) / buf_length
        if dev <= self.margin: # got one; compare against the square value
          self.ready = True
          self.x, self.y = self.do_normalize((meanx, meany))
      sample = self.raw_touch()  # get a touch
      if sample is None:
        self.touched = False
        self.ready = False
        nsamples = 0  # Invalidate buff
      else:
        self.touched = True
        buff[buffptr] = sample # put in buff
        buffptr = (buffptr + 1) % buf_length
        nsamples = min(nsamples + 1, buf_length)
      await asyncio.sleep(0)

# Asynchronous get_touch
  def get_touch_async(self):
    if self.ready:
      self.ready = False
      return self.x, self.y
    return None
#
# do_normalize(touch)
# calculate the screen coordinates from the touch values, using the calibration values
# touch must be the tuple return by get_touch
#
  def do_normalize(self, touch):
    xmul = self.calibration[3] + (self.calibration[1] - self.calibration[3]) * (touch[1] / 4096)
    xadd = self.calibration[2] + (self.calibration[0] - self.calibration[2]) * (touch[1] / 4096)
    ymul = self.calibration[7] + (self.calibration[5] - self.calibration[7]) * (touch[0] / 4096)
    yadd = self.calibration[6] + (self.calibration[4] - self.calibration[6]) * (touch[0] / 4096)
    x = int((touch[0] + xadd) * xmul)
    y = int((touch[1] + yadd) * ymul)

    #print(" rotation {} (x, y) ({}, {})".format(self.rotation, x, y), end="")
    if self.rotation == 0:
      x = x
      y = y
    elif self.rotation == 1:
      t = y
      y = 240 -x
      x = t
    elif self.rotation == 2:
      x = 240 - x
      y = 320 - y
    elif self.rotation == 3:
      t = 320 - y
      y = x
      x = t
    elif self.rotation == 4:
      x = x
      y = 320-y
    elif self.rotation == 5:
      t = y
      y = x
      x = t
    elif self.rotation == 6:
      x = 240-x
      y = y
    else: # 7
      t = 320 - y
      y = 240-x
      x = t

    #print("(x, y) (", x, ", ", y, ")")

    return (x, y)
#
# raw_touch(tuple)
# raw read touch. Returns (x,y) or None
#
  def raw_touch(self):
    global CONTROL_PORT
    self.cs.value(0)
    x  = self.touch_talk(T_GETX, 12)
    y  = self.touch_talk(T_GETY, 12)
    self.cs.value(1)
    if x > X_LOW and y < Y_HIGH:  # touch pressed?
      return (x, y)
    else:
      return None
#
# Send a command to the touch controller and wait for the response
# cmd:  command byte
# bits: expected data size. Reasonable values are 8 and 12
#
  def touch_talk(self, cmd, bits):
    self.xmit[0] = cmd

    self.spi.write_readinto(self.xmit, self.recv)
    
    return (self.recv[1] * 256 + self.recv[2]) >> (15 - bits)