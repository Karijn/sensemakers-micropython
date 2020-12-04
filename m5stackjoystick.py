from machine import Pin, I2C
from time import sleep_ms

'''
usage:
from m5stackjoystick import joy, joyc
joy()
joyc()
'''

def joy():
  i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

  buf = bytearray(3)
  i2c.readfrom_into(82, buf)
  print( 'X = ', buf[0] )
  print( 'Y = ', buf[1] )
  print( 'B = ', buf[2] )


def joyc():
  while(True):
    joy()
    sleep_ms(500)
