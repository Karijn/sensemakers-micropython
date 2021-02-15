import network
import os
import ure

global sta_if

class INITBOARD:

  def __init__(self):
    self.selectnetwork = False
    self.selecttouch = False
    self.ssid   = ''
    self.passwd = ''
    self.calibration = None

  def yesno(self, question):
    answer = ' '
    answeri = -1
    while answeri == -1:
      answer = input(question + ' (y/n) ?')
      answeri = "NY".find(answer.upper())
    return True if answeri == 1 else False

  def initboard(self):
    self.initnetwork()
    self.inittouch()

  def initnetwork(self):
    self.selectnetwork = self.yesno('Select network?') 
    if self.selectnetwork:
      self.ssid   = input('Enter SSID     : ')
      self.passwd = input('Enter Password : ')

      try:
        os.mkdir('/config')
      except:
        pass

      f = open('/config/connect.py', "wt")
      # f.write('import ntptime\n')
      # f.write('ntptime.settime()\n')

      f.write('import network\n')
      f.write('sta_if = network.WLAN(network.STA_IF)\n')
      f.write('sta_if.active(True)\n')
      f.write('sta_if.connect("{}", "{}")\n'.format(self.ssid, self.passwd))
 
      f.close()
      print('_connect.py updated')

  def inittouch(self):
    if self.yesno('calibrate touchpanel'):
      import calibrate
      self.selecttouch = True
      self.calibration = calibrate.calibrate() 
      print(self.calibration)
      try:
        os.mkdir('/config')
      except:
        pass
      f = open('/config/touch.py', "wt")
      f.write('touch_calibrate = {}\n'.format(self.calibration))
  
x = INITBOARD()
x.initboard()
