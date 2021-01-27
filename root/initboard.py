import network
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

    self.updateboot()


  def initnetwork(self):
    self.selectnetwork = self.yesno('Select network?') 
    if self.selectnetwork:
      self.ssid   = input('Enter SSID     : ')
      self.passwd = input('Enter Password : ')

  def inittouch(self):
    if self.yesno('calibrate touchpanel'):
      import calibrate
      
      self.selecttouch = True
      self.calibration = calibrate.calibrate() 
      print(self.calibration)

  def updateboot(self):
    path = 'boot.py'
    changed = False
    lines = []
    f = open(path, "r")
    for line in f:
      line = ure.sub("[\n\r]", "", line)
      if self.selectnetwork:
        line = ure.sub("sta_if\.connect.*$", "sta_if\.connect('{}', '{}')".format(self.ssid, self.passwd), line)
        changed = True
      lines.append(line)
    f.close()

    for line in lines:
      print(line)
    
    print()
    print('-----------------------------------------------')
    print('-----------------------------------------------')
    print()

    if changed and self.yesno('update boot.py'):
      f = open(path, "w")
      for line in lines:
        f.write(line)
        f.write('\n')
      f.close()
      print('boot.py updated')

x = INITBOARD()
x.initboard()
