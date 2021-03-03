import machine
import time

from lib.sensors.nunchuck import *


"""
proudly stolen from: https://github.com/kfricke/micropython-nunchuck

The MIT License (MIT)

Copyright (c) 2015 Kai Fricke

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

© 2021 GitHub, Inc.
"""
nun = Nunchuck(machine.I2C(
    scl=machine.Pin(5),
    sda=machine.Pin(4),
    freq=100000
    ))

x = 0
y = 0
while True:
  if not nun.joystick_center():
    if nun.joystick_up():
      y += 1
    elif nun.joystick_down():
      y -= 1
    if nun.joystick_left():
      x -= 1
    elif nun.joystick_right():
      x += 1
  print(x, y, nun.joystick_x(), nun.joystick_y(), end='   ')

  j = nun.joystick()
  a = nun.accelerator()
  b = nun.buttons()
  jx = nun.joystick_x()
  jy = nun.joystick_y()
  print("Joystick: X={0: <4} Y={1: <4}  Accelerator: X={2: <3} Y={3: <3} Z={4: <3} Buttons: C={5} Z={6}".format(
      j[0], j[1],
      a[0], a[1], a[2],
      b[0], b[1]
      ))

  time.sleep_ms(100)