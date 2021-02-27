from machine import Pin, I2C

class joystick():

  def __init__(self, i2c = None, address = 0x52):
    if i2c is None:
      i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    self.i2c = i2c
    self.address = address

  def readx(self):
    buf = self.i2c.readfrom(self.address, 3)
    return buf[0]

  def ready(self):
    buf = self.i2c.readfrom(self.address, 3)
    return buf[1]

  def readz(self):
    buf = self.i2c.readfrom(self.address, 3)
    return buf[2] == 1

  def readxy(self):
    buf = self.i2c.readfrom(self.address, 3)
    return buf[0], buf[1]

  def readxyz(self):
    buf = self.i2c.readfrom(self.address, 3)
    return buf[0], buf[1], buf[2] == 1

  
def test():
  j = joystick()

  while True:
    x, y, z = j.readxyz()
    print( 'X = {}, y = {}, z = {}'.format(x, y, z))

test()
